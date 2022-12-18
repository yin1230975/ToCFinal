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

# machine = LifeNumCounterMachine(
#     states=['show_num','show_analysis','call_counsel'],
#     transitions=[
#         {'trigger' : 'advance' , 'source' : 'user' , 'dest' : 'show_num' , 'conditions' : 'is_going_to_input_birth'},
#         {'trigger' : 'advance' , 'source' : 'show_num' , 'dest' : 'show_analysis' , 'conditions' : 'is_going_to_watch_analysis'},
#         {'trigger' : 'advance' , 'source' : 'show_num' , 'dest' : 'call_counsel' , 'conditions' : 'is_going_to_call_councel'},
#         {'trigger' : 'goBack' , 
#         'source' : ['show_num','show_analysis','call_counsel'] , 
#         'dest' : 'user'}
#     ],
#     initial = 'user',
#     auto_transitions = False,
#     show_conditions = True
# )

# machine.advance()
# print(machine.state)
# machine.advance()
# print(machine.state)
# machine.goBack()
# print(machine.state)
# machine.advance()
# print(machine.state)

# machine.get_graph().draw('fsm.png', prog='dot', format='png')
