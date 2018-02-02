import urllib
import requests
import mechanicalsoup
import mysql.connector
from bs4 import BeautifulSoup
from urllib.error import HTTPError

#Enter Term To search and Enter Max Pages To crawl
term="java logging".replace(' ','%20')
pages=260

#mysql connection
con=mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='javalog')
mycur=con.cursor();
#mysql connection end

br=mechanicalsoup.Browser()
br.addheaders=[('User-agent','chrome')]
sno=0;
for j in range (0,pages,10):
 query="http://www.google.com/search?num=10&q="+term+"&start="+str(j)
   
 htmltext=br.get(query)
 soup=BeautifulSoup(htmltext.content,"html.parser")
 search=soup.findAll('div',attrs={'id':'search'})

 for websites in search[0].find_all('div',attrs={'class':'g'}):
    #heading 
    headings=websites.find_all('h3',attrs={'class':'r'})
    heading=headings[0].text
    print (heading)
    #heading ends

    #url starts
    urls=websites.find_all('cite')
    try:
        url="http://"+urls[0].text
        print (url)
    except IndexError:
        url="NULL"
        print ('error')
    #url ends

    #content starts
    contents=websites.find_all('span',attrs={'class':'st'})
    try:
          content=contents[0].text
          print (content)
    except IndexError:
          content="NULL"
          print ('error')
    #content ends
          
    #query starts
    insertQ=("insert into javalogging (sno, heading, URL, content) values (%s,%s, %s, %s)")
    data=(sno,heading,url,content)       
    mycur.execute(insertQ,data)
    con.commit()
    sno=sno+1;
    #query ends
          

