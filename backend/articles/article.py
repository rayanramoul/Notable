import pickle
import torch

class Article:
    def __init__(self, arti):
        self.source = arti["source"]
        self.author = arti["author"]
        self.content =  arti["content"]
        self.description = arti["description"]
        self.title = arti["title"]
        self.urlToImage = arti["urlToImage"]
        self.tranformed = {}
        self.fake=""
        self.category="" 
        self.objectivity=""
        self.extract()
    def describe(self):
        print("SOURCE : "+str(self.source))
        print("AUTHOR : "+str(self.source))
        print("CONTENT PREVIEW : "+str(self.content[:20]))

    def extract(self):
        from postagging.transform import transform_to_pos
        count_vectorizer = pickle.load(open("../../training/models/countvectorizer-category.pickle", "rb"))
        transformer = pickle.load(open("../../training/models/tfidf-category.pickle", "rb"))
        model = pickle.load(open("../../training/models/model-category.pickle", "rb"))
        #print("Content : "+str(self.content))

        try:
            counts = count_vectorizer.transform([self.content])
        except:
            counts = count_vectorizer.transform([self.title])
        tfidf = transformer.transform(counts)
        self.category = model.predict(tfidf)

        try:
            self.tranformed = transform_to_pos(self.content)
        except:
            self.tranformed = transform_to_pos(self.title)
        grilli = []
        for i in self.tranformed:
            grilli.append(self.tranformed[i])
        import numpy as np
        gril_np = np.asarray(grilli)
        gril_torch = torch.tensor(gril_np)
        device = torch.device('cpu')
        gril_mid =gril_torch.to(device=device, dtype=torch.float32).type(torch.FloatTensor)
        
        
        model2 = torch.load("../../training/models/model-objectivity.pickle")
        model2.eval()
        with torch.no_grad():
            self.objectivity = torch.round(model2(gril_mid))
        
        model3 = pickle.load(open("../../training/models/model-fakenews.pickle", "rb"))
        count_vectorizer2 = pickle.load(open("../../training/models/countvectorizer-fake.pickle", "rb"))
        transformer2 = pickle.load(open("../../training/models/tfidf-fake.pickle", "rb"))
        try:
            counts2 = count_vectorizer2.transform([self.content])
        except:
            counts2 = count_vectorizer2.transform([self.title])
        tfidf2 = transformer2.transform(counts2)
        f = model3.predict(tfidf2)
        if "1" in str(f[0]):
            self.fake = "Fake"
        else:
            self.fake = "Not Fake"

        

        
        