import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', True)
    
    # Database Configuration
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'financial.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # WhatsApp Bot Configuration
    WHATSAPP_ENABLED = os.getenv('WHATSAPP_ENABLED', 'true').lower() == 'true'
    
    # Financial Settings
    DEFAULT_CURRENCY = 'Rp'  # Indonesian Rupiah
    SAVINGS_ALLOCATION_PERCENTAGE = 20  # Default percentage of income to allocate to savings
    
    # API Configuration
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Security Configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # Categories for transactions
    EXPENSE_CATEGORIES = [
        'Housing',
        'Transportation',
        'Food',
        'Utilities',
        'Healthcare',
        'Entertainment',
        'Shopping',
        'Education',
        'Savings',
        'Other'
    ]

    INCOME_CATEGORIES = [
        'Salary',
        'Business',
        'Investment',
        'Freelance',
        'Other'
    ]

    @staticmethod
    def init_app(app):
        """Initialize application with config settings"""
        app.config.from_object(__class__)
