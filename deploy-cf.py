import json, os, base64, urllib.request

with open('/tmp/cf_token2') as f:
    token = f.read().strip()

acc_id = '13dbd75f367f8c2cd1f5ab8edc36641e'
proj_dir = '/root/projects/com-viet'

files_map = {
    'index.html': 'index.html',
    'api/suggest.js': 'api/suggest.js',
    'manifest.json': 'manifest.json',
    'sw.js': 'sw.js',
    'icons/icon-72x72.png': 'icons/icon-72x72.png',
    'icons/icon-96x96.png': 'icons/icon-96x96.png',
    'icons/icon-128x128.png': 'icons/icon-128x128.png',
    'icons/icon-144x144.png': 'icons/icon-144x144.png',
    'icons/icon-152x152.png': 'icons/icon-152x152.png',
    'icons/icon-192x192.png': 'icons/icon-192x192.png',
    'icons/icon-384x384.png': 'icons/icon-384x384.png',
    'icons/icon-512x512.png': 'icons/icon-512x512.png',
    'icons/apple-touch-icon.png': 'icons/apple-touch-icon.png',
}

# Check which files actually exist
for dest, src_path in files_map.items():
    full_path = os.path.join(proj_dir, src_path)
    if not os.path.exists(full_path):
        print(f'MISSING: {src_path}')
    else:
        print(f'  OK: {src_path} ({os.path.getsize(full_path)} bytes)')

print('---')
manifest = {}
for dest, src_path in files_map.items():
    full_path = os.path.join(proj_dir, src_path)
    with open(full_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    manifest[dest] = b64

payload = json.dumps({'manifest': manifest, 'branch': 'main'}).encode()

req = urllib.request.Request(
    f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/pages/projects/com-bo-nau/deployments',
    data=payload,
    headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    },
    method='POST',
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode()
        r = json.loads(body)
        if r.get('success'):
            rs = r['result']
            print('✅ Deployed!')
            print('  URL:', rs.get('url'))
            print('  Aliases:', rs.get('aliases'))
            print('  Environment:', rs.get('environment'))
        else:
            for e in r.get('errors', []):
                print(f'Error {e["code"]}: {e["message"]}')
            print('Response:', json.dumps(r, indent=2)[:500])
except urllib.request.HTTPError as e:
    body = e.read().decode()
    print(f'HTTP Error {e.code}')
    print('Body:', body[:2000])
except Exception as e:
    import traceback
    print(f'Error: {e}')
    traceback.print_exc()