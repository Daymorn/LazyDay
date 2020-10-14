# LazyDay - UO Assistant
Stealth-Client scripts to assist with repetitive spell casting and bandage healing while playing Ultima Online.

# NOTE: This is a work in progress, and I hope to add more content eventually.
# This is particularly true for the list of spells defined and the number of character templates to choose from.
# Otherwise, get to it and look up the ClilocIDs yourself.

# Installation
# Download or clone LazyDay into your StealthClient scripts folder.
# cd <path to>\Stealth_v*.*.*\Scripts\
git clone https://github.com/Daymorn/LazyDay.git

# Run
# 1. edit lazyday.py to what suits your needs
# 2. load LazyDay\lazyday.py into the Stealth Client and push play.

# Modification
# lazyday.py
        # Initialize character 
        # Required.
        char.setStats()
        
        # Check if you need to bandage yourself. 
        # Optional
        char.bandageSelf()
        
        # Uncomment if you want to bandage another player
        # Must replace <player id> with the proper id via stealth
        # Optional
        # char.bandageOther(<player id>)
        
        # Check if need to cast desired buffs
        # Defined in json\dicts.json -> templates.<name>
	# Currently supports: 'Death Knight', 'Paladin', 'Mage', 'Skald'
        # Optional
        char.checkBuffs('Death Knight')
        
        # Unique to the 'Treasures of the undead Lords' event
        # Will check for 'the three' loot and auto insure them
        # Optional 
        InsureTheThree()
        
        # Millisecond interval between each cycle
        # 1000ms works well for me
        Wait(1000)   
