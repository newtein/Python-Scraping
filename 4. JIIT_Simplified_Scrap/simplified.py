import urllib.request
import requests
import mysql.connector
from collections import defaultdict
from bs4 import BeautifulSoup

con=mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='simplified')
mycur=con.cursor();

url="https://www.jiitsimplified.com/view.php"
r=requests.get(url)
soup=BeautifulSoup(r.content,"html.parser")

for link2 in soup.find_all('a'):
            next=str(link2.get("href")) 
            if "company" in next:
                url="https://www.jiitsimplified.com/"+next
                company_name=next.replace("company/","").replace(".php","")
                r=requests.get(url)
                soup=BeautifulSoup(r.content.decode('utf-8', 'ignore'),"html.parser")
                for link1,link2 in zip(soup("div",{"class":"review"}),soup("div",{"class":"reviewdetail"})):
                    
                    for name,position,branch,year,package, gtips,skills,bandw in zip(link1('div',{"class":"name"}),link1('div',{"class":"position"}),link1('div',{"class":"branch"}),link2("div",{"class":"year"}),link2("div",{"class":"package"}),link2("div",{"class":"generaltips"}),link2("div",{"class":"skillrounds"}),link2("div",{"class":"bandw"})):
                             rawname=name.text.strip()
                             num=rawname[0:1]
                             name=rawname[4:].strip()
                             position=position.text.strip()
                             branch=branch.text.strip()
                             year=year.text.strip()
                             package=package.text.strip()
                             id=company_name+num
                             gtips=gtips.find("div",{"class":"box"}).text.strip()
                             key_skill=skills.findAll("div",{"class":"experience"})[0].text.strip()
                             key_tips=skills.findAll("div",{"class":"experience"})[1].text.strip()
                             books=bandw.findAll("div",{"class":"smallbox"})[0].text.strip()
                             web=bandw.findAll("div",{"class":"smallbox"})[1].text.strip()
                             insertQ=("insert into review (id,company, sno, name, year,package,branch,position) values (%s,%s, %s, %s, %s,%s,%s,%s)")
                             data=(id,company_name,num,name,year,package,branch,position)
                             mycur.execute(insertQ,data)
                             con.commit()
                             
                             print(num,name,position,branch,year,package)
                    r=0;
                    exper=defaultdict(list);
                    tip=defaultdict(list);
                    for rounds in link2("div",{"class":"rounds"}):                             
                             exp=rounds("div",{"class":"experience"})
                             
                             exper[r]=exp[0].text.strip()                           
                             tip[r]=exp[1].text.strip()
                             
                             r=r+1

                    insertQ=("insert into detail (id,r1Exp,r1Tips,r2Exp,r2Tips,r3Exp,r3Tips,r4Exp,r4Tips,key_skills,key_tips,books,web,general_tips) values (%s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    data=(id,exper[0],tip[0],exper[1],tip[1],exper[2],tip[2],exper[3],tip[3],key_skill,key_tips,books,web,gtips)
                    mycur.execute(insertQ,data)
                    con.commit()
       

