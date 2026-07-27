import os
import json
import yaml

def clean_value(val):
    if val is None:
        return ""
    # Вычищаем абсолютно любой мусор по кавычкам
    s = str(val).strip()
    for bad in ['&quot;', '"', "'"]:
        s = s.replace(bad, '')
    return s

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

    esign_repo = {
        "name": "Sber App Source",
        "identifier": "com.sberappsource.repo",
        "description": "Магазин приложений Сбербанк для iOS",
        "apps": []
    }
    
    for app in apps:
        esign_repo["apps"].append({
            "name": clean_value(app.get("name", "Сбербанк")),
            "version": clean_value(app.get("version", "15.7.0")),
            "bundle": clean_value(app.get("bundle_identifier", "ru.sberbank.sberbankonline")),
            "down": clean_value(app.get("download_url", "")),
            "icon": clean_value(app.get("icon_url", "")),
            "desc": clean_value(app.get("description", ""))
        })

    with open('esign.json', 'w', encoding='utf-8') as f:
        json.dump(esign_repo, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_repos()
