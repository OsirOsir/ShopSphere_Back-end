# ShopSphere Backend #
ShopSphere is an e-commerce platform that provides users with a seamless shopping experience, where they can browse items, search for products, manage their shopping cart, and access personalized user accounts. Admin users have additional access to manage the store's data. The app is built with React and leverages a backend API to manage user sessions, authentication, and product data.


*User Features*
Sign Up & Sign In: Allows users to create accounts and sign in securely.
Search Products: Users can search for items using keywords.
Shopping Cart: Add, view, and manage items in the cart.
Help & Support: Integrated help modal for user guidance.
Admin Features
User Roles: Admin access is role-based, granting special privileges to manage the store’s data.
Admin Panel: Accessible only by users with an admin role for store management.
Common Features
Modals: Help and Payment modals for user assistance and secure checkout.
Product Display: Dynamic product search and display based on user input.

# Setup & Installation #
npm install 

use this to intall the requirements                 
**pip install -r requirements.txt**
flask db init
flask db migrate
flask db upgrade

npm start
Node.js
npm run server

*Visit http://127.0.0.1:5555 to view ShopSphere in your browser.*
Project Structure
Login or Sign Up:

Navigate to the navbar’s "Sign In" button to log in. First-time users should sign up to access the platform.
Search Products:

Use the search bar to find products based on name or keywords.
Manage Cart:

Add products to your cart by clicking the "Add to Cart" button on product cards.
View cart contents by clicking the cart icon, where you can review items or proceed to checkout.
Help & Payment:

Access support via the "Help" button.
Use the "Cart" button to open the payment modal and review items before checkout.
Components
Key Components
Navbar: Contains search bar, sign-in, and cart management options.
SearchBar: Search functionality that dynamically filters products.
HelpModal: Provides general support information to users.
PaymentModal: Allows users to review and complete purchases.
ProductDisplay: Displays products based on search input or available inventory.
API Routes
User Authentication Example:

POST /api/login - Authenticate users.

Future Enhancements
Order History: Allow users to view their previous orders.
Product Categories: Implement product categorization for easier navigation.
Admin Management Panel: Allow admins to add or edit products directly from the app.
Wishlist: Enable users to save items to a wishlist for future purchases.

**Thankyou! everyone that contribute @CalebKiK @OsirOsir @Joeken10 @shalyne23 @Bmwash**
We welcome contributions to ShopSphere! To contribute
