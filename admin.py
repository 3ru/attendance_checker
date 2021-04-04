from db import output, make_db, delete
import sys


def check():
    print("特殊なカードが認証されました\n数字を選択してください\n")
    print("1. csvを出力")
    print("2. データ削除")
    print("3. システム終了")
    ans = input('>> ')
    if ans == "1":
        print("勤怠ログをCSV出力しますか? y/N")
        ans = input('>> ')
        if ans == "y":
            output()
            print("\nlogsフォルダ下に出力されました\n")
    elif ans == "2":
        print("\n【注意】本当にDBを削除しますか? YES/n")
        ans = input('>> ')
        if ans == "YES":
            output(safe=False)
            delete()
            print("\n【推奨】全データを削除しました\n")
            print("DBを再構築しますか？ y/N")
            ans = input('>> ')
            if ans == "y":
                make_db()
                print("\nDBを再構築しました\n")
    elif ans == "3":
        print("\n【注意】本当にシステム終了しますか? YES/n")
        ans = input('>> ')
        if ans == "YES":
            print("\n管理者によって強制終了しました\n")
            sys.exit(0)

