def save_products_image(instance, filename):
    return 'products/' + '/'.join([instance.product.name, filename])


def save_collections_image(instance, filename):
    return 'collections/' + '/'.join([instance.name, filename])
