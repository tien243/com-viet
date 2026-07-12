#!/usr/bin/env python3
import subprocess, json

# Read token
with open('/tmp/cf_token2') as f:
    t = f.read().strip()

# Build header parts
bearer = 'Bearer ' + t
a = 'Authorization: ' + bearer
headers = ['-H', a, '-H', 'Content-Type: application/json']
acc = '13dbd75f367f8c2cd1f5ab8edc36641e'

# Get zone
r = subprocess.run(['curl', '-s', f'https://api.cloudflare.com/client/v4/zones?name=combonau.com',
    '-H', a], capture_output=True, text=True, timeout=10)
zones = json.loads(r.stdout)
if zones.get('result'):
    zone_id = zones['result'][0]['id']
    print(f'Zone: {zone_id}')
    
    # Add domain
    body = json.dumps({'zone_id': zone_id, 'custom_domain': 'combonau.com'})
    r2 = subprocess.run(['curl', '-s', '-X', 'POST',
        f'https://api.cloudflare.com/client/v4/accounts/{acc}/pages/projects/com-bo-nau/domains',
        *headers, '-d', body], capture_output=True, text=True, timeout=15)
    resp = json.loads(r2.stdout)
    if resp.get('success'):
        print("✅ Domain added! Status:", resp['result'].get('status'))
    else:
        for e in resp.get('errors',[]):
            print(f'Error {e["code"]}: {e["message"]}')
else:
    print('Zone not found')