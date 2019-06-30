import pickle
import torch

class Article:
    def __init__(self, arti):
        print("keys : "+str(arti.keys()))
        self.source = arti["source"]
        self.author = arti["author"]
        self.content =  arti["content"]
        self.description = arti["description"]
        self.title = arti["title"]
        self.urlToImage = arti["urlToImage"]
        self.extract()
        self.tranformed = {}
        self.fake=88
        self.category="sports" 
        self.objectivity="objective"
    def describe(self):
        print("SOURCE : "+str(self.source))
        print("AUTHOR : "+str(self.source))
        print("CONTENT PREVIEW : "+str(self.content[:20]))

    def extract(self):
        from training.postagging.transform import transform_to_pos
        count_vectorizer = pickle.load(open("./training/models/countvectorizer.pickle", "rb"))
        transformer = pickle.load(open("./training/models/tfidf.pickle", "rb"))
        model = pickle.load(open("./training/models/model-category.pickle", "rb"))
        #print("Content : "+str(self.content))
        counts = count_vectorizer.transform([self.content])
        tfidf = transformer.transform(counts)
        self.tranformed = transform_to_pos(self.content)
        grilli = []
        for i in self.tranformed:
            grilli.append(self.tranformed[i])
        import numpy as np
        gril_np = np.asarray(grilli)
        gril_torch = torch.tensor(gril_np)
        device = torch.device('cpu')
        gril_mid =gril_torch.to(device=device, dtype=torch.float32).type(torch.FloatTensor)
        self.category = model.predict(tfidf)
        model = pickle.load(open("./training/models/model-fakenews.pickle", "rb"))

        self.fake = model.predict(tfidf)

        model = pickle.load(open("./training/models/model-objectivity.pickle", "rb"))
        model.eval()
        with torch.no_grad():
            self.objectivity = torch.round(model(gril_mid))

        
        