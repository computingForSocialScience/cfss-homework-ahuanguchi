import json, pymysql

def write_to_mysql(cursor, json_file):
    pass

if __name__ == '__main__':
    db = pymysql.connect(user='root', database='cfss')
    c = db.cursor()
    
    try:
        pass
    finally:
        c.close()
        db.close()
