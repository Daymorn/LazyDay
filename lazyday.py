from py_stealth import *
from lib.character import Character

if __name__ == '__main__':
    char = Character(Self())
    
    while True:       
        # Check if you need to bandage yourself. 
        # Optional
        char.bandageSelf()
        # Check if you need to bandage a party member. 
        # Optional
        #char.bandageParty()
        # Check if you need to bandage a pet. 
	# Pet must be guilded/green.
	# Will bandage guildmates pets as well, most damaged first.
        # Optional
        #char.bandagePets()        
 
        # Check if need to cast desired buffs
        # Defined in json\dicts.json -> templates.<name>
        # Currently supports: 'Death Knight', 'Paladin', 'Mage', 'Skald'
        #   'ProvoBard Tamer', 'PeaceBard Tamer'
        # Optional
        char.checkBuffs('Death Knight')
        
        # Millisecond interval between each cycle
        # 1000ms works well for me
        # 500ms is very responsive
        Wait(1000) 
