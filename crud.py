# pip install marshmallow
# routes.py
from flask import request, jsonify
from app import app, db
from models import Item
from marshmallow import Schema, fields, ValidationError

# Schema for input validation
class ItemSchema(Schema):
    item_name = fields.Str(required=True, error_messages={"required": "Item Name cannot be empty."})
    description = fields.Str(required=True, error_messages={"required": "Description cannot be empty."})
    price = fields.Float(required=True, error_messages={"required": "Price cannot be empty."})
    category = fields.Str(required=True, error_messages={"required": "Category cannot be empty."})
    items_available = fields.Int(required=True, error_messages={"required": "Items Available cannot be empty."})
    image_url = fields.Str(required=True, error_messages={"required": "Image URL cannot be empty."})

# Endpoint to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    try:
        # Load and validate the request data
        schema = ItemSchema()
        data = schema.load(request.json)

        # Create the new item
        new_item = Item(**data)
        db.session.add(new_item)
        db.session.commit()

        return jsonify(new_item.to_dict()), 201

    except ValidationError as err:
        return jsonify(err.messages), 400  # Return validation errors with a 400 response

# Convert Item to dictionary
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

# create item func
from flask import jsonify
from app import db
from models import Item

def create_item(item_data):
    try:
        # Extract data from the passed dictionary
        item_name = item_data.get('item_name')
        description = item_data.get('description')
        price = item_data.get('price')
        category = item_data.get('category')
        items_available = item_data.get('items_available')
        image_url = item_data.get('image_url')
        
        # Create a new Item instance
        new_item = Item(
            item_name=item_name,
            description=description,
            price=price,
            category=category,
            items_available=items_available,
            image_url=image_url
        )

        # Add and commit the new item to the database
        db.session.add(new_item)
        db.session.commit()

        return jsonify({'message': 'Item created successfully!', 'item_id': new_item.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# update item
def update_item(item_id, updated_data):
    try:
        # Find the item by its ID
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        # Update the item's fields
        item.item_name = updated_data.get('item_name', item.item_name)
        item.description = updated_data.get('description', item.description)
        item.price = updated_data.get('price', item.price)
        item.category = updated_data.get('category', item.category)
        item.items_available = updated_data.get('items_available', item.items_available)
        item.image_url = updated_data.get('image_url', item.image_url)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Item updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# delete item
def delete_item(item_id):
    try:
        # Find the item by its ID
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        # Delete the item from the database
        db.session.delete(item)
        db.session.commit()

        return jsonify({'message': 'Item deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
