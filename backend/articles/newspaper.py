key="8dd30817317e423daacc736d07f34ebc"



from newsapi import NewsApiClient
from backend.articles.article import Article

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

       def get_articles(self, sources):
              
              while '' in sources:
                     sources.remove('')
              print("SOURCES : "+str(sources))
              if len(sources)==0:
                     return []
              all_articles = self.newsapi.get_everything(q='bitcoin',
                                                 sources=','.join(sources),
                                                 language='en',
                                                 sort_by='relevancy',)
              arts = []
              for i in range(len(all_articles)):
                     arts.append(Article(all_articles['articles'][i]))
              return arts