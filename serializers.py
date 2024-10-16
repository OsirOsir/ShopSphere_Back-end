def user_serializer(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }

def item_serializer(item):
    return {
        "id": item.id,
        "item_name": item.item_name,  # Updated to match your models.py
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "product_quantity": item.product_quantity,  # Preserved from the 'products' version
        "items_available": item.items_available,  # If needed, you can choose to keep or remove
        "offer_price": item.offer_price,  # If needed, you can choose to keep or remove
        "image_url": item.image_url,
        "is_in_stock": item.is_in_stock(),  
    }

def notification_serializer(notification):
    """Serialize a Notification object into a dictionary."""
    return {
        'id': notification.id,
        'user_id': notification.user_id,
        'item_id': notification.item_id,
        'item_name': notification.item.item_name,  
        'message': notification.message
    }
