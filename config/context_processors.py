from app.models import Category, Collection, WebsiteInfo


def nav_processor(request):
    categories = Category.objects.all()
    collections = Collection.objects.values('name', 'slug')
    website_info = WebsiteInfo.objects.get(pk=1)

    context = {
        'categories_context': categories,
        'collections_context': collections,
        'website_info_context': website_info,
    }

    return context
