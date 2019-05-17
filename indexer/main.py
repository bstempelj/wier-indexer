import re, time
from nltk import word_tokenize
from stopwords import stop_words_slovene as si_stopwords
from stopwords import oth_stopwords
from pathlib import Path
from bs4 import BeautifulSoup

from db import DB


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

        word_freq = {}
        for i, word in enumerate(words):
            if word not in word_freq:
                word_freq[word] = (1, [i])
            else:
                num_freq = word_freq[word][0]
                freq_idxs = word_freq[word][1]
                word_freq[word] = (num_freq+1, freq_idxs+[i])

        return words, word_freq


def parse_domain(domain):
    sites = [site for site in domain.iterdir() if site.suffix == '.html']
    print('Parsing {} sites from {}...'.format(len(sites), domain))

    sites_with_word_freqs = {}
    domain_words = []
    for site in sites:
        (words, word_freq) = parse_site(site)
        domain_words += words
        sites_with_word_freqs[site] = word_freq

    return domain_words, sites_with_word_freqs


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

    # (3) parse sites and save posting
    # and words in database
    distinct_words = set()

    for domain_name in domains:
        # predolgo trajata na laptopu, bom na kišti pognou :)
        if domain_name in ['evem', 'podatki']:
            continue
        start_t = time.time()
        domain = parse_domain(domains[domain_name])
        db.save_domain_posting(domain[1])
        distinct_words.update(domain[0])
        end_t = time.time() - start_t
        print('Parsed {} words in {} seconds.'.format(
            len(domain[0]), round(end_t, 2)), end='\n'*2)

    db.save_words(distinct_words)

    # (4) log number of found words
    print('Loaded {} distinct words from database.'.format(len(db.load_words())))

    db.close()
