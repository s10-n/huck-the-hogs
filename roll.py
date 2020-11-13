import random

def pig_roll():
    number = random.randint(1,201)
    if number <= 70:
        return {'name':'Sider (no dot)','score':0}
    elif number > 70 and number <= 130:
        return {'name':'Sider (dot)','score':0}
    elif number > 130 and number <= 174:
        return {'name':'Razorback','score':5}
    elif number > 174 and number <= 192:
        return {'name':'Trotter','score':5}
    elif number > 192 and number <= 197:
        return {'name':'Snouter','score':10}
    elif number > 198 and number <= 199:
        return {'name':"Makin' Bacon",'score':0}
    elif number == 200:
        return {'name':'Jowler','score':15}
        
#for i in range(2):
    #print(pig_roll(random.randint(1,201)))
