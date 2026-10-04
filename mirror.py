from pathlib import Path
import re, html, urllib.request, urllib.parse, hashlib, concurrent.futures, json

root = Path(__file__).parent
dist = root / 'dist'
source = Path('/tmp/kitalabel-reference.html').read_text()
# Keep the original public design, but remove tracking, WordPress runtime and forms.
source = re.sub(r'<script\b[^>]*>.*?</script>', '', source, flags=re.S|re.I)
source = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', source, flags=re.S|re.I)
source = re.sub(r'<link[^>]+(?:api\.w\.org|xmlrpc|wlwmanifest|canonical|oembed)[^>]*>', '', source)
source = re.sub(r'<title>.*?</title>', '<title>KitaLabel — Demo SapaGo</title>', source, flags=re.S)
source = re.sub(r'(<form\b[^>]*).*?(</form>)', '<div class="demo-form-note">Konsultasikan kebutuhan label melalui chat di kanan bawah.</div>', source, flags=re.S|re.I)
source = source.replace('loading="lazy"', 'loading="eager"')
assets = {}
pattern = r'https://marketz\.kitalabel\.com/[^\s\"<>\)\(\x27]+'

def urls(text):
    results = set()
    for value in re.findall(pattern, html.unescape(text)):
        value = value.rstrip(';\\')
        if re.search(r'\.(css|png|jpg|jpeg|webp|svg|mp4|woff2?|ttf|gif)(?:\?|$)', value):
            results.add(value)
    return results

def download(url):
    ext = Path(urllib.parse.urlparse(url).path).suffix
    name = hashlib.sha256(url.encode()).hexdigest()[:12] + ext
    path = dist / 'assets' / name
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=40) as resp: data = resp.read()
        path.write_bytes(data)
        return url, name, None
    except Exception as e: return url, None, str(e)

pending = urls(source)
for stage in range(4):
    if not pending: break
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        for url, name, error in pool.map(download, pending):
            if name: assets[url] = name
            else: print('FAILED', url, error)
    next_urls=set()
    for url, name in list(assets.items()):
        if not name.endswith('.css'): continue
        path=dist/'assets'/name
        css=path.read_text()
        def absolute(m):
            raw=m.group(1).strip(' \"\x27')
            if raw.startswith('data:'): return m.group(0)
            return 'url("'+urllib.parse.urljoin(url,raw)+'")'
        css=re.sub(r'url\(([^)]+)\)',absolute,css)
        path.write_text(css)
        next_urls |= urls(css)
    pending=next_urls-set(assets)

for url,name in sorted(assets.items(),key=lambda x:-len(x[0])):
    source=source.replace(html.escape(url, quote=True), 'assets/'+name).replace(url,'assets/'+name)
    for cssfile in (dist/'assets').glob('*.css'):
        css=cssfile.read_text().replace(url,name)
        cssfile.write_text(css)
# Make all consultation actions use the demo assistant.
source=re.sub(r'href="https://(?:api\.whatsapp\.com|wa\.me)[^"]*"', 'href="#sapago" data-chat="true"', source)
source=source.replace('href="#form"', 'href="#sapago" data-chat="true"')
source=re.sub(r'href="https://marketz\.kitalabel\.com/(?:kitalabel-doxa-lp-new/)?"', 'href="#"', source)
source=source.replace('</head>', '<link rel="stylesheet" href="demo.css"></head>')
source=source.replace('</body>', (root/'widget.html').read_text()+'<script src="config.js"></script><script src="demo.js"></script></body>')
(dist/'index.html').write_text(source)
manifest=json.loads((root/'.openai/hosting.json').read_text())
manifest['static']={'directory':'dist'}
(root/'.openai/hosting.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Mirrored',len(assets),'assets')
