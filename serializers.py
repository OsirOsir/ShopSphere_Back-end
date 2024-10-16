# serializers.py

def item_serializer(item):
    return {
        "id": item.id,
        "item_name": item.item_name,
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "items_available": item.items_available,
        "offer_price": item.offer_price,
        "image_url": item.image_url
    }
