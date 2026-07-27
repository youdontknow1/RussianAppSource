import os
import json
import yaml

def clean_value(val):
    if val is None:
        return ""
    # Убираем мусорные кодировки кавычек, если их подставил телефон
    return str(val).replace('&quot;', '').replace('"', '').strip()

def generate_repos():
    apps = []
    metadata_dir = 'metadata'
    
    if os.path.exists(metadata_dir):
        for filename in os.listdir(metadata_dir):
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                with open(os.path.join(metadata_dir, filename), 'r', encoding='utf-8') as f:
                    try:
                        app_data = yaml.safe_load(f)
                        if app_data:
                            apps.append(app_data)
                    except Exception as e:
                        print(f"Ошибка чтения файла {filename}: {e}")

    # Формат ESign (esign.json)
    esign_repo = {
        "name": "Russian App Source",
        "identifier": "com.russianappsource.repo",
        "description": "Магазин приложений для iOS",
        "apps": []
    }
    for app in apps:
        esign_repo["apps"].append({
            "name": clean_value(app.get("name", "Без названия")),
            "version": clean_value(app.get("version", "1.0.0")),
            "bundle": clean_value(app.get("bundle_identifier", "")),
            "down": clean_value(app.get("download_url", "")),
            "icon": clean_value(app.get("icon_url", "")),
            "desc": clean_value(app.get("description", ""))
        })

    with open('esign.json', 'w', encoding='utf-8') as f:
        json.dump(esign_repo, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_repos()
