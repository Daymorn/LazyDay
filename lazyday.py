from py_stealth import *
from lib.character import character
from lib.unisharp import *
from lib.functions import *
from datetime import datetime

if __name__ == '__main__':
    char = character(Self())
    
    while True:
        # Initialize character 
        # Required.
        char.setStats()
        
        # Check if you need to bandage yourself. 
        # Optional
        char.bandageSelf()
        
        # Uncomment if you want to bandage another player
        # Must replace <player objectid> with the proper id via stealth
        # You can find this under the 'World' tab in stealth
        # Optional
        # other = character(<player objectid>) # 0x********
        # other.setStats()
        # char.bandageOther(other)
        
        # Check if need to cast desired buffs
        # Defined in json\dicts.json -> templates.<name>
        # Currently supports: 'Death Knight', 'Paladin', 'Mage', 'Skald'
        #   'ProvoBard Tamer', 'PeaceBard Tamer'
        # Optional
        char.checkBuffs('Death Knight')
        
        # Unique to the 'Treasures of the Undead Lords' event
        # Will check for 'the three' loot and auto insure them
        # Optional 
        InsureTheThree()
        
        # Millisecond interval between each cycle
        # 1000ms works well for me
        Wait(1000) 
