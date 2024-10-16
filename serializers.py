def user_serializer(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "products": [product_serializer(product) for product in user.products] if user.is_admin() else []
    }

def product_serializer(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "item_availability": product.item_availability,
    }
