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

    # Создаем формат строго под Scarlet
    scarlet_repo = {
        "Meta": {
            "Name": "Russian App Source",
            "Icon": "https://raw.githubusercontent.com/youdontknow1/RussianAppSource/main/icons/sber.png"
        },
        "Apps": {}
    }
    
    for app in apps:
        name = clean_value(app.get("name", "Сбербанк"))
        scarlet_repo["Apps"][name] = {
            "BundleID": clean_value(app.get("bundle_identifier", "ru.sberbank.sberbankonline")),
            "Version": clean_value(app.get("version", "15.7.0")),
            "Download": clean_value(app.get("download_url", "")),
            "Icon": clean_value(app.get("icon_url", "")),
            "Developer": "SberAppSource",
            "Description": clean_value(app.get("description", ""))
        }

    with open('scarlet.json', 'w', encoding='utf-8') as f:
        json.dump(scarlet_repo, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_repos()
