from app import app
from models import db, MenuItem

# Local Paths for your images
img_zunka = "images/zunka_bhakar.png" 
img_thali = "images/rice_plate.jpg"
img_puri = "images/puri_bhaji.jpg"
img_palak_paneer = "images/palak_paneer.jpg"
img_masala_paneer = "images/masala_paneer.jpg"
img_mix_veg = "images/mix_veg.jpg"
img_dal = "images/dal_tadka.jpg"
img_roti = "images/chapati.jpg"
img_sweet = "images/puran_poli.jpg"
img_rice = "images/plain_rice.jpg"
img_fried_rice = "images/fried_rice.jpg"
img_drink = "images/mattha.jpg"
img_curd = "images/dahi.jpg"

with app.app_context():
    # Drop and recreate the database
    db.drop_all()
    db.create_all()
    
    print("Database tables created. Adding menu items...")

    sample_data = [
        # Specialty / Best Seller
        MenuItem(name="Zunka Bhakar (Best Seller)", category="Specialty", price=120, description="Authentic Maharashtrian Zunka served with 2 hot Bajra/Jowar Bhakris.", image_url=img_zunka),
        
        # Thalis / Plates
        MenuItem(name="Rice Plate", category="Thali", price=100, description="Simple and comforting daily meal with Rice, Dal, Sabzi, and 3 Chapatis.", image_url=img_thali),
        MenuItem(name="Puri Bhaji", category="Breakfast/Snacks", price=80, description="4 fluffy, deep-fried puris served with spicy, homestyle potato dry curry.", image_url=img_puri),
        
        # Main Course - Sabzi
        MenuItem(name="Palak Paneer", category="Main Course", price=160, description="Fresh paneer cubes simmered in a smooth, spiced spinach gravy.", image_url=img_palak_paneer),
        MenuItem(name="Masala Paneer", category="Main Course", price=170, description="Rich and spicy tomato-onion gravy loaded with soft paneer chunks.", image_url=img_masala_paneer),
        MenuItem(name="Sev Bhaji", category="Main Course", price=110, description="Spicy Maharashtrian curry topped with thick, crunchy besan sev.", image_url=img_masala_paneer),
        MenuItem(name="Mix Veg", category="Main Course", price=130, description="A healthy mix of fresh seasonal vegetables cooked in traditional spices.", image_url=img_mix_veg),
        MenuItem(name="Sev Tamatar", category="Main Course", price=120, description="Sweet, tangy, and spicy tomato curry topped with crispy sev.", image_url=img_masala_paneer),
        MenuItem(name="Baigan Bharta", category="Main Course", price=110, description="Fire-roasted eggplant mashed and cooked with onions, garlic, and fresh coriander.", image_url=img_zunka),
        
        # Dal
        MenuItem(name="Dal Tadka", category="Dal", price=110, description="Yellow lentils tempered with ghee, cumin, garlic, and dry red chilies.", image_url=img_dal),
        MenuItem(name="Dal Fry", category="Dal", price=90, description="Homestyle yellow dal cooked with onions and tomatoes.", image_url=img_dal),
        
        # Breads
        MenuItem(name="Chapati", category="Breads", price=15, description="Soft, round whole wheat flatbread made fresh.", image_url=img_roti),
        MenuItem(name="Paratha", category="Breads", price=25, description="Flaky, layered, and butter-roasted flatbread.", image_url=img_roti),
        MenuItem(name="Roti", category="Breads", price=12, description="Soft whole wheat phulka roasted on open flame.", image_url=img_roti),
        MenuItem(name="Puran Poli", category="Sweets & Breads", price=120, description="Traditional sweet flatbread stuffed with chana dal and jaggery, served with ghee.", image_url=img_sweet),
        
        # Rice
        MenuItem(name="Plain Rice", category="Rice", price=60, description="Steamed fluffy white basmati rice.", image_url=img_rice),
        MenuItem(name="Fried Rice", category="Rice", price=110, description="Indo-Chinese style rice tossed with veggies and soy sauce.", image_url=img_fried_rice),
        MenuItem(name="Namdev Rice", category="Rice", price=130, description="Special spicy Maharashtrian masala rice with a unique blend of spices.", image_url=img_fried_rice),
        
        # Beverages & Sides
        MenuItem(name="Mattha", category="Beverages", price=30, description="Spiced Maharashtrian buttermilk flavored with ginger, green chilies, and coriander.", image_url=img_drink),
        MenuItem(name="Tak (Buttermilk)", category="Beverages", price=25, description="Plain, cooling, and refreshing buttermilk.", image_url=img_drink),
        MenuItem(name="Soft Drinks", category="Beverages", price=40, description="Chilled refreshing aerated drinks.", image_url=img_drink),
        MenuItem(name="Dahi (Curd)", category="Sides", price=30, description="Fresh, thick, and creamy homemade curd.", image_url=img_curd)
    ]
    
    # Ye step ensure karega ki koi bhi image None na jaye
    for item in sample_data:
        if not item.image_url:
             item.image_url = "images/default_food.jpg" # Ek default naam de diya fallback ke liye

    db.session.add_all(sample_data)
    db.session.commit()
    print("✅ Database successfully setup with local images!")