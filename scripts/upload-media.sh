#!/usr/bin/env bash
set -euo pipefail
cd /home/user/Fortunato
set -a; . ./.env; set +a
SC="/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad"
MAN="$SC/lavori_manifest.json"
OUT="$SC/lavori_media_map.json"

echo "[" > "$OUT"
first=1
# iterate manifest entries
count=$(python3 -c "import json;print(len(json.load(open('$MAN'))))")
for i in $(seq 0 $((count-1))); do
  slug=$(python3 -c "import json;print(json.load(open('$MAN'))[$i]['slug'])")
  cli=$(python3 -c "import json;print(json.load(open('$MAN'))[$i]['client'])")
  title=$(python3 -c "import json;print(json.load(open('$MAN'))[$i]['title'])")
  cat=$(python3 -c "import json;print(json.load(open('$MAN'))[$i]['category'])")
  f="$SC/lavori_web/$slug.jpg"
  [ -f "$f" ] || { echo "MISSING $f" >&2; continue; }
  alt="$cli - $title | Idea Marketing Reggio Calabria"
  # 1) upload binary
  resp=$(curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE/wp-json/wp/v2/media" \
      -H "Content-Disposition: attachment; filename=${slug}.jpg" \
      -H "Content-Type: image/jpeg" \
      --data-binary @"$f")
  id=$(echo "$resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
  if [ -z "$id" ]; then echo "UPLOAD FAIL $slug: $(echo "$resp"|head -c200)" >&2; continue; fi
  # 2) set title + alt + caption
  url=$(curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE/wp-json/wp/v2/media/$id" \
      -H "Content-Type: application/json" \
      -d "$(python3 -c "import json,sys;print(json.dumps({'title':'$cli - $title','alt_text':'''$alt''','caption':'$cli'}))")" \
      | python3 -c "import sys,json;print(json.load(sys.stdin).get('source_url',''))")
  echo "  ok $slug -> id=$id  $url" >&2
  [ $first -eq 1 ] && first=0 || echo "," >> "$OUT"
  python3 -c "import json;print(json.dumps({'slug':'$slug','id':$id,'url':'$url','client':'''$cli''','title':'''$title''','category':'$cat'}))" >> "$OUT"
done
echo "]" >> "$OUT"
echo "=== MAP ===" >&2
python3 -c "import json;m=json.load(open('$OUT'));print(len(m),'immagini caricate')" >&2
