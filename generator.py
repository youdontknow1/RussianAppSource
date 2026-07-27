import os
import json
import yaml

def generate_repos():
    apps = []
    metadata_dir = 'metadata'
    
    if os.path.exists(metadata_dir):
        for filename in os.listdir(metadata_dir):
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                with open(os.path.join(metadata_dir, filename), 'r', encoding='utf-8') as f:
                    app_data = yaml.safe_load(f)
                    if app_data:
                        apps.append(app_data)

    # 1. Формат AltStore / SideStore (apps.json)
    altstore_repo = {
        "name": "Sber App Source",
        "subtitle": "Каталог Сбербанк",
        "apps": []
    }
    for app in apps:
        altstore_repo["apps"].append({
            "name": app.get("name"),
            "bundleIdentifier": app.get("bundle_identifier"),
            "developerName": "SberAppSource",
            "version": app.get("version"),
            "versionDate": app.get("version_date"),
            "downloadURL": app.get("download_url"),
            "iconURL": app.get("icon_url"),
            "subtitle": app.get("description"),
            "localizedDescription": app.get("description")
        })

    # 2. Формат Scarlet (scarlet.json)
    scarlet_repo = {
        "Meta": {
            "Name": "Sber App Source",
            "Icon": ""
        },
        "Apps": {}
    }
    for app in apps:
        scarlet_repo["Apps"][app.get("name")] = {
            "BundleID": app.get("bundle_identifier"),
            "Version": app.get("version"),
            "Download": app.get("download_url"),
            "Icon": app.get("icon_url"),
            "Developer": "SberAppSource",
            "Description": app.get("description")
        }

    # 3. Максимально подробный формат ESign (esign.json)
    esign_repo = {
        "name": "Sber App Source",
        "identifier": "com.sberappsource.repo",
        "description": "Магазин приложений Сбербанк для iOS",
        "apps": []
    }
    for app in apps:
        esign_repo["apps"].append({
            "name": str(app.get("name", "Unknown App")),
            "version": str(app.get("version", "1.0.0")),
            "bundle": str(app.get("bundle_identifier", "")),
            "down": str(app.get("download_url", "")),
            "icon": str(app.get("icon_url", "")),
            "desc": str(app.get("description", ""))
        })

    # Записываем готовые файлы в корень репозитория
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(altstore_repo, f, ensure_ascii=False, indent=4)
        
    with open('scarlet.json', 'w', encoding='utf-8') as f:
        json.dump(scarlet_repo, f, ensure_ascii=False, indent=4)
        
    with open('esign.json', 'w', encoding='utf-8') as f:
        json.dump(esign_repo, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_repos()
