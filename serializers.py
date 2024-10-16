# serializers.py

def user_serializer(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }  # Closing the dictionary here

def item_serializer(item):
    return {
        "id": item.id,
        "item_name": item.item_name,  # Correct field name
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "items_available": item.items_available,  # Use items_available instead of product_quantity
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
