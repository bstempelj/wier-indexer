from pathlib import Path
from bs4 import BeautifulSoup

p = Path('.')
p = p / 'data'

sites = {
    'eprostor': p / 'e-prostor.gov.si',
    'euprava': p / 'e-uprava.gov.si',
    'evem': p / 'evem.gov.si',
    'podatki': p / 'podatki.gov.si'
}

def get_html_files(p):
    return [x for x in p.iterdir() if not x.is_dir() and x.suffix == '.html']

if __name__ == '__main__':
    files = []

    for site in sites.values():
        for f in get_html_files(site):
            files.append(f)

    print('#files:', len(files))

    with open(files[0], 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        title = soup.find_all(class_='c-content-title-1')[0].find('h1').string
        print(title)
