import re
from nltk import word_tokenize
from stopwords import stop_words_slovene as si_stopwords
from stopwords import oth_stopwords
from pathlib import Path
from bs4 import BeautifulSoup

p = Path('.') / 'data'

sites = {
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


if __name__ == '__main__':
    eprostor_sites = [
        site for site in sites['eprostor'].iterdir() if site.suffix == '.html']

    for site in eprostor_sites:
        parsed_words = parse_site(site)
        print('{} => {}'.format(site, len(parsed_words)))
