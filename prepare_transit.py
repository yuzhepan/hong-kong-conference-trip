from pathlib import Path
import requests, fitz, json
root = Path(__file__).parent
out = root / 'dist' / 'maps'
out.mkdir(parents=True, exist_ok=True)
items = {
 'west-kowloon-b2': 'https://www.highspeed.mtr.com.hk/res/pdf/WEK-station-layout-B2.pdf',
 'west-kowloon-area': 'https://www.highspeed.mtr.com.hk/res/pdf/WEK-location-map.pdf',
 'kowloon': 'https://www.mtr.com.hk/archive/ch/services/layouts/kow.pdf',
 'hong-kong': 'https://www.mtr.com.hk/archive/ch/services/layouts/hok.pdf',
 'sai-ying-pun': 'https://www.mtr.com.hk/archive/ch/services/layouts/syp.pdf',
}
for name, url in items.items():
    response = requests.get(url, timeout=45)
    response.raise_for_status()
    pdf = fitz.open(stream=response.content, filetype='pdf')
    page = pdf[0]
    scale = min(2.0, 2200/max(page.rect.width, page.rect.height))
    page.get_pixmap(matrix=fitz.Matrix(scale,scale), alpha=False).save(out/f'{name}.png')
    print(name, page.get_text()[:5000])
(out/'sources.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
