# serializers.py

def user_serializer(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password
    }

def clothes_serializer(cloth):
    return {
        "id": cloth.id,
        "name": cloth.name,
        "description": cloth.description,
        "price": cloth.price,
        "image_url": cloth.image_url
    }

def whatsnew_serializer(item):
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "image_url": item.image_url,
        "release_date": item.release_date
    }

def flashsale_serializer(sale):
    return {
        "id": sale.id,
        "name": sale.name,
        "discount": sale.discount,
        "start_time": sale.start_time,
        "end_time": sale.end_time
    }

def hotincategory_serializer(item):
    return {
        "id": item.id,
        "category": item.category,
        "product_id": item.product_id
    }

def artwork_serializer(art):
    return {
        "id": art.id,
        "title": art.title,
        "artist_name": art.artist_name,
        "image_url": art.image_url,
        "price": art.price
    }

def shoes_serializer(shoe):
    return {
        "id": shoe.id,
        "name": shoe.name,
        "size": shoe.size,
        "price": shoe.price,
        "image_url": shoe.image_url
    }

def electronics_serializer(electronic):
    return {
        "id": electronic.id,
        "name": electronic.name,
        "description": electronic.description,
        "price": electronic.price,
        "image_url": electronic.image_url
    }

def book_serializer(book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "image_url": book.image_url
    }

def cart_serializer(cart):
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "total_price": cart.total_price
    }

def cartitem_serializer(item):
    return {
        "id": item.id,
        "cart_id": item.cart_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }
