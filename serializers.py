def user_serializer(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,  # From the 'authentication' branch
        "products": [product_serializer(product) for product in user.products] if user.is_admin() else []  # From 'authentication'
    }

def product_serializer(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "item_availability": product.item_availability,  # From 'main'
    }  # Closing the dictionary here

def item_serializer(item):
    return {
        "id": item.id,
        "item_name": item.item_name,  # Correct field name
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "items_available": item.items_available,  # Use items_available instead of product_quantity
        "offer_price": item.offer_price,
        "image_url": item.image_url,
        "is_in_stock": item.is_in_stock(),  # Calling the method to check stock
    }


def notification_serializer(notification):
    """Serialize a Notification object into a dictionary."""
    return {
        'id': notification.id,
        'user_id': notification.user_id,
        'item_id': notification.item_id,
        'item_name': notification.item.item_name,  # Accessing item details
        'message': notification.message
    }
