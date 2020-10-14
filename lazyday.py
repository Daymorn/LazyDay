from py_stealth import *
from lib.character import character
from lib.unisharp import *
from lib.functions import *
from datetime import datetime

if __name__ == '__main__':
    char = character(Self())  

    while True:
        # Iniitalize char. 
        # Required.
        char.setStats()
        #print(char.status)
        
        # Check if you need to bandage yourself. 
        # Optional
        char.bandageSelf()
        
        # Uncomment if you want to bandage another player
        # Must replace <player id> with the proper id via stealth
        # Optional
        # char.bandageOther(<player id>)
        
        # Check if need to cast desired buffs
        # Defined in json\dicts.json -> templates.<name>
        # Optional
        char.checkBuffs('Death Knight')
        
        # Unique to the 'Treasures of the undead Lords' event
        # Will check for 'the three' loot and auto insure them
        # Optional 
        InsureTheThree()
        
        # Millisecond interval between each cycle
        # 1000ms works well for me
        Wait(1000)   
        



