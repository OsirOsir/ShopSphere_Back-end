from flask import Flask, jsonify, request
from models import db, User, Clothes, WhatsNew, FlashSale, HotInCategory, Artwork, Shoes, Electronics, Book, Cart, CartItem
from flask_migrate import Migrate

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://groupthree:group3@localhost/shop_sphere'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return f"<h1>Welcome to ShopSphere</h1>"



@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user_serializer(user) for user in users])
    
    elif request.method == 'POST':
        data = request.json
        new_user = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_serializer(new_user)), 201

@app.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def handle_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify(user_serializer(user))
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with id {user_id} has been deleted"}


# --- Clothes ---
@app.route('/clothes', methods=['GET', 'POST'])
def handle_clothes():
    if request.method == 'GET':
        clothes = Clothes.query.all()
        return jsonify([clothes_serializer(cloth) for cloth in clothes])
    
    elif request.method == 'POST':
        data = request.json
        new_cloth = Clothes(name=data['name'], description=data['description'], price=data['price'], image_url=data['image_url'])
        db.session.add(new_cloth)
        db.session.commit()
        return jsonify(clothes_serializer(new_cloth)), 201

@app.route('/clothes/<int:cloth_id>', methods=['GET', 'DELETE'])
def handle_cloth(cloth_id):
    cloth = Clothes.query.get_or_404(cloth_id)

    if request.method == 'GET':
        return jsonify(clothes_serializer(cloth))
    
    elif request.method == 'DELETE':
        db.session.delete(cloth)
        db.session.commit()
        return {"message": f"Cloth with id {cloth_id} has been deleted"}


# --- WhatsNew ---
@app.route('/whatsnew', methods=['GET', 'POST'])
def handle_whatsnew():
    if request.method == 'GET':
        items = WhatsNew.query.all()
        return jsonify([whatsnew_serializer(item) for item in items])
    
    elif request.method == 'POST':
        data = request.json
        new_item = WhatsNew(title=data['title'], description=data['description'], image_url=data['image_url'], release_date=data['release_date'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(whatsnew_serializer(new_item)), 201

@app.route('/whatsnew/<int:item_id>', methods=['GET', 'DELETE'])
def handle_whatsnew_item(item_id):
    item = WhatsNew.query.get_or_404(item_id)

    if request.method == 'GET':
        return jsonify(whatsnew_serializer(item))
    
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return {"message": f"WhatsNew item with id {item_id} has been deleted"}


# --- FlashSale ---
@app.route('/flashsale', methods=['GET', 'POST'])
def handle_flashsale():
    if request.method == 'GET':
        sales = FlashSale.query.all()
        return jsonify([flashsale_serializer(sale) for sale in sales])
    
    elif request.method == 'POST':
        data = request.json
        new_sale = FlashSale(name=data['name'], discount=data['discount'], start_time=data['start_time'], end_time=data['end_time'])
        db.session.add(new_sale)
        db.session.commit()
        return jsonify(flashsale_serializer(new_sale)), 201

@app.route('/flashsale/<int:sale_id>', methods=['GET', 'DELETE'])
def handle_flashsale_item(sale_id):
    sale = FlashSale.query.get_or_404(sale_id)

    if request.method == 'GET':
        return jsonify(flashsale_serializer(sale))
    
    elif request.method == 'DELETE':
        db.session.delete(sale)
        db.session.commit()
        return {"message": f"FlashSale with id {sale_id} has been deleted"}


# --- HotInCategory ---
@app.route('/hotincategory', methods=['GET', 'POST'])
def handle_hotincategory():
    if request.method == 'GET':
        items = HotInCategory.query.all()
        return jsonify([hotincategory_serializer(item) for item in items])
    
    elif request.method == 'POST':
        data = request.json
        new_item = HotInCategory(category=data['category'], product_id=data['product_id'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(hotincategory_serializer(new_item)), 201

@app.route('/hotincategory/<int:item_id>', methods=['GET', 'DELETE'])
def handle_hotincategory_item(item_id):
    item = HotInCategory.query.get_or_404(item_id)

    if request.method == 'GET':
        return jsonify(hotincategory_serializer(item))
    
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return {"message": f"HotInCategory item with id {item_id} has been deleted"}


# --- Artwork ---
@app.route('/artwork', methods=['GET', 'POST'])
def handle_artwork():
    if request.method == 'GET':
        artworks = Artwork.query.all()
        return jsonify([artwork_serializer(art) for art in artworks])
    
    elif request.method == 'POST':
        data = request.json
        new_artwork = Artwork(title=data['title'], artist_name=data['artist_name'], image_url=data['image_url'], price=data['price'])
        db.session.add(new_artwork)
        db.session.commit()
        return jsonify(artwork_serializer(new_artwork)), 201

@app.route('/artwork/<int:artwork_id>', methods=['GET', 'DELETE'])
def handle_artwork_item(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)

    if request.method == 'GET':
        return jsonify(artwork_serializer(artwork))
    
    elif request.method == 'DELETE':
        db.session.delete(artwork)
        db.session.commit()
        return {"message": f"Artwork with id {artwork_id} has been deleted"}


# --- Shoes ---
@app.route('/shoes', methods=['GET', 'POST'])
def handle_shoes():
    if request.method == 'GET':
        shoes = Shoes.query.all()
        return jsonify([shoes_serializer(shoe) for shoe in shoes])
    
    elif request.method == 'POST':
        data = request.json
        new_shoe = Shoes(name=data['name'], size=data['size'], price=data['price'], image_url=data['image_url'])
        db.session.add(new_shoe)
        db.session.commit()
        return jsonify(shoes_serializer(new_shoe)), 201

@app.route('/shoes/<int:shoe_id>', methods=['GET', 'DELETE'])
def handle_shoe_item(shoe_id):
    shoe = Shoes.query.get_or_404(shoe_id)

    if request.method == 'GET':
        return jsonify(shoes_serializer(shoe))
    
    elif request.method == 'DELETE':
        db.session.delete(shoe)
        db.session.commit()
        return {"message": f"Shoe with id {shoe_id} has been deleted"}


# --- Electronics ---
@app.route('/electronics', methods=['GET', 'POST'])
def handle_electronics():
    if request.method == 'GET':
        electronics = Electronics.query.all()
        return jsonify([electronics_serializer(electronic) for electronic in electronics])
    
    elif request.method == 'POST':
        data = request.json
        new_electronic = Electronics(name=data['name'], description=data['description'], price=data['price'], image_url=data['image_url'])
        db.session.add(new_electronic)
        db.session.commit()
        return jsonify(electronics_serializer(new_electronic)), 201

@app.route('/electronics/<int:electronic_id>', methods=['GET', 'DELETE'])
def handle_electronic_item(electronic_id):
    electronic = Electronics.query.get_or_404(electronic_id)

    if request.method == 'GET':
        return jsonify(electronics_serializer(electronic))
    
    elif request.method == 'DELETE':
        db.session.delete(electronic)
        db.session.commit()
        return {"message": f"Electronic item with id {electronic_id} has been deleted"}


# --- Books ---
@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'GET':
        books = Book.query.all()
        return jsonify([book_serializer(book) for book in books])
    
    elif request.method == 'POST':
        data = request.json
        new_book = Book(title=data['title'], author=data['author'], price=data['price'], image_url=data['image_url'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_serializer(new_book)), 201

@app.route('/books/<int:book_id>', methods=['GET', 'DELETE'])
def handle_book_item(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'GET':
        return jsonify(book_serializer(book))
    
    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return {"message": f"Book with id {book_id} has been deleted"}


# --- Cart ---
@app.route('/cart', methods=['GET', 'POST'])
def handle_cart():
    if request.method == 'GET':
        carts = Cart.query.all()
        return jsonify([cart_serializer(cart) for cart in carts])
    
    elif request.method == 'POST':
        data = request.json
        new_cart = Cart(user_id=data['user_id'], total_price=data['total_price'])
        db.session.add(new_cart)
        db.session.commit()
        return jsonify(cart_serializer(new_cart)), 201

@app.route('/cart/<int:cart_id>', methods=['GET', 'DELETE'])
def handle_cart_item(cart_id):
    cart = Cart.query.get_or_404(cart_id)

    if request.method == 'GET':
        return jsonify(cart_serializer(cart))
    
    elif request.method == 'DELETE':
        db.session.delete(cart)
        db.session.commit()
        return {"message": f"Cart with id {cart_id} has been deleted"}


# --- Cart Items ---
@app.route('/cartitems', methods=['GET', 'POST'])
def handle_cartitems():
    if request.method == 'GET':
        items = CartItem.query.all()
        return jsonify([cartitem_serializer(item) for item in items])
    
    elif request.method == 'POST':
        data = request.json
        new_item = CartItem(cart_id=data['cart_id'], product_id=data['product_id'], quantity=data['quantity'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(cartitem_serializer(new_item)), 201

@app.route('/cartitems/<int:item_id>', methods=['GET', 'DELETE'])
def handle_cartitem_item(item_id):
    item = CartItem.query.get_or_404(item_id)

    if request.method == 'GET':
        return jsonify(cartitem_serializer(item))
    
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Cart item with id {item_id} has been deleted"}


# --- Serialization Helpers ---
def user_serializer(user):
    return {"id": user.id, "name": user.name, "email": user.email, "password": user.password}

def clothes_serializer(cloth):
    return {"id": cloth.id, "name": cloth.name, "description": cloth.description, "price": cloth.price, "image_url": cloth.image_url}

def whatsnew_serializer(item):
    return {"id": item.id, "title": item.title, "description": item.description, "image_url": item.image_url, "release_date": item.release_date}

def flashsale_serializer(sale):
    return {"id": sale.id, "name": sale.name, "discount": sale.discount, "start_time": sale.start_time, "end_time": sale.end_time}

def hotincategory_serializer(item):
    return {"id": item.id, "category": item.category, "product_id": item.product_id}

def artwork_serializer(art):
    return {"id": art.id, "title": art.title, "artist_name": art.artist_name, "image_url": art.image_url, "price": art.price}

def shoes_serializer(shoe):
    return {"id": shoe.id, "name": shoe.name, "size": shoe.size, "price": shoe.price, "image_url": shoe.image_url}

def electronics_serializer(electronic):
    return {"id": electronic.id, "name": electronic.name, "description": electronic.description, "price": electronic.price, "image_url": electronic.image_url}

def book_serializer(book):
    return {"id": book.id, "title": book.title, "author": book.author, "price": book.price, "image_url": book.image_url}

def cart_serializer(cart):
    return {"id": cart.id, "user_id": cart.user_id, "total_price": cart.total_price}

def cartitem_serializer(item):
    return {"id": item.id, "cart_id": item.cart_id, "product_id": item.product_id, "quantity": item.quantity}


if __name__ == '__main__':
    app.run(debug=True)
