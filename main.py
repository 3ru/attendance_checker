import settings
from db import main
from admin import check
import nfc
import binascii
from datetime import datetime

while True:
    with nfc.ContactlessFrontend("usb") as clf:
        print("カードをスキャンしてください...\n")
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        ID = binascii.hexlify(tag.identifier).decode().upper()
        TYPE = tag.product
        if TYPE == "Type4Tag":
            print("このカードは対応していません⚠\n")
            continue
        elif ID == settings.AT:
            check()
            continue
        user, state = main(ID, TYPE)
        state = "出勤" if state else "退勤"
        print(datetime.now())
        print(user, "さんが", state, "しました\n")
