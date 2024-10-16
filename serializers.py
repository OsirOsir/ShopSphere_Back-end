# def user_serializer(user):
#     return {
#         "id": user.id,
#         "name": user.name,
#         "email": user.email,
       
# # serializers.py

# def item_serializer(item):
#     return {
#         "id": item.id,
#         "name": item.name,
#         "description": item.description,
#         "price": item.price,
#         "category": item.category,
#         "items_available": item.items_available,
#         "offer_price": item.offer_price,
#         "image_url": item.image_url
#     }


# serializers.py

def item_serializer(item):
    return {
        'id': item.id,
        'item_name': item.item_name,
        'description': item.description,
        'price': item.price,
        'category': item.category,
        'product_quantity': item.product_quantity,
        'image_url': item.image_url,
        'is_in_stock': item.is_in_stock()  
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
