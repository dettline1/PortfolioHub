"""
Интерактивный скрипт для быстрого добавления нового проекта в портфолио
"""

import os
import sys
import json
from pathlib import Path

# Исправление кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def create_project():
    """Создание нового проекта через интерактивный ввод"""
    
    print("=" * 60)
    print("  Добавление нового проекта в портфолио")
    print("=" * 60)
    print()
    
    # Получаем данные от пользователя
    print("Введите информацию о проекте:\n")
    
    # ID проекта (название папки)
    while True:
        project_id = input("ID проекта (латиница, дефисы): ").strip().lower()
        project_id = project_id.replace(' ', '-')
        
        if not project_id:
            print("❌ ID не может быть пустым!")
            continue
        
        # Проверяем, не существует ли уже такой проект
        project_path = Path('projects') / project_id
        if project_path.exists():
            print(f"❌ Проект с ID '{project_id}' уже существует!")
            continue
        
        break
    
    # Название проекта
    name = input("Название проекта: ").strip()
    if not name:
        name = project_id.replace('-', ' ').title()
    
    # Описание
    description = input("Описание проекта: ").strip()
    if not description:
        description = "Описание проекта"
    
    # Теги
    print("\nТеги (через запятую, например: python,flask,api):")
    tags_input = input("Теги: ").strip()
    tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
    
    if not tags:
        tags = ["python"]
    
    # Ссылка на GitHub
    link = input("\nСсылка на GitHub (оставьте пустым если нет): ").strip()
    if link and not link.startswith('http'):
        link = f"https://github.com/{link}"
    
    # Создаем данные проекта
    project_data = {
        "name": name,
        "description": description,
        "tags": tags,
        "link": link if link else f"https://github.com/yourusername/{project_id}"
    }
    
    # Создаем папку и файл
    try:
        project_path.mkdir(parents=True, exist_ok=True)
        
        info_file = project_path / 'info.json'
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("✅ Проект успешно добавлен!")
        print("=" * 60)
        print(f"\n📁 Папка: {project_path.absolute()}")
        print(f"📄 Файл: {info_file.absolute()}")
        print("\nДанные проекта:")
        print(json.dumps(project_data, ensure_ascii=False, indent=2))
        print("\n💡 Обновите страницу портфолио, чтобы увидеть новый проект!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при создании проекта: {e}")
        return False
    
    return True


def main():
    """Главная функция"""
    
    # Проверяем наличие папки projects
    projects_dir = Path('projects')
    if not projects_dir.exists():
        projects_dir.mkdir(parents=True, exist_ok=True)
    
    # Создаем проект
    success = create_project()
    
    # Предлагаем добавить еще один проект
    if success:
        print("\n" + "-" * 60)
        another = input("\nДобавить еще один проект? (y/n): ").strip().lower()
        if another in ['y', 'yes', 'д', 'да']:
            print()
            main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Отменено пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")

