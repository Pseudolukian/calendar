#!/usr/bin/env python3
"""
Отладочный сервер MkDocs для просмотра документации.
Запускает MkDocs development server с автоматической перезагрузкой.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_mkdocs_installed():
    """Проверяет, установлен ли MkDocs."""
    try:
        result = subprocess.run(
            ["python", "-c", "import mkdocs; print('MkDocs установлен')"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ MkDocs найден")
        return True
    except subprocess.CalledProcessError:
        print("❌ MkDocs не найден")
        return False

def generate_openapi():
    """Генерирует OpenAPI спецификацию."""
    try:
        print("📝 Генерация OpenAPI спецификации...")
        
        # Импортируем приложение FastAPI
        sys.path.insert(0, str(Path(__file__).parent))
        from main import app
        
        import json
        
        # Получаем OpenAPI схему
        openapi_schema = app.openapi()
        
        # Создаем директорию docs если её нет
        docs_dir = Path(__file__).parent / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Сохраняем схему в файл
        openapi_file = docs_dir / "openapi.json"
        with open(openapi_file, 'w', encoding='utf-8') as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        
        print(f"✅ OpenAPI схема сохранена: {openapi_file}")
        print(f"📊 Найдено {len(openapi_schema.get('paths', {}))} endpoints")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка генерации OpenAPI: {e}")
        return False

def start_mkdocs_server():
    """Запускает отладочный сервер MkDocs."""
    try:
        print("🚀 Запуск MkDocs development server...")
        print("📚 Документация будет доступна по адресу: http://localhost:8001")
        print("🔄 Автоматическая перезагрузка включена")
        print("⏹️  Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        # Запускаем MkDocs сервер
        subprocess.run([
            "python", "-m", "mkdocs", "serve", 
            "--dev-addr=0.0.0.0:8001",
            "--livereload"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️  Сервер остановлен пользователем")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска MkDocs: {e}")
    except FileNotFoundError:
        print("❌ MkDocs не найден. Установите: uv pip install mkdocs mkdocs-material neoteroi-mkdocs")

def main():
    """Основная функция запуска."""
    print("📖 Запуск отладочного сервера документации")
    print("=" * 50)
    
    # Проверяем рабочую директорию
    current_dir = Path.cwd()
    mkdocs_config = current_dir / "mkdocs.yml"
    
    if not mkdocs_config.exists():
        print(f"❌ Файл mkdocs.yml не найден в {current_dir}")
        print("💡 Убедитесь, что вы запускаете скрипт из корня проекта")
        sys.exit(1)
    
    print(f"✅ Конфигурация MkDocs найдена: {mkdocs_config}")
    
    # Проверяем установку MkDocs
    if not check_mkdocs_installed():
        print("💡 Установите MkDocs: uv pip install mkdocs mkdocs-material neoteroi-mkdocs")
        sys.exit(1)
    
    # Генерируем OpenAPI спецификацию
    if not generate_openapi():
        print("⚠️  Продолжаем без OpenAPI спецификации...")
    
    # Запускаем сервер
    start_mkdocs_server()

if __name__ == "__main__":
    main()
