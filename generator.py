import os
import json
import yaml

def clean_value(val):
    if val is None:
        return ""
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

    # Задаем красивую иконку для самого репозитория по умолчанию
    default_icon = "https://raw.githubusercontent.com/youdontknow1/RussianAppSource/main/icons/sber.png"

    # 1. Сборка для Скарлет
    scarlet_repo = {
        "Meta": {
            "Name": "Russian App Source",
            "Icon": default_icon
        },
        "Apps": {}
    }
    
    # 2. Сборка для E-Sign
    esign_repo = {
        "name": "Russian App Source",
        "identifier": "com.sberappsource.repo",
        "description": "Магазин приложений для iOS",
        "apps": []
    }

    for app in apps:
        name = clean_value(app.get("name", "Сбербанк"))
        bundle = clean_value(app.get("bundle_identifier", "ru.sberbank.sberbankonline"))
        version = clean_value(app.get("version", "15.7.0"))
        down = clean_value(app.get("download_url", ""))
        
        # Если у приложения нет иконки, ставим дефолтную
        icon = clean_value(app.get("icon_url", ""))
        if not icon:
            icon = default_icon
            
        desc = clean_value(app.get("description", ""))

        # Пишем в Скарлет
        scarlet_repo["Apps"][name] = {
            "BundleID": bundle,
            "Version": version,
            "Download": down,
            "Icon": icon,
            "Developer": "SberAppSource",
            "Description": desc
        }

        # Пишем в E-Sign
        esign_repo["apps"].append({
            "name": name,
            "version": version,
            "bundle": bundle,
            "down": down,
            "icon": icon,
            "desc": desc
        })

    with open('scarlet.json', 'w', encoding='utf-8') as f:
        json.dump(scarlet_repo, f, ensure_ascii=False, indent=4)

    with open('esign.json', 'w', encoding='utf-8') as f:
        json.dump(esign_repo, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_repos()
