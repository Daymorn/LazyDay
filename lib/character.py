from py_stealth import *
from lib.unisharp import *
from datetime import datetime
import json
import math
from pathlib import Path

class character():

    def __init__(self, _charid):
        super().__init__()
        self.char = _charid
        self.status = {}
        self.party = {}
        self.tstamp = {}
        self.buffsActive = {}
        self.dicts = {}
        self.setStats()

    def __getJSON(self, _fname):
        _lazyday = Path(__file__).parent.parent.absolute()
        _jsonfile = _lazyday / 'json' / _fname
        return json.loads(_jsonfile.read_bytes())

    def setBuffs(self):
        self.buffsActive = GetBuffBarInfo()
        
    def isDamaged(self):
        if GetHP(self.char) < GetMaxHP(self.char):
            return True
        else:
            return False
            
    def isHealing(self):
        if any(_b for _b in self.buffsActive if _b['ClilocID1'] == 1151311):
            return True
        else:
            return False

    def setStats(self):
        self.status = {
            'name': GetName(self.char),
            'str': GetStr(self.char),
            'dex': GetDex(self.char),
            'int': GetInt(self.char),
            'hp': GetHP(self.char),
            'hp_max': GetMaxHP(self.char),
            'hp_per': abs(GetHP(self.char) / GetMaxHP(self.char)),
            'mana': GetMana(self.char),
            'mana_max': GetMaxMana(self.char),
            'stam': GetStam(self.char),
            'stam_max': GetMaxStam(self.char),
            'damaged': self.isDamaged(),
            'paralyzed': IsParalyzed(self.char),
            'poisoned': IsPoisoned(self.char),
            'war': IsWarMode(self.char),
            'notoriety': GetNotoriety(self.char),
            'mortal_strike': IsYellowHits(self.char),
            'dead': IsDead(self.char),
            'npc': IsNPC(self.char),
            'x': GetX(self.char),
            'y': GetY(self.char),
            'z': GetZ(self.char)
        }
        if self.char == Self():
            self.setBuffs()
            _ext = GetExtInfo()
            self.status = {**self.status, **_ext} 
            self.dicts = self.__getJSON('dicts.json')
            self.status['pets'] = PetsCurrent()
            self.status['inparty'] = InParty()
            if self.status['inparty']:
                # always start with no members
                # only add member if it exists locally
                self.party = {}
                for _m in PartyMembersList():
                    if _m != Self() and IsObjectExists(_m):
                        self.party[_m] = character(_m)

    def checkBuffs(self, _template):
        self.setStats()

        if self.char != Self():
            return
            
        self.setBuffs()
        _buffsList = self.dicts['templates'][_template]['buffs']
        for _i in _buffsList:
            _active = [_buff['ClilocID1'] for _buff in self.buffsActive]
            if self.dicts['spells'][_i]['ClilocID1'] not in _active:
                
                if 'rhand' in self.dicts['spells'][_i]['reqs'] and\
                  not ObjAtLayer(RhandLayer()):
                    continue

                if 'war' in self.dicts['spells'][_i]['reqs'] and\
                  not self.status['war']:
                    continue

                if 'peace' in self.dicts['spells'][_i]['reqs'] and\
                  self.status['war']:
                    continue

                _cost = self.dicts['spells'][_i]['mana']
                _lmc = self.status['Lower_Mana_Cost']
                if _lmc > 0:
                    _adjCost = _cost - (_cost * (_lmc/100))
                    if math.ceil(_adjCost) > self.status['mana']:
                        continue

                CastToObject(_i, Self())
                WaitForClientTargetResponse(5000);
            
    def bandageSelf(self):
        self.setStats()

        if self.isHealing():
            return
            
        BandageTypes = [0x0E21] 
        if self.status['damaged'] or\
          self.status['poisoned'] or\
          self.status['mortal_strike'] and\
          self.status['dead'] == False:
            _bandages = NewFind(BandageTypes, [0xFFFF], [Backpack()], True)
            if len(_bandages) == 0:
                AddToSystemJournal('Out of bandages...') 
                return
            else:
                AddToSystemJournal('Bandaging self...')
                UseObject(_bandages[0])
                WaitTargetSelf()  

    def bandageOther(self, _other):
        if not IsObjectExists(_other.char):
            return

        self.setStats()
        _other.setStats()

        #_other is expected as class 'character'    
        if self.isHealing():
            return
            
        _x = abs(self.status['x'] - _other.status['x'])
        _y = abs(self.status['y'] - _other.status['y'])
        if _x > 1 or _y > 1:
            #AddToSystemJournal('You are too far away to heal target...')
            return  
            
        BandageTypes = [0x0E21] 
        if _other.status['damaged'] or\
          _other.status['poisoned'] or\
          _other.status['mortal_strike'] and\
          _other.status['dead'] == False:
            _bandages = NewFind(BandageTypes, [0xFFFF], [Backpack()], True)
            if len(_bandages) == 0:
                AddToSystemJournal('Out of bandages...') 
                return
            else:
                AddToSystemJournal('Bandaging other...')
                UseObject(_bandages[0])
                WaitTargetObject(_other.char) 

    def bandageParty(self):
        self.setStats()

        if len(self.party) == 0:
            return

        if self.isHealing():
            return

        # sort party members by hit points. lowest -> greatest
        # requires python 3.6+
        _party = {k: v for k, v in sorted(self.party.items(), key=lambda item: item[1].status['hp'])}
            
        # check distance between self and each party member
        for _m in _party:
            _x = abs(self.status['x'] - _party[_m].status['x'])
            _y = abs(self.status['y'] - _party[_m].status['y'])
            # skip player if not within 1 tile
            if _x > 1 or _y > 1:
                continue  

            # Bandage 
            BandageTypes = [0x0E21] 
            if _party[_m].status['damaged'] or\
              _party[_m].status['poisoned'] or\
              _party[_m].status['mortal_strike'] and\
              _party[_m].status['dead'] == False:
                _bandages = NewFind(BandageTypes, [0xFFFF], [Backpack()], True)
                if len(_bandages) == 0:
                    AddToSystemJournal('Out of bandages...') 
                    return
                else:
                    AddToSystemJournal('Bandaging other...')
                    UseObject(_bandages[0])
                    WaitTargetObject(_party[_m].char) 
                    return


