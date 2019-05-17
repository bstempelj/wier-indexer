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

  def load_words(self):
    return [word[0] for word in self.cursor.execute('SELECT * FROM IndexWord')]

  def close(self):
    self.conn.close()
