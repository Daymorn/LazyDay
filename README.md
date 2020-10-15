# LazyDay - UO Assistant
Stealth-Client scripts to assist with repetitive spell casting and bandage healing while playing Ultima Online.

NOTE: A lot of credit goes to user Unisharp for both examples and functions that I am using.
http://www.scriptuo.com/index.php?action=profile;u=3879

I am trying to focus on game play assistance for actions that I think are more tedious than fun. 
This is a work in progress and can be extended out to cover quite a bit more.
This is particularly true for the list of spells defined and the number of character templates to choose from.
I will likely extend this more over time, otherwise please feel free to look up the ClilocIDs yourself and share.

# Installation
Download or clone LazyDay into your StealthClient scripts folder.
        cd <path to>\Stealth_v#.#.#\Scripts\
        git clone https://github.com/Daymorn/LazyDay.git

# Run
1. edit lazyday.py to what suits your needs
2. load LazyDay\lazyday.py into the Stealth Client and push play.

# Modification
# lazyday.py
        # Initialize character 
        # Required.
        char.setStats()
        
        # Check if you need to bandage yourself. 
        # Optional
        char.bandageSelf()
        
        # Uncomment if you want to bandage another player (Must be in party to see health)
        # Must replace <player objectid> with the proper id via stealth.
        # You can find this under the 'World' tab in stealth
        # Optional
        # other = character(<player objectid>) # 0x********
        # other.setStats()
        # char.bandageOther(other)
        
        # Check if need to cast desired buffs
        # Defined in json\dicts.json -> templates.'name' 
        # Currently supports: 'Death Knight', 'Paladin', 'Mage', 'Skald'
        # Optional
        char.checkBuffs('Death Knight')
        
        # Unique to the 'Treasures of the Undead Lords' event
        # Will check for 'the three' loot and auto insure them
        # Optional 
        InsureTheThree()
        
        # Millisecond interval between each cycle
        # 1000ms works well for me
        Wait(1000)   
