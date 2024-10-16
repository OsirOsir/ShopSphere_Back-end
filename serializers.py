# serializers.py

def user_serializer(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }  # Make sure to close the dictionary here

def item_serializer(item):
    return {
        "id": item.id,
        "name": item.item_name,  # Updated key to match your models.py
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "items_available": item.items_available,
        "offer_price": item.offer_price,
        "image_url": item.image_url
    }
