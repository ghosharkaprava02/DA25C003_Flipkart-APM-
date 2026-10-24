"""Package only browser-runnable assets. No source prompts, personal details or dependencies."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib

root=Path(__file__).resolve().parent.parent
out=root/'submission';out.mkdir(exist_ok=True)
files=['index.html','styles.css','engine.js','app.js']
dest=out/'Arkaprava_Ghosh_IIT_Madras_Prototype.zip'
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
 for f in files:z.write(root/f,'UNSCRIPTED/'+f)
with ZipFile(dest) as z:
 assert z.testzip() is None
 for f in files:
  assert z.read('UNSCRIPTED/'+f)==(root/f).read_bytes(),f
 assert all(x.endswith(('.html','.css','.js')) for x in z.namelist())
print('ZIP verified:',dest.name,round(dest.stat().st_size/1024,1),'KB')
print('SHA256:',hashlib.sha256(dest.read_bytes()).hexdigest())
