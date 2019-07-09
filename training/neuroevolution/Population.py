from numpy import random
from random import randint
from Comrad import Comrad
import torch

class Population():
    def __init__(self):
        self.sizepop = 20
        self.datafile = "path" 
        self.people = []
        
        self.learnX = []
        self.testX = []
        self.validationX = []

        self.learnY = []
        self.testY = []
        self.validationY =[ ]
        
        self.crossrate = 10
        self.mutationrate = 10
        
        self.ntrain = 30

        self.global_best_score = 0

        self.load_dataset()
        self.learning()

    def load_dataset(self):
        import numpy as np # linear algebra
        import pandas as pd 
        import pickle

        from sklearn.naive_bayes import MultinomialNB
        from sklearn.model_selection import train_test_split

        file = pd.read_excel("../../datasets/SportsArticles/features.xlsx")
        file.dropna()



        # Get output 
        output = file["Label"]
        #print(str(output.head()))

        # Get input 
        inputs = file.drop(['Label','TextID','URL','baseform','fullstops','imperative','present3rd','present1st2nd','sentence1st','sentencelast','txtcomplexity','pronouns1st','pronouns2nd','pronouns3rd','compsupadjadv','past','ellipsis','semanticobjscore','semanticsubjscore'], axis=1)
        inputs = inputs.rename(index=str, columns={"NNPs": "NNP", "INs": "IN","TOs":"TO","semicolon":";","commas":",","colon":":"})
        kek = list(inputs)
        ot = ['NNP', 'VBD', 'VBN', 'IN', 'CD', 'VBP', ',', 'DT', 'NN', 'JJ', 'RB', 'TO', 'SYM', 'PRP', 'NNS', 'CC', 'PRP$', 'POS', 'FW', 'VBG', ':', 'WRB', 'EX', 'JJR', 'WDT', 'totalWordsCount', ';', 'questionmarks', 'exclamationmarks', 'Quotes']
        inputs = inputs[ot]
        print(" LISTE : "+str(list(inputs.columns)))
        print(" LEN LISTE : "+str(len(list(inputs.columns))))

        #print(str(list(inputs)))

        # 0 = objective
        # 1 = subjective
        output = output.replace("objective", 0)
        output = output.replace("subjective", 1)

        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        device = torch.device('cpu')


        self.learnX, self.testX, self.learnY , self.testY = train_test_split(inputs, output, test_size=0.33, shuffle=True)
        self.learnX = torch.tensor(self.learnX.to_numpy())
        self.learnY = torch.tensor(self.learnY.to_numpy())
        self.learnX = self.learnX.to(device=device, dtype=torch.int64).type(torch.FloatTensor)
        self.learnY = self.learnY.to(device=device, dtype=torch.int64).type(torch.FloatTensor)
        self.testX = torch.tensor(self.testX.to_numpy())
        self.testY = torch.tensor(self.testY.to_numpy())
        self.testX = self.testX.to(device=device, dtype=torch.float32).type(torch.FloatTensor)
        self.testY = self.testY.to(device=device, dtype=torch.float32).type(torch.FloatTensor)

        print("Training ")


        self.D_in = len(list(inputs))# Input Dimension
        self.D_out= 1


    def random_dataset(self):
        self.learnX = torch.randn(100000)  
        self.learnY = torch.exp(self.learnX)
        
        self.testX = torch.randn(100000)  
        self.testY = torch.exp(self.testX)
        
        self.validationX = torch.randn(1000)  
        self.validationY = torch.exp(self.validationX)

    def learning(self):
        found = False
        max_iterations = 3
        self.people = self.generate()
        i=0
        while i<max_iterations:
            self.mutation()
            self.crossover()
            self.selection()
            i += 1


    def generate(self):
        pop = []
        for i in range(self.sizepop):
            nbrlayers = randint(2,20)
            representation = []
            representation_activs = []
            learning_rate = random.uniform(1e-5,1e-8)
            for j in range(nbrlayers):
                representation.append(randint(1,200))
                if(j==nbrlayers-1):
                    representation_activs.append("sigmoid")
                else:
                    representation_activs.append(random.choice(["relu","sigmoid","tanh","lrelu"]))
            optim = random.choice(["lbfg","rp","sgd","adam"])
            pop.append(Comrad(representation, representation_activs, learning_rate, optim,self.D_in, self.D_out))
        return pop

    def selection(self):
        result = []
        count = 1
        for j in range(self.sizepop):
            max_fit = 0
            max_index = -1
            for i in self.people:
                i.learn(self.learnX, self.learnY, self.testX, self.testY, self.ntrain)
                if i.score>max_fit:
                    max_fit = i.score
                    max_index = self.people.index(i)
                if i.score>self.global_best_score:
                    self.global_best_score = i.score
                    print('\n\n')
                    print("BEST MODEL WITH "+str(i.score))
                    print(str(i.model))
                    print('\n\n')
                    i.save()
            result.append(self.people.pop(max_index))
            
        self.people = result

    def mutation(self):
        for i in range(self.mutationrate):
            random.choice(self.people).mutate()

    def crossover(self):
        for i in range(self.mutationrate):
            self.people.append(random.choice(self.people).crossover(random.choice(self.people)))
    
    def load_best(self):
        model = torch.load("trained_model")
        model.eval()
        return model

pop = Population()
