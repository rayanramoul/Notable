import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import mean_squared_error
from numpy import random
from random import choice

class Comrad():
    def __init__(self, representation, representation_activs, learning_rate, optim, din, dout):
        self.nbrlayers = 1
        self.layers= []
        self.score= 0
        self.epochs= 100
        self.representation = representation
        self.representation_activs = representation_activs
        self.learning_rate = learning_rate
        self.accuracies = []
        self.precisions = []
        
        self.D_in = din # Input Dimension
        self.D_out= dout # Output Dimension
        modules = []
        count = 0
        import torch.nn.functional as F
        for i in range(len(representation)):


            if count==0:
                modules.append(nn.Linear(self.D_in, representation[i]))
            elif count==len(representation)-1:
                modules.append(nn.Linear(representation[i-1], self.D_out))
            else:
                modules.append(nn.Linear(representation[i-1], representation[i]))
            

            if self.representation_activs[i]=='relu':
                modules.append(nn.ReLU())
            elif self.representation_activs[i]=='sigmoid':
                modules.append(nn.Sigmoid())
            elif self.representation_activs[i]=='tanh':
                modules.append(nn.Tanh())
            elif self.representation_activs[i]=='lrelu':
                modules.append(nn.LeakyReLU())           # Leaky relu
            count+=1
        self.model = nn.Sequential(*modules)
        
        if optim=="lbfg":
            optimizer = torch.optim.LBFGS(self.model.parameters(), lr=self.learning_rate)
        elif optim=="rp":
            optimizer = torch.optim.Rprop(self.model.parameters(), lr=self.learning_rate)
        elif optim=="sgd":
            optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)
        else:
            optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        self.optimizer = optimizer
        self.optim = optim
        
    def mutate(self):
        self.score = 0
        cho = choice([0,1,2,3])
        rep_activs = self.representation_activs
        rep = self.representation
        optim = self.optim
        learning_rate = self.learning_rate
        if cho==0:
            index = random.randint(0,len(rep)-1)
            rep[index] = random.randint(1,200)
        if cho==1:
            index = random.randint(0,len(rep_activs)-1)
            rep_activs[index] = choice(["relu","sigmoid","tanh","lrelu"]) 
        if cho==2:
            optim = choice(["lbfg","rp","sgd","adam"])

        else:
            learning_rate = random.uniform(1e-5,1e-8)

        
        self = Comrad(rep, rep_activs, learning_rate, optim, self.D_in, self.D_out)
        
    def crossover(self, comrad):
        pick = []
        pick.append(len(self.representation))
        pick.append(len(comrad.representation))
        #print("pick  :"+str(pick))
        size = choice(pick)
        newrep = []
        newrep_activs = []
        #print("size : "+str(size))
        for i in range(size):
            pick = []
            pick_act = []

            cho = random.choice([0,1])
            if cho==0:
                if i<len(self.representation):
                    newrep.append(self.representation[i])
                    newrep_activs.append(self.representation_activs[i])
                else:
                    newrep.append(comrad.representation[i])
                    newrep_activs.append(comrad.representation_activs[i])
            else:
                if i<len(comrad.representation):
                    newrep.append(comrad.representation[i])
                    newrep_activs.append(comrad.representation_activs[i])
                else:
                    newrep.append(self.representation[i])
                    newrep_activs.append(self.representation_activs[i])
            cho = random.randint(1,200)
        del newrep_activs[-1]
        newrep_activs.append("sigmoid")
        l = choice([self.learning_rate, comrad.learning_rate])
        opt = choice([self.optim, comrad.optim])
        #print("new size : "+str((len(newrep))))
        c = Comrad(newrep, newrep_activs, l, opt,self.D_in, self.D_out)

        return c

    def test(self, testX, testY):
        from sklearn.metrics import accuracy_score, precision_score
        testX = testX.resize_(100000, self.D_in)
        testY = testY.resize_(100000, self.D_out)
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            fX = torch.round(self.model(testX))
            fY = torch.round(testY)
            try:
                self.accuracies.append(accuracy_score(fX, fY))
                self.precisions.append(precision_score(fX, fY, average="micro"))
            except:
                print("LOST ///")
                print("LEARNING RATE : "+str(self.learning_rate))
                self.accuracies.append(0)
                self.precisions.append(0)

        #print("ACCURACY  : "+str(self.accuracy)+" PRECISION : "+str(self.precision))
        

    def learn(self, learnX, learnY, testX, testY, ntrain):
        
        print("\n\n"+str(self.model)+"\n")
        print("Optimizer : "+str(self.optimizer))
        print("Learning Rate : "+str(self.learning_rate))
        for traini in range(ntrain):
            

            N = 32 # Batch Size
            epochs = 100

            self.model.train()


            size = list(learnX.shape)[0]
            loss_fn = torch.nn.MSELoss(reduction='sum')
            for t in range(epochs):
                #print("Epoch ("+str(t+1)+"/"+str(epochs)+")")
                for i in range(0, int(size/N)):
                        self.optimizer.zero_grad()
                        batchX, batchY = learnX[i*N:(i*N)+N], learnY[i*N:(i*N)+N]
                        batchX = batchX.resize_(N, self.D_in)  #.to_numpy()#.resize_(N, D_in)
                        batchY = batchY.resize_(N, self.D_out)   #.to_numpy()#.resize_(N, D_out)
                        
                        y_pred = self.model(batchX)
                        

                        loss = loss_fn(y_pred, batchY)
                        
                        loss.backward()
                        def closure():
                            return loss
                        with torch.no_grad():
                            if self.optim=="lbfg":
                                self.optimizer.step(closure)
                            else:
                                self.optimizer.step()
            self.test(testX, testY)
        import numpy as np
        self.mean_accuracy = np.mean(self.accuracies)
        self.mean_precision = np.mean(self.precisions)
        self.best_accuracy = max(self.accuracies)
        self.worst_accuracy = min(self.accuracies)
        self.best_precision = max(self.precisions)
        self.worst_precision = min(self.precisions)
        self.score = (self.mean_accuracy+self.mean_precision+self.best_accuracy+self.worst_accuracy+self.best_precision+self.worst_precision)/6
        print("SCORE : "+str(self.score))
        print("MEAN ACCURACY : "+str(self.mean_accuracy))
        print("MEAN PRECISION : "+str(self.mean_precision))
        print("BEST ACCURACY : "+str( self.best_accuracy))
        print("WORST ACCURACY  : "+str(self.worst_accuracy))
        print("BEST PRECISION  : "+str(self.best_precision))
        print("WORST PRECISION : "+str(self.worst_precision))
        self.track()
        
    def track(self):
        f = open("stat","a+")
        f.write("\n\tMODEL\n")
        f.write(str(self.model))
        f.write("LEARNING RATE : "+str(self.learning_rate)+'\t')
        
        f.write("EPOCHS : "+str(self.epochs)+'\n')
        f.write("OPTIMIZER : "+str(self.optimizer)+"\n")
        f.write("SCORE : "+str(self.score)+'\n')
        f.write("MEAN ACCURACY : "+str(self.mean_accuracy)+'\n')
        f.write("MEAN PRECISION : "+str(self.mean_precision)+'\n')
        f.write("BEST ACCURACY : "+str( self.best_accuracy)+'\n')
        f.write("WORST ACCURACY  : "+str(self.worst_accuracy)+'\n')
        f.write("BEST PRECISION  : "+str(self.best_precision)+'\n')
        f.write("WORST PRECISION : "+str(self.worst_precision)+'\n\n')
            
    def save(self):
        torch.save(self.model, "../models/model-objectivity.pickle")