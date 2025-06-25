from model.model import Model
from model.stato import Stato

model = Model()
model.buildGraph(2000)

for n in model.getAllNodi():
    print(n.StateNme + str(model.getNumeroVicini(n.CCode)))
print(model.getNumCompConnesse())

