# E-commerce Sales Chatbot

A comprehensive e-commerce sales chatbot application with Python Flask backend and modern JavaScript frontend.

## Features

- 🤖 Interactive chatbot interface for product search and purchase
- 🔐 User authentication and session management
- 📱 Responsive design (desktop, tablet, mobile)
- 🛍️ Product catalog with search and filtering
- 💾 SQLite database with 100+ mock products
- 🔄 RESTful API for seamless frontend-backend communication
- 📊 Chat history and session tracking

## Technology Stack

### Backend

- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-JWT-Extended** - JWT token authentication
- **SQLite** - Database for development

### Frontend

- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Client-side logic
- **Responsive Design** - Mobile-first approach
- **Local Storage** - Session persistence

## Project Structure

```
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── routes/             # API routes
│   │   ├── auth.py         # Authentication routes
│   │   ├── products.py     # Product-related routes
│   │   └── chatbot.py      # Chatbot interaction routes
│   ├── utils/              # Utility functions
│   │   ├── database.py     # Database utilities
│   │   └── chatbot_logic.py # Chatbot processing logic
│   └── data/               # Mock data and database
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── css/
│   │   └── styles.css      # Main stylesheet
│   ├── js/
│   │   ├── app.js          # Main application logic
│   │   ├── chatbot.js      # Chatbot interface logic
│   │   └── auth.js         # Authentication logic
│   └── assets/             # Images and other assets
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**

   ```bash
   cd "Development of an E-commerce Sales"
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**

   ```bash
   cd backend
   python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open the application**
   - Backend API: `http://localhost:5000`
   - Frontend: Open `frontend/index.html` in your browser

## API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Products

- `GET /api/products` - Get all products with filtering
- `GET /api/products/<id>` - Get specific product
- `GET /api/products/search?q=<query>` - Search products

### Chatbot

- `POST /api/chatbot/message` - Send message to chatbot
- `GET /api/chatbot/history` - Get chat history

## Usage

1. **Registration/Login**: Create an account or login with existing credentials
2. **Product Search**: Use the chatbot to search for products by name, category, or description
3. **Product Filtering**: Apply filters by price range, category, or brand
4. **Product Details**: Click on products to view detailed information
5. **Chat History**: View previous conversations and interactions

## Sample Queries

- "Show me laptops under $1000"
- "I need a smartphone with good camera"
- "What books do you have by Stephen King?"
- "Show me running shoes in size 10"
- "I want to buy a coffee maker"

## Development

### Adding New Products

1. Edit `backend/utils/database.py`
2. Add product data to the `populate_products()` function
3. Reinitialize the database

### Customizing Chatbot Responses

1. Edit `backend/utils/chatbot_logic.py`
2. Modify the `process_message()` function
3. Add new intent recognition patterns

### Styling

1. Edit `frontend/css/styles.css`
2. Follow the existing mobile-first responsive design patterns

## Features in Detail

### Chatbot Capabilities

- Natural language product search
- Price range filtering
- Category-based recommendations
- Product comparison
- Purchase guidance
- Order status inquiries

### User Experience

- Intuitive chat interface
- Real-time message updates
- Session persistence
- Mobile-optimized design
- Fast product search and filtering

### Security

- Password hashing with bcrypt
- JWT token-based authentication
- CORS protection
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Support

For questions or issues, please refer to the documentation in the `docs/` directory or create an issue in the repository.
