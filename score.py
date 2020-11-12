import roll

def scoring(roll1, roll2):
    print(roll1)
    print(roll2)
    if roll1['name'] == "Makin' Bacon" or roll2['name'] == "Makin' Bacon":
        return {'name':"Makin' Bacon",'score':0}
    elif roll1 == roll2:
        if roll1['name'] == 'Sider (no dot)' or roll1['name'] == 'Sider (dot)':
            return {'name':'Sider','score':1}
        else:
            return {'name':f"Double {roll1['name']}",'score':roll1['score'] * 4}
    elif not roll1['score'] + roll2['score']:
        return {'name':'Pig Out','score':0}
    else:
        return {'name':f"{roll1['name']} + {roll2['name']}",'score':roll1['score'] + roll2['score']}

#scoring(pig_roll(random.randint(1,201)),pig_roll(random.randint(1,201)))
