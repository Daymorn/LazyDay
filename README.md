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
```
        cd <path to>\Stealth_v#.#.#\Scripts\
        git clone https://github.com/Daymorn/LazyDay.git
```
# Run
1. edit lazyday.py to what suits your needs
2. load LazyDay\lazyday.py into the Stealth Client and push play.

# Modification
# lazyday.py
```
if __name__ == '__main__':
    char = character(Self())
    
    while True:       
        # Check if you need to bandage yourself. 
        # Optional
        char.bandageSelf()
        # Uncomment if you want to auto bandage party members
        # It attempts to heal the most damaged player first, if within 1 tile.
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
```
# json/dicts.json
'reqs' currently supports:
'war' 
'peace' 
'rhand' 
'self_<over|under><1-99>%hp' 
'pet_<over|under><1-99>%hp'
'party_<over|under><1-99>%hp'
```
"actions": {
	"bandage pet": {
		"reqs": [ "peace", "pet_under90%hp" ]
	},
	"bandage party": {
		"reqs": [ "party_under98%hp" ]
	}
},
...
	"curse weapon": {
		"mana": 7,
		...
		"reqs": [ "war", "rhand", "self_over50%hp" ]
	}
```
