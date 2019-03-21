from products.models import Category
from utils import memoize


@memoize
def product_categories(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }