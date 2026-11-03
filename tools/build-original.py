#!/usr/bin/env python3
"""Build a Starship-derived theme with the original 20 artworks in grayscale."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True, help='Original Quattro Sunset checkout')
parser.add_argument('--output', type=Path, required=True, help='New output directory; must not already exist')
parser.add_argument('--base-theme', type=Path, default=Path('/usr/share/omarchy/themes/starship'))
args = parser.parse_args()
root = args.output.resolve()
source = args.source.resolve()
base = args.base_theme.resolve()
root.mkdir(exist_ok=False)
for p in base.iterdir():
    if p.is_file() and p.name != 'preview.png':
        shutil.copy2(p, root / p.name)
(root / 'backgrounds').mkdir()
(root / 'previews').mkdir()
(root / 'tools').mkdir()
shutil.copy2(__file__, root / 'tools/build-original.py')
shutil.copy2(source / 'LICENSE', root / 'LICENSE')
entries = json.loads((source / 'wallpapers.json').read_text())['wallpapers']
catalog = []
font = subprocess.check_output(['fc-match', '-f', '%{file}', 'sans'], text=True).strip()
gallery = ['magick', 'montage', '-font', font, '-pointsize', '16', '-fill', '#f5f5f7', '-background', '#1c1c1e']
for i, entry in enumerate(entries, 1):
    original = source / entry['file']
    assert hashlib.sha256(original.read_bytes()).hexdigest() == entry['sha256']
    filename = '07-jerusalem-sunset.png' if i == 7 else original.name
    target = root / 'backgrounds' / filename
    subprocess.run(['magick', str(original), '-grayscale', 'Rec709Luma', '-sigmoidal-contrast', '2.5x45%', '-depth', '8', str(target)], check=True)
    result = subprocess.check_output(['magick', 'identify', '-format', '%wx%h %[colorspace]', str(target)], text=True)
    assert result.startswith(f"{entry['width']}x{entry['height']}")
    # Every pixel has equal red, green and blue channels; original geometry is unchanged.
    chroma = subprocess.check_output(['magick', str(target), '-colorspace', 'sRGB', '-fx', 'max(r,max(g,b))-min(r,min(g,b))', '-format', '%[fx:maxima]', 'info:'], text=True)
    assert float(chroma) == 0
    catalog.append({**entry, 'file': 'backgrounds/' + filename, 'original_sha256': entry['sha256'], 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    gallery += ['-label', f"{i:02}  {entry['title']}", str(target)]
    print(f'{i:02}/20 {entry["title"]}', flush=True)
subprocess.run(gallery + ['-geometry', '384x256+12+12', '-tile', '4x5', str(root / 'previews/wallpaper-gallery.jpg')], check=True)
subprocess.run(['magick', str(root / catalog[0]['file']), '-resize', '768x512', str(root / 'preview.png')], check=True)
(root / 'wallpapers.json').write_text(json.dumps({'theme': 'Biblical Graphite', 'base_theme': 'Starship', 'method': 'Rec709Luma grayscale, sigmoidal contrast 2.5x45%; no resizing, blur or spatial filtering', 'wallpapers': catalog}, indent=2) + '\n')
(root / 'README.md').write_text('''# Biblical Graphite

A clone of the laptop's Starship theme with 20 grayscale biblical wallpapers from sthuizen's Quattro Sunset collection, source commit a0d5fd80bea51c11a9df70e02cb28c0ce3329608.

The Starship interface palette is preserved. The artwork uses Rec.709 luminance grayscale with gentle sigmoidal contrast (2.5x45%). No blur, rescaling or spatial filtering changes the original outlines. All wallpapers remain 1536 × 1024. The original colours and files remain in the source repository.

Omarchy and its contributors supplied the Starship theme. The original artwork licence is preserved in LICENSE. wallpapers.json records source and output SHA-256 checksums. previews/wallpaper-gallery.jpg shows the full collection.

Install by copying this directory to ~/.config/omarchy/themes/biblical-graphite, then run `omarchy theme set biblical-graphite`. Use `omarchy theme bg next` to cycle the 20 wallpapers. Return with `omarchy theme set starship`.

tools/build-original.py reproduces the artwork using explicit source and output directories. It creates a fresh output directory and refuses to overwrite an existing one. Python 3, ImageMagick and Fontconfig are required.
''')
print('Built and verified 20 grayscale wallpapers in', root)
