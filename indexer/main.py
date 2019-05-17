import re, time
from nltk import word_tokenize
from stopwords import stop_words_slovene as si_stopwords
from stopwords import oth_stopwords
from pathlib import Path
from bs4 import BeautifulSoup

from db import DB


def parse_site(site):
    """
    Find text the body of a site, split by words, convert them to
    lowercase and strip out the unimportant ones. The result is a
    list.
    """
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
    """
    Parse all sites in a given domain and return a list of words.
    """
    sites = [site for site in domain.iterdir() if site.suffix == '.html']
    print('Parsing {} sites from {}...'.format(len(sites), domain))
    words = []
    for site in sites:
        words += parse_site(site)
    return words


if __name__ == '__main__':
    # (1) set paths to websites
    p = Path('.') / 'data'
    domains = {
        'eprostor': p / 'e-prostor.gov.si',
        'euprava': p / 'e-uprava.gov.si',
        'evem': p / 'evem.gov.si',
        'podatki': p / 'podatki.gov.si'
    }

    # (2) init database
    db = DB('inverted-index.db')
    db.drop_tables()
    db.create_tables()

    # (3) parse data
    start_t = time.time()
    eprostor = parse_domain(domains['eprostor'])
    end_t = time.time() - start_t
    print('Parsed {} words in {} seconds.'.format(
        len(eprostor), round(end_t, 2)), end='\n'*2)

    start_t = time.time()
    euprava = parse_domain(domains['euprava'])
    end_t = time.time() - start_t
    print('Parsed {} words in {} seconds.'.format(
        len(euprava), round(end_t, 2)), end='\n'*2)

    # => EVEM ima 650 strani in na mojmu kompu traja čist predoug!!!
    # start_t = time.time()
    # evem = parse_domain(domains['evem'])
    # end_t = time.time() - start_t
    # print('Parsed {} words in {} seconds.'.format(
    #     len(evem), round(end_t, 2)), end='\n'*2)

    # => PODATKI niso nič boljš, ker imajo 561 strani...
    # start_t = time.time()
    # podatki = parse_domain(domains['podatki'])
    # end_t = time.time() - start_t
    # print('Parsed {} words in {} seconds.'.format(
    #     len(podatki), round(end_t, 2)), end='\n'*2)

    # (5) save words to database, query them back and
    # close connection to database
    db.save_words(set(eprostor + euprava))
    print('Loaded {} words from database.'.format(len(db.load_words())))
    db.close()

