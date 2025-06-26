import re
import random
from models import Product, Category, db
from sqlalchemy import and_, or_, func

class ChatbotProcessor:
    """Chatbot logic processor for handling user messages and generating responses"""
    
    def __init__(self):
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bhow are you\b',
                r'\bwhat\'s up\b'
            ],
            'product_search': [
                r'\b(show|find|search|look for|need|want|looking for)\b.*\b(product|item|thing)\b',
                r'\b(show me|find me|search for|look for)\b',
                r'\b(laptop|phone|book|shoe|watch|camera|tablet|headphone)\b',
                r'\bunder \$?\d+\b',
                r'\bless than \$?\d+\b',
                r'\bbetween \$?\d+ and \$?\d+\b'
            ],
            'price_filter': [
                r'\bunder \$?(\d+)\b',
                r'\bless than \$?(\d+)\b',
                r'\bbetween \$?(\d+) and \$?(\d+)\b',
                r'\bcheaper than \$?(\d+)\b',
                r'\bbudget.*\$?(\d+)\b'
            ],
            'category_filter': [
                r'\b(electronics|books|clothing|shoes|accessories|home|sports|beauty|toys)\b',
                r'\b(smartphone|laptop|tablet|camera|headphone|speaker)\b',
                r'\b(fiction|non-fiction|novel|textbook|cookbook)\b',
                r'\b(shirt|pant|dress|jacket|sneaker|boot|sandal)\b'
            ],
            'brand_filter': [
                r'\b(apple|samsung|google|microsoft|sony|nike|adidas|amazon)\b',
                r'\b(brand|make|manufacturer)\b'
            ],
            'recommendation': [
                r'\b(recommend|suggest|what should|best|top|popular|trending)\b',
                r'\b(what\'s good|what do you recommend|any suggestions)\b'
            ],
            'help': [
                r'\b(help|how|what can you do|what can I do|commands)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|thanks|thank you|that\'s all)\b'
            ]
        }
        
        self.category_mapping = {
            'electronics': ['laptop', 'phone', 'smartphone', 'tablet', 'camera', 'headphone', 'speaker', 'computer'],
            'books': ['book', 'novel', 'fiction', 'non-fiction', 'textbook', 'cookbook', 'biography'],
            'clothing': ['shirt', 'pant', 'dress', 'jacket', 'clothes', 'clothing'],
            'shoes': ['shoe', 'sneaker', 'boot', 'sandal', 'footwear'],
            'accessories': ['watch', 'jewelry', 'bag', 'wallet', 'accessory'],
            'home': ['furniture', 'kitchen', 'bedroom', 'living room', 'home'],
            'sports': ['sports', 'fitness', 'exercise', 'gym', 'outdoor'],
            'beauty': ['beauty', 'makeup', 'skincare', 'cosmetics'],
            'toys': ['toy', 'game', 'kids', 'children', 'baby']
        }
    
    def process_message(self, message, user_id):
        """Process user message and return appropriate response"""
        message_lower = message.lower()
        
        # Detect intent
        intent = self._detect_intent(message_lower)
        
        # Extract entities
        entities = self._extract_entities(message_lower)
        
        # Generate response based on intent
        if intent == 'greeting':
            response = self._handle_greeting()
        elif intent == 'product_search':
            response = self._handle_product_search(entities)
        elif intent == 'recommendation':
            response = self._handle_recommendation(entities)
        elif intent == 'help':
            response = self._handle_help()
        elif intent == 'goodbye':
            response = self._handle_goodbye()
        else:
            response = self._handle_general_search(message_lower)
        
        return {
            'response': response['text'],
            'intent': intent,
            'entities': entities,
            'products': response.get('products', [])
        }
    
    def _detect_intent(self, message):
        """Detect user intent from message"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return 'general'
    
    def _extract_entities(self, message):
        """Extract entities from user message"""
        entities = {}
        
        # Extract price range
        price_patterns = [
            (r'under \$?(\d+)', 'max_price'),
            (r'less than \$?(\d+)', 'max_price'),
            (r'cheaper than \$?(\d+)', 'max_price'),
            (r'budget.*\$?(\d+)', 'max_price'),
            (r'between \$?(\d+) and \$?(\d+)', 'price_range'),
            (r'from \$?(\d+) to \$?(\d+)', 'price_range')
        ]
        
        for pattern, entity_type in price_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                if entity_type == 'price_range':
                    entities['min_price'] = float(match.group(1))
                    entities['max_price'] = float(match.group(2))
                else:
                    entities[entity_type] = float(match.group(1))
                break
        
        # Extract category
        for category, keywords in self.category_mapping.items():
            for keyword in keywords:
                if re.search(r'\b' + keyword + r'\b', message, re.IGNORECASE):
                    entities['category'] = category
                    entities['search_term'] = keyword
                    break
            if 'category' in entities:
                break
        
        # Extract brand
        brand_pattern = r'\b(apple|samsung|google|microsoft|sony|nike|adidas|amazon|hp|dell|asus|lenovo)\b'
        brand_match = re.search(brand_pattern, message, re.IGNORECASE)
        if brand_match:
            entities['brand'] = brand_match.group(1).title()
        
        # Extract general search terms
        search_terms = []
        # Remove common words and extract meaningful terms
        common_words = {'i', 'need', 'want', 'looking', 'for', 'show', 'me', 'find', 'search', 'get', 'buy', 'purchase', 'a', 'an', 'the', 'some', 'any'}
        words = re.findall(r'\b\w+\b', message.lower())
        for word in words:
            if word not in common_words and len(word) > 2:
                if not re.match(r'^\d+$', word):  # Skip pure numbers
                    search_terms.append(word)
        
        if search_terms and 'search_term' not in entities:
            entities['search_terms'] = search_terms
        
        return entities
    
    def _handle_greeting(self):
        """Handle greeting messages"""
        greetings = [
            "Hello! Welcome to our e-commerce store. How can I help you find the perfect product today?",
            "Hi there! I'm here to help you discover amazing products. What are you looking for?",
            "Hey! Ready to find something awesome? Tell me what you need and I'll help you search our catalog.",
            "Good day! I'm your shopping assistant. What product can I help you find today?"
        ]
        return {'text': random.choice(greetings)}
    
    def _handle_help(self):
        """Handle help requests"""
        help_text = """I'm here to help you find products! Here's what I can do:

🔍 **Search for products**: Just tell me what you're looking for
   - "Show me laptops under $1000"
   - "I need running shoes"
   - "Find smartphones with good cameras"

💰 **Filter by price**: Set your budget
   - "Under $500"
   - "Between $100 and $300"

🏷️ **Filter by category or brand**: Be specific
   - "Apple products"
   - "Books by Stephen King"
   - "Nike shoes"

⭐ **Get recommendations**: Ask for suggestions
   - "What's popular?"
   - "Recommend something good"
   - "Show me top rated products"

Just ask me naturally, like you would ask a friend! What would you like to find?"""
        
        return {'text': help_text}
    
    def _handle_goodbye(self):
        """Handle goodbye messages"""
        goodbyes = [
            "Thank you for shopping with us! Have a great day! 🛍️",
            "Goodbye! Hope you found what you were looking for. Come back anytime! 👋",
            "Thanks for visiting! Feel free to ask if you need anything else. See you soon! 😊",
            "Have a wonderful day! Happy shopping! 🎉"
        ]
        return {'text': random.choice(goodbyes)}
    
    def _handle_product_search(self, entities):
        """Handle product search with entities"""
        # Build search query
        query = Product.query.filter(Product.is_available == True)
        
        search_info = []
        
        # Apply category filter
        if 'category' in entities:
            category = Category.query.filter(
                func.lower(Category.name).like(f"%{entities['category'].lower()}%")
            ).first()
            if category:
                query = query.filter(Product.category_id == category.id)
                search_info.append(f"category: {category.name}")
        
        # Apply price filters
        if 'max_price' in entities:
            query = query.filter(Product.price <= entities['max_price'])
            search_info.append(f"under ${entities['max_price']}")
        
        if 'min_price' in entities:
            query = query.filter(Product.price >= entities['min_price'])
            search_info.append(f"over ${entities['min_price']}")
        
        if 'min_price' in entities and 'max_price' in entities:
            search_info[-2:] = [f"${entities['min_price']} - ${entities['max_price']}"]
        
        # Apply brand filter
        if 'brand' in entities:
            query = query.filter(Product.brand.ilike(f"%{entities['brand']}%"))
            search_info.append(f"brand: {entities['brand']}")
        
        # Apply text search
        search_terms = []
        if 'search_term' in entities:
            search_terms.append(entities['search_term'])
        elif 'search_terms' in entities:
            search_terms.extend(entities['search_terms'])
        
        if search_terms:
            search_filter = or_(*[
                or_(
                    Product.name.ilike(f'%{term}%'),
                    Product.description.ilike(f'%{term}%')
                ) for term in search_terms
            ])
            query = query.filter(search_filter)
            search_info.append(f"matching: {', '.join(search_terms)}")
        
        # Execute query and get results
        products = query.order_by(Product.rating.desc(), Product.name).limit(10).all()
        
        # Generate response
        if products:
            product_list = [product.to_dict() for product in products]
            
            if search_info:
                search_description = " (" + ", ".join(search_info) + ")"
            else:
                search_description = ""
            
            response_text = f"Great! I found {len(products)} product{'s' if len(products) != 1 else ''} for you{search_description}:\n\n"
            
            for i, product in enumerate(products[:5], 1):  # Show top 5 in text
                response_text += f"{i}. **{product.name}** - ${product.price:.2f}\n"
                if product.brand:
                    response_text += f"   Brand: {product.brand}\n"
                response_text += f"   Rating: {'⭐' * int(product.rating)} ({product.rating}/5)\n"
                if product.description and len(product.description) > 0:
                    desc = product.description[:100] + "..." if len(product.description) > 100 else product.description
                    response_text += f"   {desc}\n"
                response_text += "\n"
            
            if len(products) > 5:
                response_text += f"...and {len(products) - 5} more products! Check the product list below."
            
            return {
                'text': response_text.strip(),
                'products': product_list
            }
        else:
            response_text = "I couldn't find any products matching your criteria"
            if search_info:
                response_text += f" ({', '.join(search_info)})"
            response_text += ". Try:\n\n"
            response_text += "• Adjusting your price range\n"
            response_text += "• Using different keywords\n"
            response_text += "• Browsing our categories\n"
            response_text += "• Asking for recommendations"
            
            return {'text': response_text}
    
    def _handle_recommendation(self, entities):
        """Handle recommendation requests"""
        # Get top-rated products
        query = Product.query.filter(Product.is_available == True)
        
        # Apply any filters from entities
        if 'category' in entities:
            category = Category.query.filter(
                func.lower(Category.name).like(f"%{entities['category'].lower()}%")
            ).first()
            if category:
                query = query.filter(Product.category_id == category.id)
        
        if 'max_price' in entities:
            query = query.filter(Product.price <= entities['max_price'])
        
        products = query.order_by(Product.rating.desc(), Product.name).limit(8).all()
        
        if products:
            product_list = [product.to_dict() for product in products]
            
            response_text = f"Here are my top recommendations for you:\n\n"
            
            for i, product in enumerate(products[:4], 1):  # Show top 4 in text
                response_text += f"{i}. **{product.name}** - ${product.price:.2f}\n"
                response_text += f"   {'⭐' * int(product.rating)} ({product.rating}/5) | {product.category.name if product.category else 'Product'}\n"
                if product.brand:
                    response_text += f"   Brand: {product.brand}\n"
                response_text += "\n"
            
            response_text += "These are highly rated by our customers! Need something more specific? Just ask! 😊"
            
            return {
                'text': response_text,
                'products': product_list
            }
        else:
            return {
                'text': "I'm sorry, I couldn't find any products to recommend at the moment. Please try searching for specific items!"
            }
    
    def _handle_general_search(self, message):
        """Handle general search when intent is unclear"""
        # Extract potential product terms
        words = re.findall(r'\b\w+\b', message.lower())
        search_terms = [word for word in words if len(word) > 2 and not re.match(r'^\d+$', word)]
        
        if search_terms:
            # Search products using extracted terms
            search_filter = or_(*[
                or_(
                    Product.name.ilike(f'%{term}%'),
                    Product.description.ilike(f'%{term}%'),
                    Product.brand.ilike(f'%{term}%')
                ) for term in search_terms
            ])
            
            products = Product.query.filter(
                and_(Product.is_available == True, search_filter)
            ).order_by(Product.rating.desc()).limit(8).all()
            
            if products:
                product_list = [product.to_dict() for product in products]
                
                response_text = f"I found some products that might interest you:\n\n"
                
                for i, product in enumerate(products[:3], 1):
                    response_text += f"{i}. **{product.name}** - ${product.price:.2f}\n"
                    response_text += f"   {'⭐' * int(product.rating)} ({product.rating}/5)\n\n"
                
                response_text += "Is this what you were looking for? You can also try:\n"
                response_text += "• Being more specific: 'Show me laptops under $800'\n"
                response_text += "• Asking for recommendations: 'What's popular?'\n"
                response_text += "• Getting help: 'What can you do?'"
                
                return {
                    'text': response_text,
                    'products': product_list
                }
        
        # Fallback response
        fallback_responses = [
            "I'm not sure I understand. Could you be more specific? For example, try 'Show me laptops' or 'I need shoes under $100'.",
            "I'd love to help! Try asking like: 'Find me smartphones' or 'Show products under $50' or 'What do you recommend?'",
            "Let me help you find what you need! You can search by saying things like 'Show me books' or 'I want electronics under $200'."
        ]
        
        return {'text': random.choice(fallback_responses)}
