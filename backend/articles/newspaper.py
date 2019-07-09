key="8dd30817317e423daacc736d07f34ebc"



from newsapi import NewsApiClient
from article import Article

class News:
       def __init__(self):
              self.newsapi = NewsApiClient(api_key=key)
              
       def get_sources(self, addi):
              l = self.newsapi.get_sources()['sources']
              ret = []
              for i in l:
                     if i["language"]=="en" and i["id"] not in addi:
                            ret.append(i["id"])
              return ret

       def write_sources(self):
              l = self.newsapi.get_sources()['sources']
              ret = []
              for i in l:
                     if i["language"]=="en":
                            ret.append(i["id"])
              r=open('../../sources','w')
              for i in ret:
                     r.write(str(i)+'*')

       def get_articles(self, sources):
              
              while '' in sources:
                     sources.remove('')
              if len(sources)==0:
                     return []
              all_articles = self.newsapi.get_everything(sources=','.join(sources),
                                                 language='en',
                                                 sort_by='relevancy',
                                                 pageSize=20,)
              arts = []
              print("NUMBER ARTICLES : "+str(len(all_articles['articles'])))
              count=1
              for i in range(len(all_articles['articles'])):
                     print("count : "+str(count))
                     a = Article(all_articles['articles'][i])
                     arts.append(a)
                     count+=1
              print("ARTS LEN :"+str(len(arts)))
              return arts