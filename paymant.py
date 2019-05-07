#In The Name Of God
import sys
import sqlite3
import time
from tabulate import tabulate


try:
    conn = sqlite3.connect('Moneyes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pools(
                pays integer,
                ctgry text,
                time integer)''')
    conn.commit()
    conn.text_factory = str
    
    def Help():
        print('''Usage:
            hesabdari.py --init 
            hesabdari.py --add <amount> <category> (add category and amount to DataBase)
            ex: 
                [hesabdari.py --add 100 food]
            hesabdari.py --del <amount> <category> (delete category and amount to DataBase)
            ex:
                [hesabdari.py --del 100 food]
            hesabdari.py --show (show all category and amounts)
            hesabdari.py -s <category>  (show sorted category)
            ex:
                [hesabdari.py -s HeadPhone]
            ''')

    #show all database category
    def show():
        c.execute('SELECT * FROM pools')
        return c.fetchall()

    #show database category's sorted by sys.argv[2]
    def show2():
        c.execute('SELECT * FROM pools WHERE ctgry= :ctgry COLLATE NOCASE',({'ctgry':sys.argv[2]}))
        return c.fetchall()[0][1]
 
    if sys.argv[1] == '--add':
        print('Successfuly Added!!!')
        with conn:
            c.execute('INSERT INTO pools VALUES (:pays, :ctgry , :time)'
            ,{'pays': sys.argv[2] ,'ctgry' : sys.argv[3] , 'time' : time.strftime("%Y - %m - %d | %H:%M")})
   
    elif (sys.argv[1] == '--show') and (1 < len(sys.argv) < 3):
        c.execute("SELECT SUM(pays) FROM pools")
        result = c.fetchone()[0]
        print(f'Total : {result}-T')
        ss = show()
        print(tabulate(ss))

    elif (sys.argv[1] == '--show') and (len(sys.argv) > 2):
        ww = show2()
        print(tabulate(ww))

    elif (sys.argv[1] == '--del') and (len(sys.argv) > 2):
        with conn:
            c.execute('DELETE FROM pools WHERE ctgry =:ctgry AND pays = :pays COLLATE NOCASE'
            ,{'ctgry': sys.argv[2], 'pays' : sys.argv[3]})

    elif sys.argv[1] == '-h' or '--help':
        Help()
    
    conn.close()
except IndexError:
    print('''Type hesabdari.py [-h] Or [--help] Arguments''')