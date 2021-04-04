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


def output(safe=True):
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        df_log = pd.read_sql('SELECT * FROM log', conn)
        df_user = pd.read_sql('SELECT * FROM user', conn)
        df_user.rename(columns={"id": "user_id"}, inplace=True)
        df = pd.merge(df_log.drop(columns=["id"]), df_user[["user_id", "name"]], on="user_id").drop(columns=["user_id"])
        df = df.reindex(columns=['time', 'state', 'name']).sort_values("time").rename(
            columns={"time": "時刻", "state": "勤怠", "name": "名前"})
        n = str(datetime.now()).replace(':', '').replace('.', '').replace('-', '').replace(' ', '')
        file_name_footer = "attendance_log" if safe else "delete_backup"
        df.to_csv(f'logs/{n}_{file_name_footer}.csv', encoding='cp932', index=False)
        print(df)
        cur.close()
    return None


def delete():
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS USER')
        cur.execute('DROP TABLE IF EXISTS ATTENDANCE')
        cur.execute('DROP TABLE IF EXISTS LOG')
    return None
