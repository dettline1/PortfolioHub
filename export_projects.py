"""
Скрипт для экспорта всех проектов в различные форматы
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime

# Исправление кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_projects():
    """Загрузка всех проектов"""
    projects = []
    projects_dir = Path('projects')
    
    if not projects_dir.exists():
        return projects
    
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            info_file = project_dir / 'info.json'
            if info_file.exists():
                try:
                    with open(info_file, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                        project_data['id'] = project_dir.name
                        projects.append(project_data)
                except Exception as e:
                    print(f"Ошибка при чтении {info_file}: {e}")
    
    return projects


def export_to_json(projects, filename='projects_export.json'):
    """Экспорт в JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    print(f"✅ Экспортировано в {filename}")


def export_to_csv(projects, filename='projects_export.csv'):
    """Экспорт в CSV"""
    if not projects:
        print("⚠️  Нет проектов для экспорта")
        return
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        # Определяем поля
        fieldnames = ['id', 'name', 'description', 'tags', 'link']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for project in projects:
            # Преобразуем список тегов в строку
            row = project.copy()
            row['tags'] = ', '.join(project.get('tags', []))
            writer.writerow(row)
    
    print(f"✅ Экспортировано в {filename}")


def export_to_markdown(projects, filename='projects_export.md'):
    """Экспорт в Markdown"""
    content = f"# Экспорт проектов\n\n"
    content += f"*Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    content += f"**Всего проектов: {len(projects)}**\n\n"
    content += "---\n\n"
    
    for i, project in enumerate(projects, 1):
        content += f"## {i}. {project.get('name', 'Без названия')}\n\n"
        content += f"**ID:** `{project.get('id', 'N/A')}`\n\n"
        content += f"**Описание:** {project.get('description', 'Нет описания')}\n\n"
        
        if project.get('tags'):
            tags_str = ' '.join([f'`{tag}`' for tag in project['tags']])
            content += f"**Технологии:** {tags_str}\n\n"
        
        if project.get('link'):
            content += f"**Ссылка:** [{project['link']}]({project['link']})\n\n"
        
        content += "---\n\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Экспортировано в {filename}")


def export_to_html(projects, filename='projects_export.html'):
    """Экспорт в HTML таблицу"""
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Экспорт проектов</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: bold;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .tag {
            display: inline-block;
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9em;
        }
        a {
            color: #667eea;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>📁 Экспорт проектов</h1>
    <p><strong>Всего проектов:</strong> """ + str(len(projects)) + """</p>
    <p><em>Сгенерировано: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</em></p>
    
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Название</th>
                <th>Описание</th>
                <th>Технологии</th>
                <th>Ссылка</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for i, project in enumerate(projects, 1):
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in project.get('tags', [])])
        
        html += f"""            <tr>
                <td>{i}</td>
                <td><strong>{project.get('name', 'Без названия')}</strong></td>
                <td>{project.get('description', 'Нет описания')}</td>
                <td>{tags_html}</td>
                <td><a href="{project.get('link', '#')}" target="_blank">GitHub</a></td>
            </tr>
"""
    
    html += """        </tbody>
    </table>
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Экспортировано в {filename}")


def main():
    """Главная функция"""
    print("=" * 70)
    print("  Экспорт проектов PortfolioHub")
    print("=" * 70)
    print()
    
    projects = load_projects()
    
    if not projects:
        print("⚠️  Проекты не найдены!")
        print("   Добавьте проекты в папку /projects")
        return
    
    print(f"Найдено проектов: {len(projects)}\n")
    
    # Экспорт во все форматы
    print("Экспорт в различные форматы:\n")
    
    export_to_json(projects)
    export_to_csv(projects)
    export_to_markdown(projects)
    export_to_html(projects)
    
    print("\n" + "=" * 70)
    print("✅ Экспорт завершен!")
    print("=" * 70)
    
    print("\nСозданные файлы:")
    print("  • projects_export.json - JSON формат")
    print("  • projects_export.csv - CSV для Excel")
    print("  • projects_export.md - Markdown документ")
    print("  • projects_export.html - HTML таблица")


if __name__ == "__main__":
    main()

