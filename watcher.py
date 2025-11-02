"""
Скрипт для автоматического обновления портфолио при добавлении новых проектов.
Использует watchdog для мониторинга изменений в папке projects.
"""

import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Исправление кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class ProjectWatcher(FileSystemEventHandler):
    """Обработчик событий файловой системы"""
    
    def __init__(self):
        self.last_event_time = 0
        self.debounce_seconds = 2  # Задержка для избежания дублирования событий
    
    def on_any_event(self, event):
        """Обработка любого события в папке projects"""
        current_time = time.time()
        
        # Игнорируем слишком частые события
        if current_time - self.last_event_time < self.debounce_seconds:
            return
        
        # Обрабатываем только изменения info.json файлов
        if event.is_directory or not event.src_path.endswith('info.json'):
            return
        
        self.last_event_time = current_time
        
        if event.event_type in ['created', 'modified', 'deleted']:
            print(f"\n[{time.strftime('%H:%M:%S')}] Обнаружено изменение: {event.event_type}")
            print(f"Файл: {event.src_path}")
            print("✓ Портфолио будет автоматически обновлено при следующем запросе\n")


def main():
    """Запуск мониторинга папки projects"""
    projects_dir = Path('projects')
    
    # Создаем папку projects если её нет
    if not projects_dir.exists():
        projects_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] Создана папка: {projects_dir.absolute()}")
    
    print("=" * 60)
    print("  PortfolioHub - Автоматический мониторинг проектов")
    print("=" * 60)
    print(f"\n[*] Отслеживание изменений в: {projects_dir.absolute()}")
    print("[*] Нажмите Ctrl+C для остановки\n")
    
    # Создаем наблюдателя
    event_handler = ProjectWatcher()
    observer = Observer()
    observer.schedule(event_handler, str(projects_dir), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[!] Остановка мониторинга...")
        observer.stop()
    
    observer.join()
    print("[+] Мониторинг остановлен")


if __name__ == "__main__":
    main()

