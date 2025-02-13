import json
import requests
from flask import Flask, Response

app = Flask(__name__)

config = None
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("[!] Failed to load config.json")

if config is None:
    print("[!] Failed to load config.json")

def fetch_manifest(addon_url):
    try:
        response = requests.get(f"{addon_url}/manifest.json")
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

def fetch_catalog(addon_url):
    try:
        manifest = fetch_manifest(addon_url)
        if not manifest:
            return None

        if 'tv' not in manifest.get('types', []):
            return None

        catalog_id = None
        for catalog in manifest.get('catalogs', []):
            if catalog.get('type') == 'tv':
                catalog_id = catalog.get('id')
                break

        if not catalog_id:
            return None

        catalog_url = f"{addon_url}/catalog/tv/{catalog_id}.json"
        response = requests.get(catalog_url)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

@app.route('/playlist.m3u8')
def get_playlist():
    if not config["addons"]:
        return Response("#EXTM3U\n", mimetype='application/vnd.apple.mpegurl')

    m3u8_content = "#EXTM3U\n"
    channels_added = set()

    for addon_url in config["addons"]:
        catalog = fetch_catalog(addon_url)
        if not catalog:
            continue

        for channel in catalog.get('metas', []):
            name = channel.get('name', '')
            if name in channels_added:
                continue

            logo = channel.get('logo', '')
            group = channel.get('genres', ['Live TV'])[0]

            streams = channel.get('streams', [])
            if streams:
                stream_url = streams[0].get('url', '')
                if stream_url:
                    m3u8_content += f'#EXTINF:-1 tvg-id="{channel["id"]}" tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{name}\n'
                    m3u8_content += f'{stream_url}\n'
                    channels_added.add(name)

    return Response(m3u8_content, mimetype='application/vnd.apple.mpegurl')

def main():        
    app.run(host=config["host"], port=config["port"])
