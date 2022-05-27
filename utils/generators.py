from django.utils.text import slugify

def generate_unique_username(instance):
    full_name = instance.first_name + '-' + instance.last_name
    origin_username = slugify(full_name)
    unique_username = origin_username
    numb = 1
    klass = instance.__class__
    if instance is not None:
        while klass.objects.filter(username=unique_username).exclude(id=instance.id).exists():
            unique_username = '%s-%d' % (origin_username, numb)
            numb += 1
    else:
        while klass.objects.filter(username=unique_username).exists():
            unique_username = '%s-%d' % (origin_username, numb)
            numb += 1
    return unique_username

def generate_unique_slug(klass, field, instance=None):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    if instance is not None:
        while klass.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
    else:
        while klass.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
    return unique_slug