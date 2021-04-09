<img src="docs/title.jpg">  

![GitHub top language](https://img.shields.io/github/languages/top/Ryuyxx/attendance_checker?style=for-the-badge)
![GitHub repo file count](https://img.shields.io/github/languages/code-size/Ryuyxx/attendance_checker?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Ryuyxx/attendance_checker?style=for-the-badge)


<h3 align="center">
    Attendance management system
</h3>

## Description
This is a attendance management system using NFC tags.  
It uses the [`nfcpy`](https://nfcpy.readthedocs.io/en/latest/) library to retrieve the card information and store it in a database.  
Since I'm Japanese, console logs are displayed in Japanese.  


## Dependency
Only three additionals need to be installed
- nfcpy
- pandas
- python-dotenv
- sqlite3
- binascii
- datetime


## Usage  

1. Get nfc card reader [ex.](https://www.amazon.com/nfc-reader/s?k=nfc+reader) (I'm Using [PaSoRi RC-S380](https://www.sony.net/Products/felica/business/products/RC-S380.html))

2. Follow [here](https://nfcpy.readthedocs.io/en/latest/topics/get-started.html)  

3. Install
   
    ```bash
    $ pip install nfcpy   # Should be installed on Step 2
    $ pip install pandas
    $ pip install python-dotenv
    ```
    
4. Settings  

    1. make `.env` file
    2. set database location and admin card id.  
       (To get the card ID, look inside the DB or use like [this](https://github.com/Ryuyxx/idm-check/blob/master/main.py))
    ```text
    DBNAME = "dbs/USER.db"
    ADMIN_TYPE = "XXXXXXXXX"
    ```

5. Run
   
    ```bash
    python3 main.py
    ```


## ERD

    Soon...