import roll

def scoring(roll1, roll2):
    if roll1['name'] == "Oinker":
        return roll1
    elif roll2['name'] == "Oinker":
        return roll2
    elif roll1 == roll2:
        if roll1['name'] == 'Sider (no dot)' or roll1['name'] == 'Sider (dot)':
            return {'name':'Sider','score':1}
        else:
            return {'name':f"Double {roll1['name']}",'score':roll1['score'] * 4}
    elif not roll1['score'] + roll2['score']:
        return {'name':'Pig Out','score':0}
    else:
        return {'name':f"{roll1['name']} + {roll2['name']}",'score':roll1['score'] + roll2['score']}

#scoring({'name':"Oinker",'score':0},{'name':"Oinker",'score':0})
