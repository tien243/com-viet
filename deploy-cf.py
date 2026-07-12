import subprocess, json, os, base64

with open('/tmp/cf_token2') as f:
    token = f.read().strip()

hdr = 'Bearer ' + token
auth_hdr = 'Authorization: ' + hdr
headers = ['-H', auth_hdr, '-H', 'Content-Type: application/json']

acc_id = '13dbd75f367f8c2cd1f5ab8edc36641e'
proj_dir = '/root/projects/com-viet'

# Build manifest with base64-encoded file contents
manifest = {}
files_map = {
    'index.html': 'index.html',
    'api/suggest.js': 'api/suggest.js'
}

for dest, src_path in files_map.items():
    full_path = os.path.join(proj_dir, src_path)
    with open(full_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    manifest[dest] = b64

payload = json.dumps({
    'manifest': manifest,
    'branch': 'main'
})

result = subprocess.run(['curl', '-s', '-X', 'POST',
    f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/pages/projects/com-bo-nau/deployments',
    *headers, '-d', payload], capture_output=True, text=True, timeout=30)
resp = json.loads(result.stdout)

if resp.get('success'):
    r = resp['result']
    print('✅ Deployed!')
    print('  URL:', r.get('url'))
    print('  Aliases:', r.get('aliases'))
    print('  Environment:', r.get('environment'))
else:
    for e in resp.get('errors',[]):
        print(f'Error {e["code"]}: {e["message"]}')
    print('Response:', json.dumps(resp, indent=2)[:500])