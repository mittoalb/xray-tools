"""Bundle web/index.html + physics.js + data.json into one self-contained HTML file.
Run: python3 tools/build_standalone.py
  -> dist/monochromator-workbench.html  (open locally)
  -> docs/index.html                    (served by GitHub Pages)
"""
import os
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
web = os.path.join(root, 'web')
page = open(os.path.join(web, 'index.html')).read()
phys = open(os.path.join(web, 'physics.js')).read()
data = open(os.path.join(web, 'data.js')).read()
inline = f'<script>\n{data}</script>\n<script>\n{phys}\n</script>'
tag = '<script src="data.js"></script>\n<script src="physics.js"></script>'
assert tag in page
page = page.replace(tag, inline)
html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>[hidden]{display:none!important}body{margin:0}img{max-width:100%}</style>\n'
        '</head>\n<body>\n' + page + '\n</body>\n</html>\n')
os.makedirs(os.path.join(root, 'dist'), exist_ok=True)
out = os.path.join(root, 'dist', 'monochromator-workbench.html')
open(out, 'w').write(html)
print('wrote', out, os.path.getsize(out) // 1024, 'kB')
docs = os.path.join(root, 'docs')
os.makedirs(docs, exist_ok=True)
open(os.path.join(docs, 'index.html'), 'w').write(html)
open(os.path.join(docs, '.nojekyll'), 'w').close()   # serve files as-is, no Jekyll processing
print('wrote', os.path.join(docs, 'index.html'))
