from pathlib import Path
from bs4 import BeautifulSoup

p = Path('.') / 'data'

sites = {
    'eprostor': p / 'e-prostor.gov.si',
    'euprava': p / 'e-uprava.gov.si',
    'evem': p / 'evem.gov.si',
    'podatki': p / 'podatki.gov.si'
}

if __name__ == '__main__':
    test_site = sites['eprostor'] / 'e-prostor.gov.si.1.html'
    with test_site.open(encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        title = soup.find_all(class_='c-content-title-1')[0].find('h1').string
        content = soup.find_all(class_='ce-bodytext')[0].get_text()
        print(content)
