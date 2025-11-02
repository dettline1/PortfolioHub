"""
Скрипт для валидации всех info.json файлов в проектах
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

# Исправление кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def validate_project(info_file: Path) -> Tuple[bool, str]:
    """
    Валидация одного info.json файла
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверяем обязательные поля
        required_fields = ['name', 'description', 'tags', 'link']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return False, f"Отсутствуют поля: {', '.join(missing_fields)}"
        
        # Проверяем типы данных
        if not isinstance(data['name'], str) or not data['name'].strip():
            return False, "Поле 'name' должно быть непустой строкой"
        
        if not isinstance(data['description'], str) or not data['description'].strip():
            return False, "Поле 'description' должно быть непустой строкой"
        
        if not isinstance(data['tags'], list) or len(data['tags']) == 0:
            return False, "Поле 'tags' должно быть непустым списком"
        
        if not isinstance(data['link'], str):
            return False, "Поле 'link' должно быть строкой"
        
        # Проверяем длину описания
        if len(data['description']) < 10:
            return False, "Описание слишком короткое (минимум 10 символов)"
        
        if len(data['description']) > 500:
            return False, "Описание слишком длинное (максимум 500 символов)"
        
        return True, "OK"
        
    except json.JSONDecodeError as e:
        return False, f"Ошибка JSON: {e}"
    except Exception as e:
        return False, f"Ошибка: {e}"


def main():
    """Валидация всех проектов"""
    
    print("=" * 70)
    print("  Валидация проектов PortfolioHub")
    print("=" * 70)
    print()
    
    projects_dir = Path('projects')
    
    if not projects_dir.exists():
        print("❌ Папка 'projects' не найдена!")
        return
    
    # Находим все info.json файлы
    info_files = list(projects_dir.glob('*/info.json'))
    
    if not info_files:
        print("⚠️  Проекты не найдены!")
        print(f"   Добавьте проекты в папку: {projects_dir.absolute()}")
        return
    
    print(f"Найдено проектов: {len(info_files)}\n")
    
    # Валидация каждого проекта
    valid_count = 0
    invalid_count = 0
    
    for info_file in info_files:
        project_name = info_file.parent.name
        is_valid, message = validate_project(info_file)
        
        if is_valid:
            print(f"✅ {project_name}")
            print(f"   {info_file}")
            valid_count += 1
        else:
            print(f"❌ {project_name}")
            print(f"   {info_file}")
            print(f"   Ошибка: {message}")
            invalid_count += 1
        
        print()
    
    # Итоги
    print("=" * 70)
    print(f"Результаты валидации:")
    print(f"  ✅ Валидных проектов: {valid_count}")
    print(f"  ❌ Невалидных проектов: {invalid_count}")
    print(f"  📊 Всего: {len(info_files)}")
    print("=" * 70)
    
    if invalid_count > 0:
        print("\n⚠️  Исправьте ошибки в невалидных проектах!")
        exit(1)
    else:
        print("\n🎉 Все проекты валидны!")
        exit(0)


if __name__ == "__main__":
    main()

