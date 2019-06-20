from numpy import random
from random import randint
from .Comrad import Comrad
import torch

class Population():
    def __init__(self):
        self.sizepop = 2
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
        
        self.random_dataset()
        self.learning()

    def random_dataset(self):
        self.learnX = torch.randn(100000)  
        self.learnY = torch.exp(self.learnX)
        
        self.testX = torch.randn(100000)  
        self.testY = torch.exp(self.testX)
        
        self.validationX = torch.randn(1000)  
        self.validationY = torch.exp(self.validationX)

    def learning(self):
        found = False
        max_iterations = 100
        self.people = self.generate()
        i=0
        while i<max_iterations:
            print("\t\tGENERATION "+str(i+1))
            count = 1
            for j in self.people:
                print("COMRAD "+str(count))
                j.learn(self.learnX, self.learnY, self.validationX, self.validationY)
                count += 1
            self.mutation()
            self.crossover()
            self.selection()
            i += 1


    def generate(self):
        pop = []
        for i in range(self.sizepop):
            nbrlayers = randint(2,20)
            representation = []
            for j in range(nbrlayers):
                representation.append(randint(1,200))
            pop.append(Comrad(representation))
        return pop

    def selection(self):
        result = []
        
        for j in range(self.sizepop):
            max_fit = 0
            max_index = -1
            for i in self.people:
                i.test(self.testX, self.testY)
                if i.score>max_fit:
                    max_fit = i.score
                    max_index = self.people.index(i)
            result.append(self.people.pop(max_index))
            if len(result)==1:
                result[0].save()
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

