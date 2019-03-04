from django.utils.text import slugify
import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_order_id_generator(instance, new_order_id=None):
    """
    Generate a unique id(uppercase)
    """
    if new_order_id is not None:
        order_id = new_order_id
    Klass = instance.__class__
    # check if same order_id exists
    # qs_exists = Klass.objects.filter(order_id=order_id).exists()
    qs_exists = False
    if qs_exists:
        new_order_id = "{randstr}".format(
            randstr=random_string_generator(
                size=10, chars=string.ascii_uppercase + string.digits))
        return unique_order_id_generator(instance, new_order_id=new_order_id)
    return new_order_id
