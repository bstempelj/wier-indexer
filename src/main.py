from pathlib import Path

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
