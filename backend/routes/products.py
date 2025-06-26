from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Product, Category, db
from sqlalchemy import and_, or_, func

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    """Get all products with optional filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        brand = request.args.get('brand')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'name')  # name, price, rating, created_at
        sort_order = request.args.get('sort_order', 'asc')  # asc, desc
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Build query
        query = Product.query.filter(Product.is_available == True)
        
        # Apply filters
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if brand:
            query = query.filter(Product.brand.ilike(f'%{brand}%'))
        
        if search:
            search_filter = or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%'),
                Product.brand.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Apply sorting
        if sort_by == 'price':
            sort_column = Product.price
        elif sort_by == 'rating':
            sort_column = Product.rating
        elif sort_by == 'created_at':
            sort_column = Product.created_at
        else:
            sort_column = Product.name
        
        if sort_order == 'desc':
            sort_column = sort_column.desc()
        
        query = query.order_by(sort_column)
        
        # Paginate results
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': products.page,
                'pages': products.pages,
                'per_page': products.per_page,
                'total': products.total,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            },
            'filters_applied': {
                'category_id': category_id,
                'min_price': min_price,
                'max_price': max_price,
                'brand': brand,
                'search': search,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get products', 'details': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product by ID"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        if not product.is_available:
            return jsonify({'error': 'Product is not available'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get product', 'details': str(e)}), 500

@products_bp.route('/search', methods=['GET'])
def search_products():
    """Search products with advanced filtering"""
    try:
        query_text = request.args.get('q', '').strip()
        
        if not query_text:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Get additional filters
        category_id = request.args.get('category_id', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        brand = request.args.get('brand')
        limit = request.args.get('limit', 20, type=int)
        
        # Limit results to prevent abuse
        limit = min(limit, 100)
        
        # Build search query
        search_filter = or_(
            Product.name.ilike(f'%{query_text}%'),
            Product.description.ilike(f'%{query_text}%'),
            Product.brand.ilike(f'%{query_text}%')
        )
        
        query = Product.query.filter(
            and_(
                Product.is_available == True,
                search_filter
            )
        )
        
        # Apply additional filters
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if brand:
            query = query.filter(Product.brand.ilike(f'%{brand}%'))
        
        # Order by relevance (name matches first, then description)
        products = query.order_by(
            func.case(
                [(Product.name.ilike(f'%{query_text}%'), 1)],
                else_=2
            ),
            Product.rating.desc(),
            Product.name
        ).limit(limit).all()
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'query': query_text,
            'results_count': len(products),
            'filters_applied': {
                'category_id': category_id,
                'min_price': min_price,
                'max_price': max_price,
                'brand': brand
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = Category.query.order_by(Category.name).all()
        
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get categories', 'details': str(e)}), 500

@products_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    """Get products by category"""
    try:
        category = Category.query.get(category_id)
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)
        
        # Get additional filters
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        brand = request.args.get('brand')
        
        # Build query
        query = Product.query.filter(
            and_(
                Product.category_id == category_id,
                Product.is_available == True
            )
        )
        
        # Apply filters
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if brand:
            query = query.filter(Product.brand.ilike(f'%{brand}%'))
        
        # Order by rating and name
        query = query.order_by(Product.rating.desc(), Product.name)
        
        # Paginate results
        products = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'category': category.to_dict(),
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': products.page,
                'pages': products.pages,
                'per_page': products.per_page,
                'total': products.total,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get category products', 'details': str(e)}), 500

@products_bp.route('/brands', methods=['GET'])
def get_brands():
    """Get all product brands"""
    try:
        # Get distinct brands from products
        brands = db.session.query(Product.brand).filter(
            and_(
                Product.brand.isnot(None),
                Product.brand != '',
                Product.is_available == True
            )
        ).distinct().order_by(Product.brand).all()
        
        brand_list = [brand[0] for brand in brands]
        
        return jsonify({
            'brands': brand_list,
            'count': len(brand_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get brands', 'details': str(e)}), 500

@products_bp.route('/price-range', methods=['GET'])
def get_price_range():
    """Get min and max price range for products"""
    try:
        price_range = db.session.query(
            func.min(Product.price).label('min_price'),
            func.max(Product.price).label('max_price')
        ).filter(Product.is_available == True).first()
        
        return jsonify({
            'min_price': float(price_range.min_price) if price_range.min_price else 0,
            'max_price': float(price_range.max_price) if price_range.max_price else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get price range', 'details': str(e)}), 500

@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    """Get featured products (highest rated)"""
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)
        
        products = Product.query.filter(
            Product.is_available == True
        ).order_by(
            Product.rating.desc(),
            Product.name
        ).limit(limit).all()
        
        return jsonify({
            'featured_products': [product.to_dict() for product in products],
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get featured products', 'details': str(e)}), 500

@products_bp.route('/recommendations/<int:product_id>', methods=['GET'])
def get_product_recommendations(product_id):
    """Get product recommendations based on category and price"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        limit = request.args.get('limit', 5, type=int)
        limit = min(limit, 20)
        
        # Get products from same category with similar price range
        price_range = product.price * 0.3  # 30% price range
        
        recommendations = Product.query.filter(
            and_(
                Product.id != product_id,
                Product.category_id == product.category_id,
                Product.price >= (product.price - price_range),
                Product.price <= (product.price + price_range),
                Product.is_available == True
            )
        ).order_by(
            Product.rating.desc(),
            Product.name
        ).limit(limit).all()
        
        # If not enough recommendations, get from same category
        if len(recommendations) < limit:
            additional = Product.query.filter(
                and_(
                    Product.id != product_id,
                    Product.category_id == product.category_id,
                    Product.is_available == True,
                    Product.id.notin_([r.id for r in recommendations])
                )
            ).order_by(
                Product.rating.desc()
            ).limit(limit - len(recommendations)).all()
            
            recommendations.extend(additional)
        
        return jsonify({
            'product_id': product_id,
            'recommendations': [rec.to_dict() for rec in recommendations],
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get recommendations', 'details': str(e)}), 500
