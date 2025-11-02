# 🔌 API Документация PortfolioHub

## Обзор

PortfolioHub предоставляет простой REST API для доступа к данным проектов.

**Base URL:** `http://localhost:5000` (разработка) или ваш домен (продакшн)

---

## Endpoints

### 1. Получить все проекты

**GET** `/api/projects`

Возвращает список всех проектов в формате JSON.

#### Пример запроса:

```bash
curl http://localhost:5000/api/projects
```

#### Пример ответа:

```json
[
  {
    "id": "ai-notes-bot",
    "name": "AI Notes Bot",
    "description": "Телеграм-бот с искусственным интеллектом для создания конспектов",
    "tags": ["python", "aiogram", "openai", "telegram-bot", "ai"],
    "link": "https://github.com/yourusername/ai-notes-bot"
  },
  {
    "id": "web-scraper",
    "name": "Advanced Web Scraper",
    "description": "Мощный веб-скрапер с поддержкой JavaScript",
    "tags": ["python", "selenium", "beautifulsoup", "web-scraping"],
    "link": "https://github.com/yourusername/web-scraper"
  }
]
```

#### Коды ответов:

- `200 OK` - Успешный запрос
- `500 Internal Server Error` - Ошибка сервера

---

### 2. Генерация Sitemap

**GET** `/generate-sitemap`

Генерирует sitemap.xml файл для SEO.

#### Пример запроса:

```bash
curl http://localhost:5000/generate-sitemap
```

#### Ответ:

```
Sitemap успешно сгенерирован в файл sitemap.xml
```

---

### 3. Генерация README

**GET** `/generate-readme`

Генерирует PROJECTS_OVERVIEW.md с описанием всех проектов.

#### Пример запроса:

```bash
curl http://localhost:5000/generate-readme
```

#### Ответ:

```
README успешно сгенерирован в файл PROJECTS_OVERVIEW.md
```

---

## Использование API

### JavaScript (Fetch)

```javascript
// Получение всех проектов
fetch('http://localhost:5000/api/projects')
  .then(response => response.json())
  .then(projects => {
    console.log('Всего проектов:', projects.length);
    projects.forEach(project => {
      console.log(`${project.name}: ${project.description}`);
    });
  })
  .catch(error => console.error('Ошибка:', error));
```

### Python (requests)

```python
import requests

# Получение всех проектов
response = requests.get('http://localhost:5000/api/projects')
projects = response.json()

for project in projects:
    print(f"{project['name']}")
    print(f"  Описание: {project['description']}")
    print(f"  Теги: {', '.join(project['tags'])}")
    print(f"  Ссылка: {project['link']}")
    print()
```

### cURL

```bash
# Получение проектов
curl -X GET http://localhost:5000/api/projects

# Генерация sitemap
curl -X GET http://localhost:5000/generate-sitemap

# Генерация README
curl -X GET http://localhost:5000/generate-readme
```

---

## Фильтрация на клиенте

API возвращает все проекты. Фильтрацию можно реализовать на клиенте:

### Фильтр по тегу

```javascript
const filterByTag = (projects, tag) => {
  return projects.filter(project => 
    project.tags.includes(tag)
  );
};

// Пример использования
fetch('http://localhost:5000/api/projects')
  .then(response => response.json())
  .then(projects => {
    const pythonProjects = filterByTag(projects, 'python');
    console.log('Python проекты:', pythonProjects);
  });
```

### Поиск

```javascript
const searchProjects = (projects, query) => {
  const lowerQuery = query.toLowerCase();
  return projects.filter(project =>
    project.name.toLowerCase().includes(lowerQuery) ||
    project.description.toLowerCase().includes(lowerQuery)
  );
};

// Пример использования
fetch('http://localhost:5000/api/projects')
  .then(response => response.json())
  .then(projects => {
    const results = searchProjects(projects, 'bot');
    console.log('Результаты поиска:', results);
  });
```

---

## CORS

Для использования API с другого домена, добавьте поддержку CORS в `app.py`:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешить все домены
```

Или для конкретных доменов:

```python
CORS(app, resources={
    r"/api/*": {"origins": ["https://yourdomain.com"]}
})
```

Установите flask-cors:

```bash
pip install flask-cors
```

---

## Rate Limiting

Для защиты от злоупотреблений можно добавить ограничение запросов:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/projects')
@limiter.limit("10 per minute")
def api_projects():
    # ...
```

Установите flask-limiter:

```bash
pip install flask-limiter
```

---

## Примеры интеграции

### Виджет для сайта

```html
<!DOCTYPE html>
<html>
<head>
    <title>Мои проекты</title>
    <style>
        .project {
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .tag {
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            margin: 2px;
            display: inline-block;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div id="projects"></div>
    
    <script>
        fetch('http://localhost:5000/api/projects')
            .then(r => r.json())
            .then(projects => {
                const container = document.getElementById('projects');
                projects.forEach(p => {
                    const div = document.createElement('div');
                    div.className = 'project';
                    div.innerHTML = `
                        <h3>${p.name}</h3>
                        <p>${p.description}</p>
                        <div>
                            ${p.tags.map(t => `<span class="tag">${t}</span>`).join('')}
                        </div>
                        <a href="${p.link}" target="_blank">GitHub →</a>
                    `;
                    container.appendChild(div);
                });
            });
    </script>
</body>
</html>
```

### Telegram Bot

```python
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def projects(update: Update, context: CallbackContext):
    """Команда /projects для получения списка проектов"""
    response = requests.get('http://localhost:5000/api/projects')
    projects = response.json()
    
    message = f"📁 Всего проектов: {len(projects)}\n\n"
    
    for i, project in enumerate(projects[:5], 1):  # Первые 5
        message += f"{i}. {project['name']}\n"
        message += f"   {project['description']}\n"
        message += f"   🔗 {project['link']}\n\n"
    
    update.message.reply_text(message)

# Настройка бота
updater = Updater("YOUR_BOT_TOKEN")
updater.dispatcher.add_handler(CommandHandler("projects", projects))
updater.start_polling()
```

---

## Webhook уведомления

Для уведомления о добавлении нового проекта можно добавить webhook:

```python
import requests

@app.route('/api/webhook/project-added', methods=['POST'])
def webhook_project_added():
    """Webhook при добавлении проекта"""
    data = request.json
    
    # Отправка в Discord
    discord_webhook = "YOUR_DISCORD_WEBHOOK_URL"
    requests.post(discord_webhook, json={
        "content": f"Новый проект: {data['name']}"
    })
    
    return {"status": "ok"}, 200
```

---

## Кэширование

Для улучшения производительности можно добавить кэширование:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/projects')
@cache.cached(timeout=300)  # Кэш на 5 минут
def api_projects():
    projects = load_projects()
    return jsonify(projects)
```

---

## Поддержка

Если у вас есть вопросы или предложения по API, создайте Issue в GitHub!

**Документация актуальна на:** 2025-11-02

