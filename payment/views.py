from django.shortcuts import redirect
from django.conf import settings
from group.models import Group
from .models import Payment
from .serializers import PaymentSerializer
from activity.models import Activity
from django.http import HttpResponse
from .serializers import CouponCreateSerializer, PriceCreateSerializer, ProductCreateSerializer
from rest_framework import status, views, permissions, response, parsers, generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
import stripe
from utils.paginations import PazeSizePagination
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
                    product = stripe.Product.modify(group.product_id, name=request.user.username)
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
                    group.sub_interval = price.recurring.interval
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
                    product = stripe.Product.modify(group.product_id, name=request.user.username)
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
            payor = request.query_params["payor"]
            payor_user = User.objects.get(username=payor)
            payee_group = Group.objects.get(price_id=price_id)

            if(payee_group and len(payee_group.price_id) > 0 and len(payee_group.product_id) > 0):
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price': payee_group.price_id,
                            'quantity': 1,
                        },
                    ],
                    allow_promotion_codes=True,
                    metadata={
                        "payor": payor_user.id,
                        "payee": payee_group.author.id,
                    },
                    mode='subscription',
                    success_url=settings.FRONTEND_URL +
                    '/payment/?success=true&session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=settings.FRONTEND_URL + '/payment/?cancelled=true',
                )
                p = Payment(payor=payor_user, 
                            payee=payee_group.author,
                            checkout_id=checkout_session.id,
                            amount=payee_group.unit_amount,
                            currency=payee_group.currency,
                            interval=payee_group.sub_interval)
                p.save()
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
            line_items = stripe.checkout.Session.list_line_items(
                session['id'], limit=1)
            res = line_items["data"][0]
            
            payment = Payment.objects.get(checkout_id=event.data.object.id, completed=False)
            payment.amount = res.amount_total
            payment.completed = True
            payment.save()

            # subscribe
            group = Group.objects.select_related('author').get(
                author__id=payment.payee.id
            )
            group.subscribers.add(payment.payor.id)
            # send notification to group and user
            Activity.objects.create(target=payment.payor.id, group_id=int(res.price.metadata.group_id),
                                        sender_id=payment.payee.id, target_type="user", verb="joined")

        # Passed signature verification
        return HttpResponse(status=200)

class PayorPaymentView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    pagination_class = PazeSizePagination

    def get_queryset(self):
        return Payment.finished.filter(payor__id=self.request.user.id)

class PayeePaymentView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    pagination_class = PazeSizePagination

    def get_queryset(self):
        return Payment.finished.filter(payee__id=self.request.user.id)