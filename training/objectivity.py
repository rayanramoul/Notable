import numpy as np # linear algebra
import pandas as pd 
import pickle

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

file = pd.read_excel("../datasets/SportsArticles/features.xlsx")
file.dropna()
#print(str(file.head()))

# Get columns names
#print(str(list(file)))


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



X_train, X_test, Y_train, Y_test = train_test_split(inputs, output, test_size=0.33)
X_train = torch.tensor(X_train.to_numpy())
Y_train = torch.tensor(Y_train.to_numpy())
X_train = X_train.to(device=device, dtype=torch.int64).type(torch.FloatTensor)
Y_train = Y_train.to(device=device, dtype=torch.int64).type(torch.FloatTensor)

X_test = torch.tensor(X_test.to_numpy())
Y_test = torch.tensor(Y_test.to_numpy())
X_test = X_test.to(device=device, dtype=torch.float32).type(torch.FloatTensor)
Y_test = Y_test.to(device=device, dtype=torch.float32).type(torch.FloatTensor)

print("Training ")


D_in = len(list(inputs))# Input Dimension
D_out= 1
print(" input dim :"+str(D_in)+" output dim : "+str(D_out))
modules = []
count=0
representation = [100,100,100,100]
for i in range(len(representation)):
            if count==0:
                modules.append(nn.Linear(D_in, representation[i]))
                modules.append(nn.ReLU())
            elif count==len(representation)-1:
                modules.append(nn.Linear(representation[i-1], D_out))
                modules.append(nn.Sigmoid())
            else:
                modules.append(nn.Linear(representation[i-1], representation[i]))
                modules.append(nn.ReLU())
            count+=1
model = nn.Sequential(*modules)
learning_rate = 1e-4

N = 32 # Batch Size
epochs = 1000

model.train()


size = list(X_train.shape)[0]
loss_fn = torch.nn.MSELoss(reduction='sum')
for t in range(epochs):
    print("Epoch ("+str(t+1)+"/"+str(epochs)+")")
    for i in range(0, int(size/N)):
            batchX, batchY = X_train[i*N:(i*N)+N], Y_train[i*N:(i*N)+N]
            batchX = batchX.resize_(N, D_in)  #.to_numpy()#.resize_(N, D_in)
            batchY = batchY.resize_(N, D_out)   #.to_numpy()#.resize_(N, D_out)
            
            y_pred = model(batchX)
            

            loss = loss_fn(y_pred, batchY)
            if t==0:
                print("Loss : "+str(loss))
            model.zero_grad()
            loss.backward()

            with torch.no_grad():
                for param in model.parameters():
                    param.data -= learning_rate * param.grad


model.eval()


from sklearn.metrics import accuracy_score
with torch.no_grad():
    y_pred = torch.round(model(X_test))
    #print("Results : "+str(set(list(y_pred))))
    result = accuracy_score(Y_test, y_pred)

    print("Accuracy : "+str(result))
pickle.dump(model, open("./models/model-objectivity.pickle", "wb"))