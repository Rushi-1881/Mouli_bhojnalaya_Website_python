from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, MenuItem, Order
import urllib.parse

app = Flask(__name__)
app.secret_key = 'mauli_secret_key_123' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bhojnalaya.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- PUBLIC ROUTES ---

@app.route('/')
def home():
    featured_items = MenuItem.query.limit(3).all()
    return render_template('home.html', featured=featured_items)

@app.route('/menu')
def menu():
    menu_items = MenuItem.query.all()
    return render_template('menu.html', menu=menu_items)

@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
def add_to_cart(item_id):
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
    else:
        quantity = 1
        
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str] += quantity
    else:
        cart[item_id_str] = quantity
        
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    for item_id, quantity in cart.items():
        item = MenuItem.query.get(int(item_id))
        if item:
            item_total = item.price * quantity
            total_price += item_total
            cart_items.append({'item': item, 'quantity': quantity, 'total': item_total})
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('menu'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('menu'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        
        order_summary = ""
        total_price = 0
        for item_id, quantity in cart.items():
            item = MenuItem.query.get(int(item_id))
            if item:
                item_total = item.price * quantity
                total_price += item_total
                order_summary += f"{item.name} (x{quantity}) - ₹{item_total}\n"
        
        new_order = Order(
            customer_name=name, phone=phone, address=address, 
            total_amount=total_price, order_details=order_summary
        )
        db.session.add(new_order)
        db.session.commit()
        
        # Save order ID to user's session history
        if 'user_orders' not in session:
            session['user_orders'] = []
        session['user_orders'].append(new_order.id)
        session.modified = True
        
        whatsapp_number = "919356401434" 
        message = (
            f"🟢 *NEW PICKUP ORDER - Bhojnalaya Mauli* 🟢\n\n"
            f"*Order ID:* #{new_order.id}\n"
            f"*Customer:* {name}\n"
            f"*Phone:* {phone}\n"
            f"*Pickup Note:* {address}\n\n"
            f"*Order Details:*\n{order_summary}\n"
            f"*Total Bill:* ₹{total_price}\n"
            f"*Payment:* Pay at Store (Cash/UPI)\n\n"
            f"Please prepare my order!"
        )
        
        session.pop('cart', None)
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
        
        return render_template('success.html', whatsapp_url=whatsapp_url)

    return render_template('checkout.html')

# --- NEW: HISTORY & INVOICE ROUTES ---

@app.route('/history')
def order_history():
    order_ids = session.get('user_orders', [])
    if order_ids:
        # Fetch only the orders that belong to this user session
        orders = Order.query.filter(Order.id.in_(order_ids)).order_by(Order.order_date.desc()).all()
    else:
        orders = []
    return render_template('history.html', orders=orders)

@app.route('/invoice/<int:order_id>')
def view_invoice(order_id):
    # Ensure the user has permission to view this invoice
    if order_id not in session.get('user_orders', []):
        flash("You don't have permission to view this bill.", "danger")
        return redirect(url_for('home'))
        
    order = Order.query.get_or_404(order_id)
    return render_template('invoice.html', order=order)

# --- ADMIN ROUTES ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'mauli123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    orders = Order.query.order_by(Order.order_date.desc()).all()
    items = MenuItem.query.all()
    return render_template('admin_dashboard.html', orders=orders, items=items)

@app.route('/admin/add_item', methods=['POST'])
def add_item():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    new_item = MenuItem(
        name=request.form['name'], category=request.form['category'],
        price=request.form['price'], description=request.form['description'],
        image_url=request.form['image_url']
    )
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_item/<int:id>')
def delete_item(id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    item = MenuItem.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)