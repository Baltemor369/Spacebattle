import random as rd
from Manga import Manga

LETTER = "azertyuiopmlkjhfdsqwxcvbn"

def random_manga(ID:int):
    name = ""
    for i in range(2,rd.randrange(10)):
        name += rd.choice(LETTER)
    
    author = ""
    for i in range(2,rd.randrange(10)):
        author += rd.choice(LETTER)
    
    type = ""
    for i in range(2,rd.randrange(10)):
        type += rd.choice(LETTER)
    
    volume_number = int(rd.randrange(1,100))
    
    valuation = float(rd.randrange(1,11))
        
    return Manga(ID,str(name),str(author),str(type),volume_number,"None",valuation)