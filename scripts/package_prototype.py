"""Build a self-contained offline HTML and ZIP from unchanged application sources."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import re

root=Path(__file__).resolve().parent.parent
out=root/'submission';out.mkdir(exist_ok=True)
html=(root/'index.html').read_text(encoding='utf-8-sig')
css=(root/'styles.css').read_text(encoding='utf-8-sig')
engine=(root/'engine.js').read_text(encoding='utf-8-sig')
app=(root/'app.js').read_text(encoding='utf-8-sig')
assert all('</script' not in s.lower() for s in [engine,app]),'Escape script terminators before packaging'
assert '</style' not in css.lower(),'Escape style terminators before packaging'
assert html.count('<link rel="stylesheet" href="styles.css">')==1
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+css+'\n</style>')
for name in ['engine.js','app.js']:
 assert html.count(f'<script defer src="{name}"></script>')==1
 html=html.replace(f'<script defer src="{name}"></script>','')
# Inline scripts run after their DOM exists; source order remains engine, then UI.
assert html.count('</body>')==1
html=html.replace('</body>','<script>\n'+engine+'\n</script>\n<script>\n'+app+'\n</script>\n</body>')
assert not re.search(r'<script[^>]+src=|<link[^>]+rel="stylesheet"',html,re.I)
standalone=out/'Arkaprava_Ghosh_IIT_Madras_Prototype.html'
standalone.write_bytes(html.encode('utf-8'))
dest=out/'Arkaprava_Ghosh_IIT_Madras_Prototype.zip'
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
 z.writestr('UNSCRIPTED/index.html',html.encode('utf-8'))
with ZipFile(dest) as z:
 assert z.testzip() is None
 assert z.namelist()==['UNSCRIPTED/index.html']
 assert z.read('UNSCRIPTED/index.html')==standalone.read_bytes()
print('Standalone HTML:',standalone.name)
print('ZIP verified:',dest.name,round(dest.stat().st_size/1024,1),'KB')
print('SHA256:',hashlib.sha256(dest.read_bytes()).hexdigest())
