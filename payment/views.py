from django.shortcuts import redirect
from django.conf import settings
from group.models import Group
from activity.models import Activity
from django.http import HttpResponse
from .serializers import CouponCreateSerializer, PriceCreateSerializer, ProductCreateSerializer
from rest_framework import status, views, permissions, response, parsers, generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.contrib.auth import get_user_model
User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.get("product")
            serializer = ProductCreateSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                group = Group.objects.select_related('author').get(
                    author__username=request.user.username
                )
                if(len(group.product_id) > 0):
                    product = stripe.Product.modify(
                        group.product_id,
                        name="soho/" + request.user.username,
                        images=data["images"]
                    )
                else:
                    product = stripe.Product.create(
                        name="soho/" + request.user.username,
                        metadata={
                            "user_id": request.user.id,
                            "group_id": group.id,
                            "email": request.user.email
                        },
                        images=data["images"]
                    )

                    group.product_id = product.id
                    group.product_image = product.images[0]
                    group.save()

                return response.Response({
                    'product': product,
                })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PaymentPriceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.get("price")
            serializer = PriceCreateSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                group = Group.objects.select_related('author').get(
                    author__username=request.user.username
                )
                if(len(group.product_id) > 0):
                    product = stripe.Product.retrieve(group.product_id)
                    if(len(group.price_id) > 0):
                        stripe.Price.modify(
                            group.price_id,
                            active=False
                        )

                    price = stripe.Price.create(
                        currency=data["currency"],
                        billing_scheme="per_unit",
                        product=product.id,
                        unit_amount=data["unit_amount"],
                        recurring={
                            "interval": data["sub_interval"],
                            "interval_count": 1
                        },
                        metadata={
                            "user_id": request.user.id,
                            "group_id": group.id,
                            "email": request.user.email
                        }
                    )

                    group.price_id = price.id
                    group.currency = price.currency
                    group.unit_amount = price.unit_amount
                    price.sub_interval = price.recurring.interval
                    group.save()

                    return response.Response({
                        'price': price,
                    })
                else:
                    raise NotFound(detail="Error 404, Not Found!", code=404)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PaymentCouponView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.get("coupon")
            serializer = CouponCreateSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                group = Group.objects.select_related('author').get(
                    author__username=request.user.username
                )
                if(len(group.product_id) > 0):
                    product = stripe.Product.retrieve(group.product_id)
                    if(len(group.coupon_id) > 0):
                        stripe.Coupon.delete(group.coupon_id)

                    coupon = stripe.Coupon.create(
                        percent_off=data["percent_off"],
                        currency=group.currency,
                        duration="once",
                        applies_to={
                            "products": [product.id]
                        },
                        metadata={
                            "user_id": request.user.id,
                            "group_id": group.id,
                            "email": request.user.email
                        }
                    )

                    group.coupon_id = coupon.id
                    group.percent_off = coupon.percent_off

                    if(len(group.promotion_id) > 0):
                        stripe.PromotionCode.modify(
                            group.promotion_id,
                            active=False
                        )

                    promotion = stripe.PromotionCode.create(
                        coupon=coupon.id,
                        metadata={
                            "user_id": request.user.id,
                            "group_id": group.id,
                            "email": request.user.email
                        }
                    )

                    group.promotion_id = promotion.id
                    group.promotion_code = promotion.code

                    group.save()

                    return response.Response({
                        'coupon': coupon,
                        'promotion': promotion
                    })
                else:
                    raise NotFound(detail="Error 404, Not Found!", code=404)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
    
    def delete(self, request):
        try:
            promotion_id = request.query_params["promotion_id"]
            group = Group.objects.select_related('author').get(
                    author__username=request.user.username
                )
            if(group.promotion_id == promotion_id):
                stripe.PromotionCode.modify(
                    group.promotion_id,
                    active=False
                )
                group.promotion_id = ""
                group.promotion_code = ""
                group.coupon_id = ""
                group.percent_off = 0
                group.save()
            else:
                raise NotFound(detail="Error 404, Not Found!", code=404)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PaymentCheckoutView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            price_id = request.query_params["price_id"]
            username = request.query_params["username"]
            user = User.objects.get(username=username)
            group = Group.objects.get(price_id=price_id)
            if(group and len(group.price_id) > 0 and len(group.product_id) > 0):
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price': group.price_id,
                            'quantity': 1,
                        },
                    ],
                    allow_promotion_codes=True,
                    metadata={
                        "user_id": user.id,
                        "user_email": user.email,
                        "group_id": group.id
                    },
                    mode='subscription',
                    success_url=settings.FRONTEND_URL +
                    '/payment/?success=true&session_id={CHECKOUP_SESSION_ID}',
                    cancel_url=settings.FRONTEND_URL + '/payment/?cancelled=true',
                )
                return redirect(checkout_session.url)
            else:
                return redirect(settings.FRONTEND_URL + '/payment/?failed=true')
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PaymentWebhookView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_KEY
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
            print(line_items["data"])
            # subscribe user to group
            # send notification to user
            # send notification to group

        # Passed signature verification
        return HttpResponse(status=200)
