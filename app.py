import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Простое кэширование в памяти
_cache = {
    'github_repos': None,
    'github_repos_timestamp': None,
    'local_projects': None,
    'local_projects_timestamp': None
}


def get_github_repos():
    """Получение всех публичных репозиториев с GitHub"""
    # Проверяем кэш
    if _cache['github_repos'] and _cache['github_repos_timestamp']:
        cache_age = datetime.now() - _cache['github_repos_timestamp']
        if cache_age < timedelta(seconds=app.config['CACHE_TIMEOUT']):
            return _cache['github_repos']
    
    repos = []
    username = app.config['GITHUB_USERNAME']
    token = app.config['GITHUB_TOKEN']
    
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        # Получаем все репозитории пользователя
        url = f"{app.config['GITHUB_API_URL']}/users/{username}/repos"
        params = {
            'type': 'public',
            'sort': 'updated',
            'per_page': 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        github_repos = response.json()
        
        for repo in github_repos:
            # Пропускаем форки, если хотите
            # if repo.get('fork'):
            #     continue
            
            # Определяем основной язык для тегов
            languages = []
            if repo.get('language'):
                languages.append(repo['language'].lower())
            
            # Получаем дополнительные языки (опционально, тратит дополнительные запросы)
            # Можно раскомментировать для получения всех языков
            # try:
            #     lang_url = repo['languages_url']
            #     lang_response = requests.get(lang_url, headers=headers, timeout=5)
            #     if lang_response.status_code == 200:
            #         repo_languages = lang_response.json()
            #         languages.extend([lang.lower() for lang in repo_languages.keys() if lang.lower() not in languages])
            # except:
            #     pass
            
            # Добавляем топики как теги
            topics = repo.get('topics', [])
            all_tags = list(set(languages + topics))
            
            project_data = {
                'id': repo['name'],
                'name': repo['name'].replace('-', ' ').replace('_', ' ').title(),
                'description': repo.get('description') or 'No description provided',
                'tags': all_tags[:10],  # Ограничиваем до 10 тегов
                'link': repo['html_url'],
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'language': repo.get('language'),
                'updated_at': repo.get('updated_at'),
                'created_at': repo.get('created_at'),
                'is_fork': repo.get('fork', False),
                'homepage': repo.get('homepage'),
                'source': 'github'
            }
            
            repos.append(project_data)
        
        # Кэшируем результат
        _cache['github_repos'] = repos
        _cache['github_repos_timestamp'] = datetime.now()
        
    except requests.RequestException as e:
        print(f"Ошибка при получении репозиториев GitHub: {e}")
        # Возвращаем кэш если есть, иначе пустой список
        if _cache['github_repos']:
            return _cache['github_repos']
        return []
    
    return repos


def load_local_projects():
    """Загрузка проектов из локальной папки projects (опционально)"""
    # Проверяем кэш
    if _cache['local_projects'] and _cache['local_projects_timestamp']:
        cache_age = datetime.now() - _cache['local_projects_timestamp']
        if cache_age < timedelta(seconds=app.config['CACHE_TIMEOUT']):
            return _cache['local_projects']
    
    projects = []
    projects_dir = Path(app.config['PROJECTS_DIR'])
    
    if not projects_dir.exists():
        return projects
    
    # Перебираем все подпапки в директории projects
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            info_file = project_dir / 'info.json'
            if info_file.exists():
                try:
                    with open(info_file, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                        project_data['id'] = project_dir.name
                        project_data['source'] = 'local'
                        # Добавляем поля для совместимости
                        if 'stars' not in project_data:
                            project_data['stars'] = 0
                        if 'forks' not in project_data:
                            project_data['forks'] = 0
                        projects.append(project_data)
                except json.JSONDecodeError as e:
                    print(f"Ошибка при чтении {info_file}: {e}")
                except Exception as e:
                    print(f"Неожиданная ошибка при обработке {info_file}: {e}")
    
    # Кэшируем результат
    _cache['local_projects'] = projects
    _cache['local_projects_timestamp'] = datetime.now()
    
    return projects


def get_all_projects():
    """Получение всех проектов: GitHub + локальные"""
    github_repos = get_github_repos()
    local_projects = load_local_projects()
    
    # Объединяем, приоритет у локальных (перезаписывают GitHub если есть дубликаты)
    all_projects = {repo['id']: repo for repo in github_repos}
    
    for project in local_projects:
        all_projects[project['id']] = project
    
    return list(all_projects.values())


def get_all_tags(projects):
    """Получение всех уникальных тегов из проектов"""
    tags = set()
    for project in projects:
        tags.update(project.get('tags', []))
    return sorted(tags)


def get_all_languages(projects):
    """Получение всех уникальных языков программирования"""
    languages = set()
    for project in projects:
        if project.get('language'):
            languages.add(project['language'])
    return sorted(languages)


@app.route('/')
def index():
    """Главная страница портфолио"""
    projects = get_all_projects()
    all_tags = get_all_tags(projects)
    all_languages = get_all_languages(projects)
    
    # Фильтрация по тегу
    selected_tag = request.args.get('tag')
    if selected_tag:
        projects = [p for p in projects if selected_tag in p.get('tags', [])]
    
    # Фильтрация по языку
    selected_language = request.args.get('language')
    if selected_language:
        projects = [p for p in projects if p.get('language') == selected_language]
    
    # Поиск
    search_query = request.args.get('search', '').lower()
    if search_query:
        projects = [
            p for p in projects
            if search_query in p.get('name', '').lower() or
               search_query in p.get('description', '').lower()
        ]
    
    # Сортировка
    sort_by = request.args.get('sort', 'updated')
    if sort_by == 'stars':
        projects = sorted(projects, key=lambda x: x.get('stars', 0), reverse=True)
    elif sort_by == 'name':
        projects = sorted(projects, key=lambda x: x.get('name', '').lower())
    elif sort_by == 'updated':
        projects = sorted(projects, key=lambda x: x.get('updated_at', ''), reverse=True)
    
    # Статистика
    total_stars = sum(p.get('stars', 0) for p in get_all_projects())
    total_forks = sum(p.get('forks', 0) for p in get_all_projects())
    
    return render_template(
        'index.html',
        projects=projects,
        all_tags=all_tags,
        all_languages=all_languages,
        selected_tag=selected_tag,
        selected_language=selected_language,
        search_query=search_query,
        sort_by=sort_by,
        author=app.config['AUTHOR_INFO'],
        total_stars=total_stars,
        total_forks=total_forks,
        total_projects=len(get_all_projects())
    )


@app.route('/api/projects')
def api_projects():
    """API endpoint для получения списка проектов"""
    projects = get_all_projects()
    return jsonify(projects)


@app.route('/api/refresh')
def api_refresh():
    """Принудительное обновление кэша"""
    global _cache
    _cache = {
        'github_repos': None,
        'github_repos_timestamp': None,
        'local_projects': None,
        'local_projects_timestamp': None
    }
    return jsonify({'status': 'ok', 'message': 'Cache cleared'})


@app.route('/generate-sitemap')
def generate_sitemap():
    """Генерация sitemap.xml"""
    projects = get_all_projects()
    base_url = app.config['SITE_URL']
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Главная страница
    sitemap_content += f'''  <url>
    <loc>{base_url}/</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>\n'''
    
    # Страницы с фильтрами по тегам
    all_tags = get_all_tags(projects)
    for tag in all_tags:
        sitemap_content += f'''  <url>
    <loc>{base_url}/?tag={tag}</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n'''
    
    sitemap_content += '</urlset>'
    
    # Сохраняем sitemap
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    return 'Sitemap успешно сгенерирован в файл sitemap.xml', 200


@app.route('/generate-readme')
def generate_readme():
    """Генерация README с описанием всех проектов"""
    projects = get_all_projects()
    
    readme_content = f"# {app.config['SITE_TITLE']}\n\n"
    readme_content += f"**Автор:** {app.config['AUTHOR_INFO']['name']}\n\n"
    readme_content += f"**Роль:** {app.config['AUTHOR_INFO']['role']}\n\n"
    readme_content += f"{app.config['AUTHOR_INFO']['description']}\n\n"
    
    # Контакты
    readme_content += "## 📞 Контакты\n\n"
    contacts = app.config['AUTHOR_INFO']['contacts']
    if contacts.get('github'):
        readme_content += f"- GitHub: [{contacts['github']}]({contacts['github']})\n"
    if contacts.get('email'):
        readme_content += f"- Email: {contacts['email']}\n"
    if contacts.get('telegram'):
        readme_content += f"- Telegram: {contacts['telegram']}\n"
    
    # Статистика
    total_stars = sum(p.get('stars', 0) for p in projects)
    total_forks = sum(p.get('forks', 0) for p in projects)
    
    readme_content += f"\n## 📊 Статистика\n\n"
    readme_content += f"- **Всего проектов:** {len(projects)}\n"
    readme_content += f"- **Звезд на GitHub:** ⭐ {total_stars}\n"
    readme_content += f"- **Форков:** 🔱 {total_forks}\n"
    
    readme_content += f"\n## 📁 Проекты ({len(projects)})\n\n"
    
    # Группируем проекты по языкам
    projects_by_lang = {}
    for p in projects:
        lang = p.get('language', 'Other')
        if lang not in projects_by_lang:
            projects_by_lang[lang] = []
        projects_by_lang[lang].append(p)
    
    # Список проектов по языкам
    for lang, lang_projects in sorted(projects_by_lang.items()):
        readme_content += f"### {lang} ({len(lang_projects)})\n\n"
        
        for project in sorted(lang_projects, key=lambda x: x.get('stars', 0), reverse=True):
            readme_content += f"#### {project.get('name', 'Без названия')}\n\n"
            readme_content += f"{project.get('description', 'Нет описания')}\n\n"
            
            if project.get('stars', 0) > 0 or project.get('forks', 0) > 0:
                readme_content += f"⭐ {project.get('stars', 0)} | 🔱 {project.get('forks', 0)}\n\n"
            
            if project.get('tags'):
                tags_str = ' '.join([f"`{tag}`" for tag in project['tags'][:8]])
                readme_content += f"**Теги:** {tags_str}\n\n"
            
            if project.get('link'):
                readme_content += f"**Ссылка:** [{project['link']}]({project['link']})\n\n"
            
            readme_content += "---\n\n"
    
    # Сохраняем README
    with open('PROJECTS_OVERVIEW.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return 'README успешно сгенерирован в файл PROJECTS_OVERVIEW.md', 200


if __name__ == '__main__':
    # Поддержка переменной окружения PORT для деплоя на Render/Heroku
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
