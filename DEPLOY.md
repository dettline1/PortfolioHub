# 🚀 Руководство по деплою PortfolioHub

## 📋 Содержание

1. [Render.com (Рекомендуется)](#rendercom)
2. [Railway.app](#railwayapp)
3. [Heroku](#heroku)
4. [PythonAnywhere](#pythonanywhere)
5. [Vercel](#vercel)
6. [GitHub Pages (статический)](#github-pages)

---

## 1. Render.com (Рекомендуется) 🌟

**Преимущества:** Бесплатно, автоматический деплой, SSL сертификаты

### Шаги:

1. Зарегистрируйтесь на [render.com](https://render.com)

2. Создайте новый Web Service:
   - Dashboard → **New** → **Web Service**
   - Подключите GitHub репозиторий

3. Настройки:
   - **Name:** `my-portfolio` (ваше название)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

4. Переменные окружения (Environment):
   ```
   PYTHON_VERSION=3.11.0
   FLASK_ENV=production
   ```

5. Нажмите **Create Web Service**

6. Дождитесь деплоя (2-3 минуты)

7. Ваше портфолио доступно по адресу: `https://my-portfolio.onrender.com`

### Автообновление

Render автоматически обновляет сайт при каждом push в GitHub!

---

## 2. Railway.app

**Преимущества:** Простота, быстрый деплой, встроенная база данных

### Шаги:

1. Зарегистрируйтесь на [railway.app](https://railway.app)

2. Создайте новый проект:
   - **New Project** → **Deploy from GitHub repo**

3. Выберите репозиторий PortfolioHub

4. Railway автоматически определит Flask и создаст деплой

5. Переменные окружения:
   ```
   FLASK_ENV=production
   ```

6. Получите домен:
   - Settings → **Generate Domain**

7. Готово! Сайт доступен по адресу: `https://your-app.railway.app`

---

## 3. Heroku

**Преимущества:** Стабильность, масштабируемость

### Предварительные требования:

```bash
# Установите Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

### Шаги:

1. Логин:
```bash
heroku login
```

2. Создайте приложение:
```bash
heroku create my-portfolio-app
```

3. Добавьте buildpack:
```bash
heroku buildpacks:set heroku/python
```

4. Установите переменные:
```bash
heroku config:set FLASK_ENV=production
```

5. Деплой:
```bash
git push heroku main
```

6. Откройте приложение:
```bash
heroku open
```

### Автоматический деплой

1. Подключите GitHub в Heroku Dashboard
2. Enable Automatic Deploys
3. При каждом push в `main` будет автоматический деплой

---

## 4. PythonAnywhere

**Преимущества:** Бесплатный план навсегда, простота

### Шаги:

1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com)

2. Откройте консоль Bash

3. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/PortfolioHub.git
cd PortfolioHub
```

4. Создайте виртуальное окружение:
```bash
mkvirtualenv portfolio --python=/usr/bin/python3.10
pip install -r requirements.txt
```

5. Настройте Web App:
   - Web → **Add a new web app**
   - Framework: Flask
   - Python version: 3.10

6. WSGI Configuration (замените содержимое):
```python
import sys
import os

project_home = '/home/yourusername/PortfolioHub'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from app import app as application
```

7. Перезагрузите приложение:
   - Web → **Reload**

8. Ваш сайт: `https://yourusername.pythonanywhere.com`

---

## 5. Vercel

**Преимущества:** Очень быстрый деплой, глобальная CDN

### Дополнительная настройка:

Создайте `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Шаги:

1. Установите Vercel CLI:
```bash
npm i -g vercel
```

2. Деплой:
```bash
vercel
```

3. Следуйте инструкциям в терминале

4. Готово! Сайт доступен по сгенерированному URL

---

## 6. GitHub Pages (Статический экспорт)

Для статического сайта без серверной части.

### Шаги:

1. Установите Frozen-Flask:
```bash
pip install Frozen-Flask
```

2. Создайте `freeze.py`:
```python
from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
```

3. Сгенерируйте статические файлы:
```bash
python freeze.py
```

4. Переместите `build/` содержимое в корень

5. Создайте `.nojekyll` файл:
```bash
touch .nojekyll
```

6. Push в GitHub:
```bash
git add .
git commit -m "Deploy to GitHub Pages"
git push
```

7. В настройках репозитория:
   - Settings → Pages
   - Source: `main` branch, `/root`

8. Сайт будет доступен: `https://username.github.io/PortfolioHub`

**Примечание:** При этом методе поиск и фильтры работают только на клиенте через JS.

---

## 🔧 Настройка домена

### Render/Railway/Heroku:

1. Купите домен (Namecheap, Google Domains)

2. В настройках сервиса добавьте Custom Domain

3. Обновите DNS записи у регистратора:
   ```
   Type: CNAME
   Name: @
   Value: your-app.onrender.com
   ```

4. Дождитесь обновления DNS (до 48 часов)

---

## 📊 Мониторинг

### Render.com
- Dashboard → Logs (логи в реальном времени)
- Metrics (использование CPU, памяти)

### Railway
- Dashboard → Metrics
- Build & Deploy logs

### Heroku
```bash
heroku logs --tail
```

---

## 🐛 Устранение проблем

### Ошибка "Application Error"

1. Проверьте логи:
```bash
heroku logs --tail  # Heroku
```

2. Убедитесь, что `Procfile` существует:
```
web: python app.py
```

3. Проверьте `requirements.txt`

### Порт не определен

Убедитесь, что в `app.py`:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Статические файлы не загружаются

В `app.py` добавьте:
```python
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
```

---

## ✅ Чеклист перед деплоем

- [ ] Обновлена информация в `config.py`
- [ ] Добавлены все проекты в `/projects`
- [ ] Проверены все `info.json` файлы (валидный JSON)
- [ ] Создан `Procfile`
- [ ] Обновлен `requirements.txt`
- [ ] Установлена переменная `FLASK_ENV=production`
- [ ] Изменен `SECRET_KEY` в `config.py`
- [ ] Обновлен `SITE_URL` в `config.py`

---

## 🎉 Готово!

Ваше портфолио теперь онлайн! Поделитесь ссылкой с работодателями и коллегами.

**Нужна помощь?** Создайте Issue в GitHub репозитории.

