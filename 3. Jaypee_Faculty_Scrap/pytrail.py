import urllib.request
import requests
import mysql.connector
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import mechanize

con=mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='test2')
mycur=con.cursor();



url={}
filename=6000
for p in range (0, 2):
         url[0]="http://www.jiit.ac.in/faculty_jiit.php?id=8617&dep=pd&page="+str(p)
         r=requests.get(url[0])
         soup=BeautifulSoup(r.content,"html.parser")
         i=0
         for link2 in soup.find_all('a'):
            next=str(link2.get("href")) 
            if "faculty_jiit" in next:
                url[i]="http://jiit.ac.in/"+next
                print (url[i])
                i=i+1
         
         for j in range(0, i):
            r=requests.get(url[j])
            soup=BeautifulSoup(r.content,"html.parser")
            print (url[j])
            Name=soup.find_all("div",{"class":"hit1"})
            print (Name[0].text)
            print (Name[1].text)

            link5=soup.find_all("div",{"class":"facultyimage"})
            link6=link5[0].find_all("img")
            imgsrc="http://jiit.ac.in/"+link6[0].get('src')
            
            #image starts
            
            imgsrc=imgsrc.replace(" ","%20")
            print (imgsrc)
            try:
              imgfile=open(str(filename)+".jpeg",'wb')
              img=urllib.request.urlopen(imgsrc).read()
              imgfile.write(img)
              imgbool=1
            except HTTPError as e:
               if e.code==403:
                  imgbool=0
                  print("Image not found")
             #image ends
                  
             #dept starts
            link7=soup.find_all("h1")
            dep=link7[0].text
             #dept ends
                
            
            tname=str(Name[0].text)
            deg=str(Name[1].text)
            
            insertQ=("insert into all_info (ID,dept, Name, Design, imgbool) values (%s,%s, %s, %s, %s)")
            data=(filename,dep,tname,deg, imgbool )
           
            mycur.execute(insertQ,data)
            con.commit()
            #info starts
            link3=soup.find_all("div",{"class":"hit"})
            link4=link3[0].find_all("li")
            for info in link4:
                           insert2=("insert into coll_info values (%s, %s)")
                           data2=(filename,info.text)
                           mycur.execute(insert2,data2)
                           #print (filename)
                           con.commit();
            

            #info ends
            filename=filename+1               





    

       

                 


    
                           




#for link in links:
     #print (link.contents[0])
#x="http://www.jiit.ac.in/faculty_jiit.php?id=1282745379&dep=cse&page=0"
#htmlfile=urllib.request.urlopen(x)
#htmltext=htmlfile.read()
#driver=webdriver.Chrome()
#driver.get("http://www.jiit.ac.in/faculty_jiit.php?id=1282745379&dep=cse&page=0")


