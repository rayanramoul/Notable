import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import mean_squared_error
import random 

class comrad():
    def __init__(self, representation):
        self.nbrlayers=1
        self.layers=[]
        self.score=0
        self.epochs=10
        self.representation= representation
        D_in = 1 # Input Dimension
        D_out= 1 # Output Dimension
        modules = []
        count=0
        for i in range(len(representation)):
            if count==0:
                modules.append(nn.Linear(D_in, representation[i]))
            elif count==len(representation)-1:
                modules.append(nn.Linear(representation[i-1], D_out))
            else:
                modules.append(nn.Linear(representation[i-1], representation[i]))
            count+=1
        self.model=nn.Sequential(*modules)
        self.learning_rate = 1e-4
        print("\t\tCOMRAD"+str(self.model)+"\n")
        
    def mutate(self):
        self.score=0
        rep = self.representation
        index = random.randint(len(rep))
        rep[index] = random.randint(1,200)
        self=comrad(rep)
    
    def crossover(self, comrad):
        size = random.choice(len(self.representation), len(comrad.representation))
        newrep = []
        for i in range(size):
            newrep.append(random.choice(self.representation[i], comrad.representation[i]))
        return comrad(newrep)

    def test(self, testX, testY):
        D_in = 1 # Input Dimension
        D_out= 1 # Output Dimension
        testX=testX.resize_(100000, D_in)
        testY=testY.resize_(100000, D_out)
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            fX = self.model(testX).numpy()
            fY = testY.numpy()
            self.score=mean_squared_error(fX, fY)

        print("Score : "+str(self.score))
        self.track()

    def learn(self, learnX, learnY, validationX, validationY):
        from torch.autograd import Variable

        dtype = torch.FloatTensor
        # dtype = torch.cuda.FloatTensor # Uncomment this to run on GPU
        
        D_in = 1
        D_out= 1
        N = 32 # Batch Size
        

        self.model.train()
        device = torch.device('cpu')

        size=list(learnX.shape)[0]
        loss_fn = torch.nn.MSELoss(reduction='sum')
        for t in range(self.epochs):
            print("Epoch ("+str(t)+"/"+str(self.epochs)+")")
            for i in range(0, int(size/N)):
                batchX, batchY= learnX[i*N:(i*N)+N], learnY[i*N:(i*N)+N]
                batchX=batchX.resize_(N, D_in)
                batchY=batchY.resize_(N, D_out)

                y_pred = self.model(batchX)
            

                loss = loss_fn(y_pred, batchY)

                self.model.zero_grad()
                loss.backward()

                with torch.no_grad():
                    for param in self.model.parameters():
                        param.data -= self.learning_rate * param.grad

    def track(self):
        f= open("stat","w+")
        f.write("\n\tMODEL\n")
        f.write(str(self.model))
        f.write("SCORE (MSE) : "+str(self.score)+"\n")
            
    def save(self):
        torch.save(model, "models/trained_model")