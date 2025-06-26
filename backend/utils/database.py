from models import db, Category, Product, User
import random

def populate_database():
    """Populate database with mock e-commerce data"""
    
    # Create categories
    categories = [
        {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
        {'name': 'Books', 'description': 'Books, novels, and educational materials'},
        {'name': 'Clothing', 'description': 'Fashion and apparel'},
        {'name': 'Shoes', 'description': 'Footwear for all occasions'},
        {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
        {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
        {'name': 'Beauty & Personal Care', 'description': 'Beauty products and personal care items'},
        {'name': 'Toys & Games', 'description': 'Toys, games, and entertainment'},
        {'name': 'Automotive', 'description': 'Car accessories and automotive parts'},
        {'name': 'Health & Wellness', 'description': 'Health and wellness products'}
    ]
    
    # Create category objects
    category_objects = {}
    for cat_data in categories:
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()  # Get ID
        category_objects[cat_data['name']] = category
    
    # Product data
    products_data = [
        # Electronics
        {'name': 'iPhone 15 Pro', 'description': 'Latest Apple smartphone with advanced camera system', 'price': 999.99, 'category': 'Electronics', 'brand': 'Apple', 'rating': 4.8, 'stock': 50, 'attributes': {'storage': '128GB', 'color': 'Space Black', 'screen_size': '6.1 inch'}},
        {'name': 'Samsung Galaxy S24', 'description': 'Premium Android smartphone with AI features', 'price': 849.99, 'category': 'Electronics', 'brand': 'Samsung', 'rating': 4.6, 'stock': 45, 'attributes': {'storage': '256GB', 'color': 'Titanium Gray', 'screen_size': '6.2 inch'}},
        {'name': 'MacBook Air M3', 'description': 'Lightweight laptop with Apple M3 chip', 'price': 1299.99, 'category': 'Electronics', 'brand': 'Apple', 'rating': 4.9, 'stock': 30, 'attributes': {'ram': '8GB', 'storage': '256GB SSD', 'screen_size': '13.6 inch'}},
        {'name': 'Dell XPS 13', 'description': 'Premium ultrabook with Intel Core i7', 'price': 1199.99, 'category': 'Electronics', 'brand': 'Dell', 'rating': 4.5, 'stock': 25, 'attributes': {'ram': '16GB', 'storage': '512GB SSD', 'screen_size': '13.4 inch'}},
        {'name': 'Sony WH-1000XM5', 'description': 'Wireless noise-canceling headphones', 'price': 399.99, 'category': 'Electronics', 'brand': 'Sony', 'rating': 4.7, 'stock': 100, 'attributes': {'type': 'Over-ear', 'battery_life': '30 hours', 'noise_canceling': True}},
        {'name': 'iPad Pro 12.9"', 'description': 'Professional tablet with M2 chip', 'price': 1099.99, 'category': 'Electronics', 'brand': 'Apple', 'rating': 4.8, 'stock': 35, 'attributes': {'storage': '128GB', 'screen_size': '12.9 inch', 'connectivity': 'Wi-Fi'}},
        {'name': 'AirPods Pro 2nd Gen', 'description': 'Premium wireless earbuds with adaptive audio', 'price': 249.99, 'category': 'Electronics', 'brand': 'Apple', 'rating': 4.6, 'stock': 80, 'attributes': {'type': 'In-ear', 'battery_life': '6 hours', 'noise_canceling': True}},
        {'name': 'Samsung 55" QLED TV', 'description': '4K Smart TV with Quantum Dot technology', 'price': 899.99, 'category': 'Electronics', 'brand': 'Samsung', 'rating': 4.4, 'stock': 20, 'attributes': {'screen_size': '55 inch', 'resolution': '4K', 'smart_tv': True}},
        {'name': 'Canon EOS R6 Mark II', 'description': 'Full-frame mirrorless camera', 'price': 2499.99, 'category': 'Electronics', 'brand': 'Canon', 'rating': 4.7, 'stock': 15, 'attributes': {'megapixels': '24.2MP', 'video_recording': '4K', 'lens_mount': 'RF'}},
        {'name': 'Nintendo Switch OLED', 'description': 'Portable gaming console with OLED screen', 'price': 349.99, 'category': 'Electronics', 'brand': 'Nintendo', 'rating': 4.5, 'stock': 60, 'attributes': {'screen_size': '7 inch', 'storage': '64GB', 'type': 'Handheld/Docked'}},
        
        # Books
        {'name': 'The Seven Husbands of Evelyn Hugo', 'description': 'A captivating novel by Taylor Jenkins Reid', 'price': 16.99, 'category': 'Books', 'brand': 'Atria Books', 'rating': 4.8, 'stock': 200, 'attributes': {'genre': 'Fiction', 'pages': 400, 'language': 'English'}},
        {'name': 'Atomic Habits', 'description': 'An Easy & Proven Way to Build Good Habits & Break Bad Ones', 'price': 18.99, 'category': 'Books', 'brand': 'Avery', 'rating': 4.7, 'stock': 150, 'attributes': {'genre': 'Self-Help', 'pages': 320, 'author': 'James Clear'}},
        {'name': 'Project Hail Mary', 'description': 'A sci-fi thriller by Andy Weir', 'price': 19.99, 'category': 'Books', 'brand': 'Ballantine Books', 'rating': 4.6, 'stock': 180, 'attributes': {'genre': 'Science Fiction', 'pages': 496, 'author': 'Andy Weir'}},
        {'name': 'The Thursday Murder Club', 'description': 'A mystery novel by Richard Osman', 'price': 15.99, 'category': 'Books', 'brand': 'Pamela Dorman Books', 'rating': 4.3, 'stock': 120, 'attributes': {'genre': 'Mystery', 'pages': 368, 'author': 'Richard Osman'}},
        {'name': 'Educated', 'description': 'A memoir by Tara Westover', 'price': 17.99, 'category': 'Books', 'brand': 'Random House', 'rating': 4.5, 'stock': 100, 'attributes': {'genre': 'Memoir', 'pages': 334, 'author': 'Tara Westover'}},
        {'name': 'Python Crash Course', 'description': 'A hands-on introduction to programming', 'price': 39.99, 'category': 'Books', 'brand': 'No Starch Press', 'rating': 4.6, 'stock': 80, 'attributes': {'genre': 'Technology', 'pages': 544, 'author': 'Eric Matthes'}},
        {'name': 'The Midnight Library', 'description': 'A novel about infinite possibilities by Matt Haig', 'price': 14.99, 'category': 'Books', 'brand': 'Viking', 'rating': 4.2, 'stock': 160, 'attributes': {'genre': 'Fiction', 'pages': 288, 'author': 'Matt Haig'}},
        
        # Clothing
        {'name': 'Levi\'s 501 Original Jeans', 'description': 'Classic straight-leg denim jeans', 'price': 89.99, 'category': 'Clothing', 'brand': 'Levi\'s', 'rating': 4.4, 'stock': 75, 'attributes': {'size': '32x32', 'color': 'Dark Blue', 'material': '100% Cotton'}},
        {'name': 'Nike Dri-FIT T-Shirt', 'description': 'Moisture-wicking athletic t-shirt', 'price': 29.99, 'category': 'Clothing', 'brand': 'Nike', 'rating': 4.3, 'stock': 120, 'attributes': {'size': 'Large', 'color': 'Black', 'material': 'Polyester'}},
        {'name': 'Patagonia Better Sweater', 'description': 'Recycled fleece pullover jacket', 'price': 119.99, 'category': 'Clothing', 'brand': 'Patagonia', 'rating': 4.6, 'stock': 60, 'attributes': {'size': 'Medium', 'color': 'Navy Blue', 'material': 'Recycled Polyester'}},
        {'name': 'Uniqlo Heattech Long Sleeve', 'description': 'Thermal base layer shirt', 'price': 19.99, 'category': 'Clothing', 'brand': 'Uniqlo', 'rating': 4.2, 'stock': 200, 'attributes': {'size': 'Large', 'color': 'White', 'material': 'Polyester Blend'}},
        {'name': 'Champion Hoodie', 'description': 'Classic pullover hoodie with logo', 'price': 49.99, 'category': 'Clothing', 'brand': 'Champion', 'rating': 4.1, 'stock': 90, 'attributes': {'size': 'X-Large', 'color': 'Gray', 'material': 'Cotton Blend'}},
        
        # Shoes
        {'name': 'Nike Air Max 270', 'description': 'Lifestyle sneakers with Air Max cushioning', 'price': 149.99, 'category': 'Shoes', 'brand': 'Nike', 'rating': 4.5, 'stock': 80, 'attributes': {'size': '10', 'color': 'White/Black', 'type': 'Sneakers'}},
        {'name': 'Adidas Ultraboost 22', 'description': 'Premium running shoes with Boost technology', 'price': 189.99, 'category': 'Shoes', 'brand': 'Adidas', 'rating': 4.6, 'stock': 65, 'attributes': {'size': '9.5', 'color': 'Black', 'type': 'Running'}},
        {'name': 'Converse Chuck Taylor All Star', 'description': 'Classic canvas high-top sneakers', 'price': 59.99, 'category': 'Shoes', 'brand': 'Converse', 'rating': 4.3, 'stock': 150, 'attributes': {'size': '8', 'color': 'Red', 'type': 'Casual'}},
        {'name': 'Dr. Martens 1460 Boots', 'description': 'Iconic leather combat boots', 'price': 169.99, 'category': 'Shoes', 'brand': 'Dr. Martens', 'rating': 4.4, 'stock': 40, 'attributes': {'size': '9', 'color': 'Black', 'type': 'Boots'}},
        {'name': 'Allbirds Tree Runners', 'description': 'Sustainable running shoes made from eucalyptus', 'price': 98.99, 'category': 'Shoes', 'brand': 'Allbirds', 'rating': 4.2, 'stock': 70, 'attributes': {'size': '10.5', 'color': 'Gray', 'type': 'Running'}},
        
        # Home & Garden
        {'name': 'Instant Pot Duo 7-in-1', 'description': 'Multi-functional electric pressure cooker', 'price': 99.99, 'category': 'Home & Garden', 'brand': 'Instant Pot', 'rating': 4.7, 'stock': 50, 'attributes': {'capacity': '6 Qt', 'functions': '7', 'material': 'Stainless Steel'}},
        {'name': 'Dyson V15 Detect', 'description': 'Cordless stick vacuum with laser detection', 'price': 749.99, 'category': 'Home & Garden', 'brand': 'Dyson', 'rating': 4.5, 'stock': 25, 'attributes': {'type': 'Cordless', 'battery_life': '60 minutes', 'weight': '6.8 lbs'}},
        {'name': 'KitchenAid Stand Mixer', 'description': 'Professional-grade stand mixer', 'price': 449.99, 'category': 'Home & Garden', 'brand': 'KitchenAid', 'rating': 4.8, 'stock': 30, 'attributes': {'capacity': '5 Qt', 'color': 'Empire Red', 'attachments': 'Included'}},
        {'name': 'Weber Genesis II Gas Grill', 'description': '3-burner outdoor gas grill', 'price': 799.99, 'category': 'Home & Garden', 'brand': 'Weber', 'rating': 4.6, 'stock': 15, 'attributes': {'burners': '3', 'cooking_area': '513 sq in', 'fuel_type': 'Propane'}},
        
        # Sports & Outdoors
        {'name': 'Yeti Rambler Tumbler', 'description': 'Insulated stainless steel tumbler', 'price': 34.99, 'category': 'Sports & Outdoors', 'brand': 'Yeti', 'rating': 4.7, 'stock': 100, 'attributes': {'capacity': '20 oz', 'material': 'Stainless Steel', 'insulation': 'Double Wall'}},
        {'name': 'Patagonia Houdini Jacket', 'description': 'Ultra-lightweight windbreaker', 'price': 129.99, 'category': 'Sports & Outdoors', 'brand': 'Patagonia', 'rating': 4.4, 'stock': 45, 'attributes': {'size': 'Large', 'color': 'Blue', 'weight': '3.4 oz'}},
        {'name': 'REI Co-op Flexlite Chair', 'description': 'Lightweight packable camping chair', 'price': 59.99, 'category': 'Sports & Outdoors', 'brand': 'REI Co-op', 'rating': 4.3, 'stock': 80, 'attributes': {'weight': '1 lb 15 oz', 'capacity': '250 lbs', 'packed_size': '14x5x5 in'}},
        {'name': 'Hydro Flask Water Bottle', 'description': 'Insulated stainless steel water bottle', 'price': 44.99, 'category': 'Sports & Outdoors', 'brand': 'Hydro Flask', 'rating': 4.6, 'stock': 120, 'attributes': {'capacity': '32 oz', 'color': 'Mint', 'insulation': 'TempShield'}},
        
        # Beauty & Personal Care
        {'name': 'CeraVe Moisturizing Cream', 'description': 'Daily facial moisturizer for dry skin', 'price': 16.99, 'category': 'Beauty & Personal Care', 'brand': 'CeraVe', 'rating': 4.5, 'stock': 200, 'attributes': {'size': '16 oz', 'skin_type': 'Dry', 'spf': 'None'}},
        {'name': 'The Ordinary Niacinamide 10%', 'description': 'Zinc serum for blemish-prone skin', 'price': 7.99, 'category': 'Beauty & Personal Care', 'brand': 'The Ordinary', 'rating': 4.3, 'stock': 300, 'attributes': {'size': '30ml', 'active_ingredient': 'Niacinamide', 'skin_concern': 'Blemishes'}},
        {'name': 'Fenty Beauty Gloss Bomb', 'description': 'Universal lip luminizer', 'price': 19.99, 'category': 'Beauty & Personal Care', 'brand': 'Fenty Beauty', 'rating': 4.4, 'stock': 150, 'attributes': {'shade': 'Fenty Glow', 'finish': 'Glossy', 'size': '9ml'}},
        
        # Toys & Games
        {'name': 'LEGO Creator 3-in-1 Deep Sea Creatures', 'description': 'Build a shark, squid, or angler fish', 'price': 79.99, 'category': 'Toys & Games', 'brand': 'LEGO', 'rating': 4.6, 'stock': 60, 'attributes': {'pieces': '230', 'age_range': '7-12', 'theme': 'Creator'}},
        {'name': 'Monopoly Classic Board Game', 'description': 'The classic property trading game', 'price': 19.99, 'category': 'Toys & Games', 'brand': 'Hasbro', 'rating': 4.2, 'stock': 100, 'attributes': {'players': '2-8', 'age_range': '8+', 'game_time': '60-180 min'}},
        {'name': 'Nintendo Joy-Con Controllers', 'description': 'Wireless controllers for Nintendo Switch', 'price': 79.99, 'category': 'Toys & Games', 'brand': 'Nintendo', 'rating': 4.1, 'stock': 75, 'attributes': {'color': 'Neon Red/Blue', 'wireless': True, 'motion_controls': True}},
        
        # Automotive
        {'name': 'Garmin DriveSmart 65', 'description': 'GPS navigator with voice-activated navigation', 'price': 199.99, 'category': 'Automotive', 'brand': 'Garmin', 'rating': 4.3, 'stock': 40, 'attributes': {'screen_size': '6.95 inch', 'maps': 'North America', 'voice_control': True}},
        {'name': 'Chemical Guys Car Wash Kit', 'description': 'Complete car cleaning and detailing kit', 'price': 89.99, 'category': 'Automotive', 'brand': 'Chemical Guys', 'rating': 4.5, 'stock': 35, 'attributes': {'items': '11 piece kit', 'includes': 'Soap, wax, microfiber', 'size': 'Complete kit'}},
        
        # Health & Wellness
        {'name': 'Fitbit Charge 6', 'description': 'Advanced fitness and health tracker', 'price': 199.99, 'category': 'Health & Wellness', 'brand': 'Fitbit', 'rating': 4.4, 'stock': 85, 'attributes': {'battery_life': '7 days', 'gps': True, 'heart_rate': True}},
        {'name': 'Theragun Prime', 'description': 'Percussive therapy massage device', 'price': 299.99, 'category': 'Health & Wellness', 'brand': 'Therabody', 'rating': 4.6, 'stock': 30, 'attributes': {'battery_life': '120 minutes', 'speed_levels': '5', 'attachments': '4 included'}},
        {'name': 'Vitamix 5200 Blender', 'description': 'Professional-grade high-performance blender', 'price': 449.99, 'category': 'Health & Wellness', 'brand': 'Vitamix', 'rating': 4.7, 'stock': 25, 'attributes': {'capacity': '64 oz', 'motor': '2 HP', 'warranty': '7 years'}},
    ]
    
    # Add more products to reach 100+
    additional_products = []
    
    # Add variations of existing products
    colors = ['Black', 'White', 'Blue', 'Red', 'Gray', 'Green', 'Silver', 'Gold']
    sizes = ['Small', 'Medium', 'Large', 'X-Large', '8', '9', '10', '11', '12']
    
    base_electronics = [
        {'name': 'Wireless Bluetooth Speaker', 'description': 'Portable speaker with excellent sound quality', 'base_price': 79.99, 'brand': 'JBL', 'rating': 4.3},
        {'name': 'USB-C Charging Cable', 'description': 'Fast charging cable for modern devices', 'base_price': 19.99, 'brand': 'Anker', 'rating': 4.4},
        {'name': 'Wireless Charging Pad', 'description': 'Qi-compatible wireless charger', 'base_price': 34.99, 'brand': 'Belkin', 'rating': 4.2},
        {'name': 'Bluetooth Keyboard', 'description': 'Compact wireless keyboard for tablets', 'base_price': 69.99, 'brand': 'Logitech', 'rating': 4.1},
        {'name': 'Gaming Mouse', 'description': 'High-precision gaming mouse with RGB', 'base_price': 59.99, 'brand': 'Razer', 'rating': 4.5},
    ]
    
    for base_product in base_electronics:
        for i, color in enumerate(colors[:3]):
            variation = base_product.copy()
            variation['name'] = f"{base_product['name']} - {color}"
            variation['price'] = base_product['base_price'] + random.uniform(-10, 20)
            variation['category'] = 'Electronics'
            variation['stock'] = random.randint(20, 100)
            variation['attributes'] = {'color': color, 'model': f"Model {i+1}"}
            additional_products.append(variation)
    
    # Add more book variations
    genres = ['Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Biography', 'History', 'Cooking', 'Technology']
    authors = ['Jane Smith', 'John Doe', 'Sarah Johnson', 'Michael Brown', 'Emily Davis', 'David Wilson']
    
    for i, genre in enumerate(genres):
        book = {
            'name': f'Best of {genre} Collection',
            'description': f'A curated collection of the best {genre.lower()} books',
            'price': random.uniform(12.99, 29.99),
            'category': 'Books',
            'brand': 'Publishing House',
            'rating': random.uniform(3.8, 4.8),
            'stock': random.randint(50, 200),
            'attributes': {'genre': genre, 'author': random.choice(authors), 'pages': random.randint(200, 500)}
        }
        additional_products.append(book)
    
    # Add more clothing variations
    clothing_items = ['T-Shirt', 'Jeans', 'Sweater', 'Jacket', 'Shorts', 'Dress Shirt', 'Polo Shirt']
    brands = ['Gap', 'H&M', 'Zara', 'Old Navy', 'Banana Republic']
    
    for item in clothing_items:
        for brand in brands[:3]:
            for size in sizes[:4]:
                clothing = {
                    'name': f'{brand} {item}',
                    'description': f'Comfortable {item.lower()} perfect for everyday wear',
                    'price': random.uniform(19.99, 89.99),
                    'category': 'Clothing',
                    'brand': brand,
                    'rating': random.uniform(3.5, 4.5),
                    'stock': random.randint(30, 150),
                    'attributes': {'size': size, 'color': random.choice(colors), 'material': 'Cotton blend'}
                }
                additional_products.append(clothing)
    
    # Combine all products
    all_products = products_data + additional_products
    
    # Create product objects
    for product_data in all_products:
        category_name = product_data.pop('category')
        attributes = product_data.pop('attributes', {})
        
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            category_id=category_objects[category_name].id,
            brand=product_data.get('brand'),
            rating=product_data.get('rating', 4.0),
            stock_quantity=product_data.get('stock', 50),
            is_available=True,
            image_url=f"https://via.placeholder.com/300x300?text={product_data['name'].replace(' ', '+')}"
        )
        
        if attributes:
            product.set_attributes(attributes)
        
        db.session.add(product)
    
    # Create a demo admin user
    admin_user = User(
        username='admin',
        email='admin@ecommerce.com'
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # Create a demo regular user
    demo_user = User(
        username='demo_user',
        email='demo@example.com'
    )
    demo_user.set_password('demo123')
    db.session.add(demo_user)
    
    # Commit all changes
    db.session.commit()
    
    print(f"Database populated with:")
    print(f"- {len(categories)} categories")
    print(f"- {len(all_products)} products")
    print(f"- 2 demo users (admin/admin123, demo_user/demo123)")

def reset_database():
    """Reset database by dropping and recreating all tables"""
    db.drop_all()
    db.create_all()
    populate_database()
    print("Database reset and repopulated successfully!")

if __name__ == '__main__':
    # This can be run directly to populate the database
    from app import create_app
    app = create_app()
    with app.app_context():
        reset_database()
