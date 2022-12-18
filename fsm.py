from transitions.extensions import GraphMachine
from transitions import Machine

class LifeNumCounterMachine(GraphMachine):

    def __init__(self,**machine_configs):
        self.machine = GraphMachine(model=self,**machine_configs)
        self.lifeNum = 0
    def look_life_num(self,event):
        return True

    def is_going_to_watch_analysis(self,event):
        get_message = event.message.text
        for i in range(10):
            if(i == 4 or i == 7):
                continue
            self.lifeNum = self.lifeNum+int(get_message[i])
        print(self.lifeNum)
        return True

