from newspaper import News
import os
from datetime import date
import urllib.request
today = str(date.today())

new = News()
r = open("../../sources_save","r")
d = r.readlines()
sources = []
for i in d:
    sources+=i.split("*")
new.write_sources()
arts = new.get_articles(sources)
path = "./downloaded/"
for i in arts:
    i.title=i.title.replace('/','-')
    i.title=i.title.replace(',',' ')
    dire = path+i.title+'.'+str(today)
    os.mkdir(dire)
    dire+='/'
    fil = open(dire+"article","w")

    fil.write('author:'+str(i.author)+'\n')
    fil.write('title:'+str(i.title)+'\n')
    fil.write('fake:'+str(i.fake)+'\n')
    fil.write('category:'+str(i.category)+'\n')
    fil.write('description:'+str(i.description)+'\n')
    fil.write('objectivity:'+str(i.objectivity)+'\n')
    fil.write('content:\n'+str(i.content)+'\n')
    try:
        urllib.request.urlretrieve(str(i.urlToImage), dire+"image.jpg")
    except:
        urllib.request.urlretrieve("https://www.incimages.com/uploaded_files/image/970x450/getty_883231284_200013331818843182490_335833.jpg", dire+"image.jpg")
    
    fil.close()
