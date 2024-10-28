# pip install flask-restful flask-swagger-ui

# import to flask app
from flask import Flask, jsonify, request
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# Swagger UI Configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path to your swagger.json file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ShopSphere API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Other app configurations...

# Swagger JSON endpoint
@app.route('/static/swagger.json', methods=['GET'])
def swagger_json():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "ShopSphere API",
            "version": "1.0.0",
            "description": "API documentation for the ShopSphere application."
        },
        "basePath": "/",
        "paths": {
            "/cart/add": {
                "post": {
                    "summary": "Add item to cart",
                    "description": "Adds an item to the user's cart.",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "user_id": {
                                        "type": "integer"
                                    },
                                    "item_id": {
                                        "type": "integer"
                                    },
                                    "quantity": {
                                        "type": "integer",
                                        "default": 1
                                    }
                                },
                                "required": ["user_id", "item_id"]
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Item added to cart",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Item not found",
                        }
                    }
                }
            },
            "/cart/{user_id}": {
                "get": {
                    "summary": "View user cart",
                    "description": "Retrieves the items in the user's cart.",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Cart retrieved successfully",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "item": {
                                                    "type": "string"
                                                },
                                                "quantity": {
                                                    "type": "integer"
                                                },
                                                "subtotal": {
                                                    "type": "number"
                                                }
                                            }
                                        }
                                    },
                                    "total": {
                                        "type": "number"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Cart is empty or not found"
                        }
                    }
                }
            },
            # Add other routes similarly...
        }
    })

# Continue with your existing routes...

if __name__ == '__main__':
    app.run(port=5555)

# swagger version
swagger: "2.0"

Step 4: Additional Endpoints
1. User Authentication Endpoints
Login (/login)

POST Method: Takes a JSON body containing username and password.
Responses:
200 OK: Successful authentication.
401 Unauthorized: Invalid credentials.
Logout (/logout)

POST Method: Logs the user out.
Responses:
200 OK: Successfully logged out.
Profile (/profile/{user_id})

GET Method: Retrieves user profile information.
Responses:
200 OK: User profile data.
404 Not Found: User does not exist.
2. Admin Product Management Endpoints
Add Product (/admin/products)

POST Method: Takes product details in the body.
Responses:
201 Created: Product successfully added.
400 Bad Request: Invalid input data.
Update Product (/admin/products/{product_id})

PUT Method: Updates product information.
Responses:
200 OK: Product successfully updated.
404 Not Found: Product does not exist.
Delete Product (/admin/products/{product_id})

DELETE Method: Removes a product from the catalog.
Responses:
204 No Content: Product successfully deleted.
404 Not Found: Product does not exist.
3. Item Category Display Endpoints
Clothes Category (/api/clothes)

GET Method: Retrieves a list of clothing items.
Responses:
200 OK: List of clothing items.
Shoes Category (/api/shoes)

GET Method: Retrieves a list of shoes.
Responses:
200 OK: List of shoes.
4. Search and Special Category Management
Search Items (/api/search)

GET Method: Takes a query parameter for search terms.
Responses:
200 OK: List of items matching the search criteria.
Special Categories (/api/special)

GET Method: Retrieves items from special categories.
Responses:
200 OK: List of items in special categories.