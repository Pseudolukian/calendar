#!/usr/bin/env python3
"""
Скрипт для экспорта OpenAPI схемы в JSON файл
"""

import json
import os
from pathlib import Path

def export_openapi():
    """
    Экспортирует OpenAPI схему в отдельные JSON файлы по методам
    """
    try:
        # Импортируем приложение
        from main import app
        
        print("🔄 Генерация OpenAPI схемы...")
        
        # Получаем OpenAPI схему из приложения
        openapi_schema = app.openapi()
        
        # Создаем директории
        docs_dir = Path("docs")
        openapi_dir = docs_dir / "openapi"
        openapi_dir.mkdir(parents=True, exist_ok=True)
        
        # Базовая информация схемы
        base_schema = {
            "openapi": openapi_schema.get("openapi", "3.0.0"),
            "info": openapi_schema.get("info", {}),
            "servers": openapi_schema.get("servers", []),
            "components": openapi_schema.get("components", {})
        }
        
        paths = openapi_schema.get('paths', {})
        exported_files = []
        
        # Группируем endpoints по базовому пути
        endpoints_by_resource = {}
        
        for path, methods in paths.items():
            # Извлекаем имя ресурса из пути (например, "/api/Calendar" -> "calendar")
            resource_name = "unknown"
            
            if "/Calendar" in path:
                resource_name = "calendar"
            elif "/Events" in path:
                resource_name = "events"
            elif "/Event" in path:
                resource_name = "event"
            else:
                # Пытаемся извлечь из пути
                parts = [p for p in path.split('/') if p and p != 'api']
                if parts:
                    resource_name = parts[0].lower()
            
            if resource_name not in endpoints_by_resource:
                endpoints_by_resource[resource_name] = {}
            
            endpoints_by_resource[resource_name][path] = methods
        
        # Экспортируем каждый ресурс в отдельный файл
        for resource_name, resource_paths in endpoints_by_resource.items():
            # Создаем схему для конкретного ресурса
            resource_schema = base_schema.copy()
            resource_schema["paths"] = resource_paths
            
            # Имя файла
            output_file = openapi_dir / f"{resource_name}.json"
            
            # Сохраняем в файл
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(resource_schema, f, indent=2, ensure_ascii=False)
            
            file_size = output_file.stat().st_size
            endpoint_count = sum(len(methods) for methods in resource_paths.values())
            
            exported_files.append({
                "file": output_file,
                "resource": resource_name,
                "size": file_size,
                "endpoints": endpoint_count,
                "paths": list(resource_paths.keys())
            })
            
            print(f"✅ {resource_name.capitalize()}: {output_file.name} ({file_size} байт, {endpoint_count} методов)")
        
        # Создаем также полную схему
        full_output_file = docs_dir / "openapi.json"
        with open(full_output_file, "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        
        print("\n📊 Сводка экспорта:")
        print(f"🔖 Название API: {openapi_schema.get('info', {}).get('title', 'Неизвестно')}")
        print(f"🔢 Версия: {openapi_schema.get('info', {}).get('version', 'Неизвестно')}")
        print(f"� Директория: {openapi_dir.absolute()}")
        print(f"� Экспортировано файлов: {len(exported_files)}")
        print(f"📋 Полная схема: {full_output_file}")
        
        print("\n🎯 Детали по файлам:")
        for file_info in exported_files:
            print(f"   📄 {file_info['file'].name}")
            print(f"      🔗 Ресурс: {file_info['resource']}")
            print(f"      📊 Размер: {file_info['size']} байт ({file_info['size'] / 1024:.1f} KB)")
            print(f"      🛣️  Endpoints: {file_info['endpoints']}")
            for path in file_info['paths']:
                methods = list(openapi_schema['paths'][path].keys())
                methods_str = ', '.join(m.upper() for m in methods if m.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
                print(f"         {methods_str} {path}")
            print()
        
        print(f"🌐 Для использования в MkDocs:")
        for file_info in exported_files:
            print(f"   [OAD(./openapi/{file_info['file'].name})]")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что файл main.py существует и содержит объект app")
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")

def show_help():
    """
    Показывает справку по использованию
    """
    print("📚 OpenAPI Schema Exporter")
    print("=" * 50)
    print("Этот скрипт экспортирует OpenAPI схему вашего FastAPI приложения")
    print("в отдельные JSON файлы по ресурсам в директорию docs/openapi/.")
    print("")
    print("Использование:")
    print("  python openapi_export.py        - экспорт схемы")
    print("  python openapi_export.py --help - показать эту справку")
    print("")
    print("Структура выходных файлов:")
    print("  docs/")
    print("  ├── openapi.json          - полная схема")
    print("  └── openapi/")
    print("      ├── calendar.json     - endpoints Calendar")
    print("      ├── events.json       - endpoints Events")
    print("      └── event.json        - endpoints Event")
    print("")
    print("Каждый файл содержит:")
    print("• Базовую информацию об API (info, servers, components)")
    print("• Только endpoints относящиеся к конкретному ресурсу")
    print("• Полную схему данных для валидации")
    print("")
    print("Использование в MkDocs:")
    print("  [OAD(./openapi/calendar.json)]   - только Calendar endpoints")
    print("  [OAD(./openapi.json)]            - все endpoints")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        show_help()
    else:
        export_openapi()
