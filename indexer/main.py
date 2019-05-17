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
    """
    Parse all sites in a given domain and return a list of words.
    """
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

    # (3) parse sites and save postings in database
    start_t = time.time()
    eprostor = parse_domain(domains['eprostor'])
    db.save_domain_posting(eprostor[1])
    end_t = time.time() - start_t
    print('Parsed {} words in {} seconds.'.format(
        len(eprostor[0]), round(end_t, 2)), end='\n'*2)

    start_t = time.time()
    euprava = parse_domain(domains['euprava'])
    db.save_domain_posting(euprava[1])
    end_t = time.time() - start_t
    print('Parsed {} words in {} seconds.'.format(
        len(euprava[0]), round(end_t, 2)), end='\n'*2)

    # => EVEM ima 650 strani in na mojmu kompu traja čist predoug!!!
    # start_t = time.time()
    # evem = parse_domain(domains['evem'])
    # db.save_domain_posting(evem[1])
    # end_t = time.time() - start_t
    # print('Parsed {} words in {} seconds.'.format(
    #     len(evem[0]), round(end_t, 2)), end='\n'*2)

    # => PODATKI niso nič boljš, ker imajo 561 strani...
    # start_t = time.time()
    # podatki = parse_domain(domains['podatki'])
    # db.save_domain_posting(podatki[1])
    # end_t = time.time() - start_t
    # print('Parsed {} words in {} seconds.'.format(
    #     len(podatki[0]), round(end_t, 2)), end='\n'*2)

    # (4) save all found words in database
    db.save_words(set(eprostor[0] + euprava[0]))

    # (5) log number of found words
    print('Loaded {} words from database.'.format(len(db.load_words())))

    db.close()

