import settings
import sqlite3
import pandas as pd
from datetime import datetime

dbname = settings.DN


def make_db():
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, uid TEXT, type STRING, created_at DATETIME)')
        cur.execute('CREATE TABLE attendance(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING, working BOOLEAN)')
        cur.execute(
            'CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING, state STRING, time DATETIME)')
        conn.commit()
    return None


def main(uid, card_type):
    user_name = None
    user_id = None
    flag = None
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM USER WHERE uid = ("%s")' % uid)
        res = cur.fetchone()
        if not res:
            print('未登録です。')
            print('名前を入力してください')
            username = input('>> ')
            cur.execute('INSERT INTO user(name, uid, type, created_at) values(? ,?, ?, DateTime("now"))',
                        (username, uid, card_type))
            print('登録が完了しました。\n')

            cur.execute('SELECT id FROM USER WHERE uid = ("%s")' % uid)
            user_id = cur.fetchone()[0]
            flag = True
            cur.execute('INSERT INTO attendance(user_id, working) values(? ,?)', (user_id, flag))
            user_name = username
        else:
            user_id = res[0]
            cur.execute('SELECT NAME FROM USER WHERE ID = ("%s")' % user_id)
            user_name = cur.fetchone()[0]
            cur.execute('SELECT WORKING FROM ATTENDANCE WHERE user_id = ("%s")' % user_id)
            flag = False if cur.fetchone()[0] == 1 else True
            cur.execute('UPDATE ATTENDANCE SET WORKING = ? WHERE user_id = ?', (flag, user_id))

        state = "出勤" if flag else "退勤"
        cur.execute('INSERT INTO log(user_id, state, time) values(?, ?, DateTime("now"))', (user_id, state))
        conn.commit()
    return user_name, flag


def output():
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        df = pd.read_sql('SELECT * FROM log', conn)
        n = str(datetime.now()).replace(':', '').replace('.', '').replace('-', '').replace(' ', '')
        df.to_csv(f'logs/{n}_attendance_log.csv', encoding='cp932', index=False)
        cur.close()
    return None



# make_db()