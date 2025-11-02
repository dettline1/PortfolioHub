"""
Скрипт автоматической начальной настройки PortfolioHub
"""

import os
import sys
import json
from pathlib import Path
import subprocess

# Исправление кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def print_header(text):
    """Красивый заголовок"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(step, total, text):
    """Печать шага"""
    print(f"[{step}/{total}] {text}")


def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Требуется Python 3.7 или выше!")
        print(f"   Текущая версия: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")


def create_venv():
    """Создание виртуального окружения"""
    venv_path = Path('venv')
    
    if venv_path.exists():
        print("✅ Виртуальное окружение уже существует")
        return
    
    print("⏳ Создание виртуального окружения...")
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✅ Виртуальное окружение создано")
    except subprocess.CalledProcessError:
        print("❌ Ошибка при создании виртуального окружения")
        sys.exit(1)


def install_dependencies():
    """Установка зависимостей"""
    print("⏳ Установка зависимостей...")
    
    # Определяем путь к pip в виртуальном окружении
    if os.name == 'nt':  # Windows
        pip_path = Path('venv/Scripts/pip.exe')
    else:  # Linux/Mac
        pip_path = Path('venv/bin/pip')
    
    if not pip_path.exists():
        print("⚠️  Используем системный pip")
        pip_path = 'pip'
    
    try:
        subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Зависимости установлены")
    except subprocess.CalledProcessError as e:
        print("❌ Ошибка при установке зависимостей")
        print(e.stderr.decode())
        sys.exit(1)


def setup_config():
    """Настройка конфигурации"""
    print("\n📝 Настройка информации об авторе\n")
    
    config_path = Path('config.py')
    
    # Получаем данные от пользователя
    name = input("Ваше имя (Enter - пропустить): ").strip()
    role = input("Ваша роль (например: Python Developer): ").strip()
    description = input("Краткое описание о вас: ").strip()
    github = input("GitHub профиль (например: https://github.com/username): ").strip()
    email = input("Email: ").strip()
    telegram = input("Telegram (например: @username): ").strip()
    
    # Читаем текущий конфиг
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    # Обновляем значения
    if name:
        config_content = config_content.replace("'name': 'Ваше Имя'", f"'name': '{name}'")
    if role:
        config_content = config_content.replace("'role': 'Python Developer'", f"'role': '{role}'")
    if description:
        old_desc = 'Разработчик Python с опытом создания веб-приложений, ботов и автоматизации.'
        config_content = config_content.replace(f"'description': '{old_desc}'", 
                                               f"'description': '{description}'")
    if github:
        config_content = config_content.replace("'github': 'https://github.com/yourusername'", 
                                               f"'github': '{github}'")
    if email:
        config_content = config_content.replace("'email': 'your.email@example.com'", 
                                               f"'email': '{email}'")
    if telegram:
        config_content = config_content.replace("'telegram': '@yourusername'", 
                                               f"'telegram': '{telegram}'")
    
    # Сохраняем
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("\n✅ Конфигурация обновлена")


def create_example_project():
    """Создание примера проекта"""
    print("\n📁 Хотите создать пример проекта? (y/n): ", end='')
    choice = input().strip().lower()
    
    if choice not in ['y', 'yes', 'д', 'да']:
        return
    
    projects_dir = Path('projects')
    projects_dir.mkdir(exist_ok=True)
    
    example_dir = projects_dir / 'example-project'
    example_dir.mkdir(exist_ok=True)
    
    example_data = {
        "name": "Example Project",
        "description": "Это пример проекта. Замените на свой!",
        "tags": ["python", "example"],
        "link": "https://github.com/yourusername/example-project"
    }
    
    with open(example_dir / 'info.json', 'w', encoding='utf-8') as f:
        json.dump(example_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Пример проекта создан в projects/example-project/")


def validate_setup():
    """Проверка правильности установки"""
    print("\n🔍 Проверка установки...")
    
    errors = []
    
    # Проверяем папки
    if not Path('templates').exists():
        errors.append("Папка templates не найдена")
    if not Path('static').exists():
        errors.append("Папка static не найдена")
    if not Path('projects').exists():
        errors.append("Папка projects не найдена")
    
    # Проверяем файлы
    required_files = ['app.py', 'config.py', 'requirements.txt']
    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Файл {file} не найден")
    
    if errors:
        print("\n❌ Обнаружены ошибки:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ Все файлы на месте")
    return True


def print_next_steps():
    """Печать следующих шагов"""
    print_header("🎉 Установка завершена!")
    
    print("Следующие шаги:\n")
    
    print("1. Активируйте виртуальное окружение:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source venv/bin/activate")
    
    print("\n2. Запустите приложение:")
    print("   python app.py")
    
    print("\n3. Откройте браузер:")
    print("   http://localhost:5000")
    
    print("\n4. Добавьте свои проекты:")
    print("   python add_project.py")
    
    print("\n📚 Полезные файлы:")
    print("   • README.md - полная документация")
    print("   • QUICK_START.md - быстрый старт")
    print("   • FAQ.md - часто задаваемые вопросы")
    print("   • DEPLOY.md - руководство по деплою")
    
    print("\n💡 Советы:")
    print("   • Используйте run.bat (Windows) или run.sh (Linux/Mac) для быстрого запуска")
    print("   • Проверьте проекты: python validate_projects.py")
    print("   • Экспортируйте проекты: python export_projects.py")
    
    print("\n" + "=" * 70)
    print("Удачи с вашим портфолио! 🚀")
    print("=" * 70 + "\n")


def main():
    """Главная функция"""
    print_header("PortfolioHub - Автоматическая настройка")
    
    total_steps = 6
    
    # Шаг 1: Проверка Python
    print_step(1, total_steps, "Проверка версии Python")
    check_python_version()
    
    # Шаг 2: Создание виртуального окружения
    print_step(2, total_steps, "Создание виртуального окружения")
    create_venv()
    
    # Шаг 3: Установка зависимостей
    print_step(3, total_steps, "Установка зависимостей")
    install_dependencies()
    
    # Шаг 4: Настройка конфигурации
    print_step(4, total_steps, "Настройка конфигурации")
    setup_config()
    
    # Шаг 5: Создание примера проекта
    print_step(5, total_steps, "Создание примера проекта")
    create_example_project()
    
    # Шаг 6: Валидация
    print_step(6, total_steps, "Проверка установки")
    if not validate_setup():
        print("\n⚠️  Установка завершена с ошибками")
        sys.exit(1)
    
    # Финал
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Установка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)

