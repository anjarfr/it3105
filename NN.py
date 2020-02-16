import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self,nn_dim,input_dim):
        super(Model,self).__init__()
        self.input_dim=input_dim
        self.nn_dim=list(nn_dim)

    def init_network(self):
        self.hidden=[]
        for l in range(len(self.nn_dim)): #set layers based on specified dimensions
            if(l==len(self.nn_dim)-1): #if last layer
                self.last_l=nn.Linear(self.nn_dim[l-1],1) #only one feature out
            elif(l==0): #first layer
                self.first_l=nn.Linear(self.input_dim,self.nn_dim[l])
            else:
                self.hidden.append(nn.Linear(self.nn_dim[l-1],self.nn_dim[l]))

    def forward(self, state): #propagate the state through the layers and produce an output value
        input=[]
        for num in state:
            input.append(float(num)) #from state as string to state as list
        input=torch.as_tensor(input) #convert array to tensor
        output = F.relu(self.first_l(input)) #through first layer
        for layer in self.hidden:
            output=F.relu(layer(output))
        value = self.last_l(output)

        return value

    #the optimization function stochastic gradient descent
    def optimfunc(self,lr):
        optimizer=torch.optim.SGD(self.parameters(),lr)
        return optimizer.step()

    def lossfunc(self,output,target): #compute the MSE loss
        criterion=nn.MSELoss()

        return criterion(output,target)


    def update_func(self,param,e,td_err, learning_rate,grad): #updates the parameters
        e=e+grad
        return param + learning_rate*td_err*e
    def gradient(self,e,td_err,lr): #modify gradients
        with torch.no_grad():
            for p in self.parameters():

                p.grad = self.update_func(p, e, td_err, lr, p.grad)










