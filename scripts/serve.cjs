const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const types = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml', '.png':'image/png', '.pdf':'application/pdf', '.zip':'application/zip' };
const server = http.createServer((req, res) => {
  let file;
  try { file = path.resolve(root, '.' + decodeURIComponent(req.url.split('?')[0] === '/' ? '/index.html' : req.url.split('?')[0])); } catch { res.writeHead(400).end(); return; }
  const relative = path.relative(root, file);
  if (relative.startsWith('..') || path.isAbsolute(relative) || relative.split(path.sep).some(p => p.startsWith('.')) || relative.startsWith('reference') || relative.startsWith('tmp')) { res.writeHead(403).end(); return; }
  fs.readFile(file, (err, body) => { if (err) { res.writeHead(404).end('Not found'); return; } res.writeHead(200, {'Content-Type': (types[path.extname(file)] || 'application/octet-stream') + (['.html','.css','.js','.svg'].includes(path.extname(file)) ? '; charset=utf-8' : ''), 'X-Content-Type-Options':'nosniff'}); res.end(body); });
});
server.listen(4173, '127.0.0.1', () => console.log('UNSCRIPTED Local: http://127.0.0.1:4173'));
