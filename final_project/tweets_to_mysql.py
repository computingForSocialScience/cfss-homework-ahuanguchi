import os, json, pymysql

def write_to_mysql(cursor, json_file):
    print(json_file)
    with open(json_file, 'r') as f:
        saved = json.load(f)
    tweets_table = saved['tweets_table']
    entities_table = saved['entities_table']
    
    for row in tweets_table:
        for cell in row:
            if isinstance(cell, str):
                cell = cell.encode('utf-8', 'ignore')
    for row in entities_table:
        for cell in row[1:]:
            cell = ', '.join(cell)
    
    cursor.executemany('INSERT INTO tweets VALUES (' + ','.join(['%s'] * 10) + ');',
                       tweets_table)
    # cursor.executemany('INSERT INTO entities VALUES (' + ','.join(['%s'] * 4) + ');',
                       # entities_table)

if __name__ == '__main__':
    tweets_files = [x for x in os.listdir('.') if '_tweets' in x]
    
    db = pymysql.connect(user='root', database='cfss', charset='utf8mb4')
    c = db.cursor()
        
    try:
        c.execute('TRUNCATE tweets; TRUNCATE entities;')
        for tweets_file in tweets_files:
            write_to_mysql(c, tweets_file)
        db.commit()
    finally:
        c.close()
        db.close()
