import random
from .comrad import comrad
import torch

class population():
    def __init__(self):
        self.sizepop=2
        self.datafile="path" 
        self.people=[]
        
        self.learnX=[]
        self.testX=[]
        self.validationX=[]

        self.learnY=[]
        self.testY=[]
        self.validationY=[]
        
        self.crossrate=10
        self.mutationrate=10
        
        self.random_dataset()
        self.learning()

    def random_dataset(self):
        self.learnX=torch.randn(100000)  
        self.learnY=torch.exp(self.learnX)
        
        self.testX=torch.randn(100000)  
        self.testY=torch.exp(self.testX)
        
        self.validationX=torch.randn(1000)  
        self.validationY=torch.exp(self.validationX)

    def learning(self):
        found = False
        max_iterations = 100
        self.people = self.generate()
        i=0
        while i<max_iterations:
            print("NEW GENERATION "+str(i))
            for j in self.people:
                j.learn(self.learnX, self.learnY, self.validationX, self.validationY)
            self.mutation()
            self.crossover()
            self.selection()
            i+=1

    def fitness(self, comrad):
        pass

    def generate(self):
        pop = []
        for i in range(self.sizepop):
            nbrlayers = random.randint(2,20)
            representation = []
            for j in range(nbrlayers):
                representation.append(random.randint(1,200))
            pop.append(comrad(representation))
        return pop

    def selection(self):
        result=[]
        for j in range(self.sizepop):
            max_fit=0
            max_index=-1
            for i in self.people:
                i.test(self.testX, self.testY)
                if i.score>max_fit:
                    max_fit=i.score
                    max_index=self.people.index(i)
            result.append(self.people.pop(max_index))
        self.people=result

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

