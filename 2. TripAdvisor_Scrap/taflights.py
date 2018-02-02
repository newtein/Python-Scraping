import requests
import mysql.connector
from bs4 import BeautifulSoup


con=mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='tripadvisor')
mycur=con.cursor();

for i in range (0,26):
 url="https://www.tripadvisor.in/MetaPlacementAjax?placementName=airlines_index_main&wrap=true&skipLocation=true&page="+str(i)
 r=requests.get(url)
 soup=BeautifulSoup(r.content,"html.parser")
 data=soup("div",{"class":"airlineData"})

 for flights in data:
     for name,link in zip(flights("div",{"class":"airlineName"}),flights.find_all('a')):
         next=str(link.get("href"))
         word=next[17:26]
         index=word.index('-')
         print(name.text.strip())
         insertQ=("insert into flights (id,name) values (%s,%s)")
         dat=(word[:index].strip(),name.text.strip())
         mycur.execute(insertQ,dat)

con.commit()
         


