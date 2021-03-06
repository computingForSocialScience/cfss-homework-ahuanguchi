import os, json, pymysql

def write_to_mysql(cursor, json_file):
    print(json_file)
    with open(json_file, 'r') as f:
        saved = json.load(f)
    tweets_table = saved['tweets_table']
    entities_table = saved['entities_table']        # table rows (tuples) stored as JSON arrays, read as lists
    
    for i in range(len(entities_table)):            # replace nested lists in table cells with strings
        for j in range(1, len(entities_table[i])):
            entities_table[i][j] = ', '.join(entities_table[i][j])
    
    cursor.executemany('INSERT INTO tweets VALUES (' + ','.join(['%s'] * 10) + ')',
                       tweets_table)                # id not primary key because same tweet can have different search terms
    cursor.executemany('INSERT IGNORE INTO entities VALUES (' + ','.join(['%s'] * 4) + ')',
                       entities_table)              # each id (primary key) ends up being unique

if __name__ == '__main__':
    tweets_files = [x for x in os.listdir('.') if x.endswith('_tweets.json')]
    
    db = pymysql.connect(user='root', database='cfss', charset='utf8mb4')
    c = db.cursor()
    
    try:
        c.execute('TRUNCATE tweets;')
        c.execute('TRUNCATE entities;')
        for tweets_file in tweets_files:
            write_to_mysql(c, tweets_file)
        db.commit()
    finally:
        c.close()
        db.close()
