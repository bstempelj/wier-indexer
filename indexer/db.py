import sqlite3


class DB:
  def __init__(self, db_name):
    self.conn = sqlite3.connect(db_name)
    self.cursor = self.conn.cursor()

  def create_tables(self):
    self.cursor.execute('CREATE TABLE IF NOT EXISTS IndexWord (word TEXT PRIMARY KEY);')
    self.cursor.execute('CREATE TABLE IF NOT EXISTS Posting (\
                word TEXT NOT NULL,\
                documentName TEXT NOT NULL,\
                frequency INTEGER NOT NULL,\
                indexes TEXT NOT NULL,\
                PRIMARY KEY(word, documentName),\
                FOREIGN KEY (word) REFERENCES IndexWord(word));')

  def drop_tables(self):
    self.cursor.execute('DROP TABLE IF EXISTS IndexWord')
    self.cursor.execute('DROP TABLE IF EXISTS Posting')

  def save_words(self, words):
    for word in words:
        self.cursor.execute('INSERT INTO IndexWord VALUES (?)', (word,))
    self.conn.commit()

  def save_domain_posting(self, domain):
    for site in domain:
        for word, freq_info in domain[site].items():
            (num_freq, freq_idxs) = freq_info
            freq_idxs = ','.join(str(e) for e in freq_idxs)
            site_path = str(site.relative_to('data').as_posix())
            self.cursor.execute('INSERT INTO Posting VALUES (?, ?, ?, ?)',
                        (word, site_path, num_freq, freq_idxs))
    self.conn.commit()

  def load_words(self):
    return [word[0] for word in self.cursor.execute('SELECT * FROM IndexWord')]

  def data_retrieval(self, query):
    words = ",".join(map(lambda x: "'" + x + "'", query.split(' ')))

    sql = "SELECT word, documentName, sum(frequency), group_concat(indexes) FROM Posting WHERE word in (" + words + ") group by documentName order by frequency desc"
    return self.cursor.execute(sql).fetchall()


  def close(self):
    self.conn.close()
