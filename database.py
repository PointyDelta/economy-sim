import sqlite3
import sys
 
con = sqlite3.connect('food.db')
 
with con:
 
    cs = con.cursor()    
    ##cs.execute("CREATE TABLE elec_prices (Tariff FLOAT, Price FLOAT)")
    cs.execute("INSERT INTO manufacturing VALUES(0.5,12354.5624506)")
    cs.execute("INSERT INTO manufacturing VALUES(1,12389.6728889)")
    cs.execute("INSERT INTO manufacturing VALUES(2,12459.8937653)")
    cs.execute("INSERT INTO manufacturing VALUES(5,12670.5563948)")
    cs.execute("INSERT INTO manufacturing VALUES(10,13021.6607771)")
    cs.execute("INSERT INTO manufacturing VALUES(20,13723.8695418)")
    cs.execute("INSERT INTO manufacturing VALUES(30,14426.0783065)")

