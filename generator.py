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
        "name": "Russian App Source",
        "subtitle": "Каталог СНГ приложений",
        "apps": []
    }
    for app in apps:
        altstore_repo["apps"].append({
            "name": app.get("name"),
            "bundleIdentifier": app.get("bundle_identifier"),
            "developerName": "RussianAppSource",
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
            "Name": "Russian App Source",
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
            "Developer": "RussianAppSource",
            "Description": app.get("description")
        }

    # 3. УНИВЕРСАЛЬНЫЙ Формат ESign (esign.json)
    esign_repo = []
    for app in apps:
        esign_repo.append({
            "name": app.get("name"),
            "version": app.get("version"),
            "bundle": app.get("bundle_identifier"),
            "down": app.get("download_url"),
            "icon": app.get("icon_url"),
            "desc": app.get("description")
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
