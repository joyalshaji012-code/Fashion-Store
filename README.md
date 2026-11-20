# Fashion Store – E-commerce Platform

A full-stack e-commerce web application for fashion, built with Python and Django. Customers can browse and buy clothing, personalise designs to their taste, and pay online. Designers can submit their own designs for sale, and an admin manages the whole platform.

## Features

**Customer**
- Register, log in, and change or reset password (email OTP)
- Browse products by category
- Add products to the cart and place orders
- Customised design feature to personalise clothing
- Online payments with Razorpay
- Order history

**Designer (Worker)**
- Register and wait for admin verification
- Add, edit and manage their own products and designs
- Dashboard to manage designs

**Admin**
- Admin panel to manage products, users and activity
- Verify and manage designer registrations
- View orders and payments

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Payments:** Razorpay
- **Tools:** Git, GitHub, PyCharm

## How to Run This Project

1. **Clone the repository**
   ```
   git clone https://github.com/joyalshaji012-code/Fashion-Store.git
   cd Fashion-Store
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the requirements**
   ```
   pip install -r requirements.txt
   ```

4. **Set up MySQL**
   - Create a database in MySQL.
   - Open `Eshopping/settings.py` and set your database name, user and password.

5. **Add your Razorpay keys**
   - Replace the placeholder values with your own Razorpay test key and secret.

6. **Run the migrations**
   ```
   python manage.py migrate
   ```

7. **Create an admin user**
   ```
   python manage.py createsuperuser
   ```

8. **Start the server**
   ```
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000/ in your browser.

## Note

Passwords and API keys in this repository are placeholders. Add your own values in `settings.py` and the Razorpay code before running.

## Screenshots

*(Add screenshots of the home page, custom design feature and admin panel here.)*

## Author

**Joyal Shaji**
BCA Graduate | Java Full Stack Trainee
Kannur, Kerala
Email: joyalshaji012@gmail.com
LinkedIn: [linkedin.com/in/joyalshaji7](https://linkedin.com/in/joyalshaji7)
