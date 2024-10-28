# ShopSphere Backend

**Deployment Link:** [ShopSphere Backend on Render](https://shopsphere-back-end.onrender.com)

## Overview
ShopSphere is an e-commerce platform designed to provide a seamless shopping experience. Users can browse items, search for products, manage their shopping cart, and access personalized accounts. Admin users have additional access to manage the store's data. This app is built with React on the frontend and a Flask-powered backend API to handle user sessions, authentication, and product data.

---

## Features

### User Features
- **Sign Up & Sign In**: Securely create accounts and log in.
- **Search Products**: Search items using keywords.
- **Shopping Cart**: Add, view, and manage items in the cart.
- **Help & Support**: Integrated help modal for user assistance.

### Admin Features
- **User Roles**: Role-based admin access with special privileges to manage store data.
- **Admin Panel**: Accessible only by users with an admin role for store management.

### Common Features
- **Modals**: Includes Help and Payment modals for user assistance and secure checkout.
- **Product Display**: Dynamic product search and display based on user input.

---

## Setup & Installation

1. **Clone the Repository**:
    ```bash
    git clone <repo-link>
    cd shopsphere-backend
    ```

2. **Install Backend Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up the Database**:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

4. **Run the Backend Server**:
    ```bash
    flask run
    ```

5. **Install Frontend Dependencies**:
    ```bash
    npm install
    ```

6. **Run the Frontend Server**:
    ```bash
    npm start
    ```

**Local Development URL:** [http://127.0.0.1:5555](http://127.0.0.1:5555)

---

## Project Structure

### Login or Sign Up:
- Access the "Sign In" button in the navbar to log in or sign up if you're a new user.

### Search Products:
- Use the search bar to find products by name or keywords.

### Manage Cart:
- Add items to your cart by clicking "Add to Cart" on the product cards.
- View and manage cart contents by clicking the cart icon, where you can proceed to checkout.

### Help & Payment:
- Access support via the "Help" button for general assistance.
- Open the payment modal via the "Cart" button to review items and complete the checkout process.

---

## Components

- **Navbar**: Contains search bar, sign-in, and cart options.
- **SearchBar**: Enables product search with real-time filtering.
- **HelpModal**: Provides support information.
- **PaymentModal**: Allows users to review cart items and complete purchases.
- **ProductDisplay**: Shows products based on search input and available inventory.

---

## API Routes

### User Authentication
- **POST /api/login** - Authenticate users.

---

## Future Enhancements

- **Order History**: View previous orders.
- **Product Categories**: Improve navigation with product categorization.
- **Admin Management Panel**: Allow admins to add/edit products directly.
- **Wishlist**: Enable users to save items for future purchases.

---

## Contributors
Thanks to everyone who contributed to ShopSphere! Special mentions to:
@CalebKiK, @OsirOsir, @Joeken10, @shalyne23, @Bmwash.

We welcome contributions! To get involved, please fork the repository and submit a pull request.

---

Thank you for your interest in ShopSphere!
