T=$(cat /tmp/cf_token2)

# Add CNAME DNS record
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/4c9aae6c6e80023b10d646cd586f1def/dns_records" \
  -H "Authorization: Bearer $T" \
  -H "Content-Type: application/json" \
  -d '{"type":"CNAME","name":"combonau.com","content":"com-bo-nau.pages.dev","proxied":true}' | python3 -c '
import sys,json
d=json.load(sys.stdin)
if d.get("success"):
    print("CNAME added:", d["result"]["name"], "->", d["result"]["content"])
else:
    for e in d.get("errors",[]):
        print("Error", e["code"], ":", e["message"])
'