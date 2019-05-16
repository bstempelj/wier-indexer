import re
from nltk import word_tokenize
from stopwords import stop_words_slovene as si_stopwords
from stopwords import oth_stopwords
from pathlib import Path
from bs4 import BeautifulSoup

p = Path('.') / 'data'

domains = {
    'eprostor': p / 'e-prostor.gov.si',
    'euprava': p / 'e-uprava.gov.si',
    'evem': p / 'evem.gov.si',
    'podatki': p / 'podatki.gov.si'
}


def parse_site(site):
    with site.open(mode='rb') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        # get body text
        body = soup.find('body')
        text = body.get_text()

        # tokenize content into lowercase words
        words = list(map(lambda w: w.lower(), word_tokenize(text)))

        # remove words that appear in slovenian stopwords
        words = list(filter(lambda w: w not in si_stopwords.union(oth_stopwords), words))

        return words


def parse_domain(domain):
    sites = [site for site in domain.iterdir() if site.suffix == '.html']
    print('Parsing {} sites from {}...'.format(len(sites), domain))
    words = []
    for site in sites:
        words += parse_site(site)
    return words


if __name__ == '__main__':
    print('#words:', len(parse_domain(domains['eprostor'])))
    print('#words:', len(parse_domain(domains['euprava'])))
    print('#words:', len(parse_domain(domains['evem'])))
    print('#words:', len(parse_domain(domains['podatki'])))

    # for site in eprostor_sites:
    #     parsed_words = parse_site(site)
    #     print('{} => {}'.format(site, len(parsed_words)))
