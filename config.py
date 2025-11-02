import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

class Config:
    """Конфигурация приложения"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    PROJECTS_DIR = 'projects'
    
    # GitHub API настройки
    GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME') or 'dettline1'
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  # Опционально, но увеличивает лимит
    GITHUB_API_URL = 'https://api.github.com'
    
    # Кэширование
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', 3600))  # 1 час по умолчанию
    
    # Информация об авторе
    AUTHOR_INFO = {
        'name': 'Daniil',
        'role': 'Python Developer',
        'description': 'Python-разработчик и создатель проектов, объединяющих технологии и креатив. Люблю простые идеи, реализованные со вкусом.',
        'contacts': {
            'github': 'https://github.com/dettline1',
            'email': 'shabanov.daniil.it@gmail.com',
            'telegram': '@madaodlb'
        }
    }
    
    # Настройки сайта
    SITE_URL = 'https://yourdomain.com'  # Измените на свой домен
    SITE_TITLE = 'Daniil Projects'

