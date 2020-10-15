from py_stealth import *
from lib.unisharp import *
from datetime import datetime
import json
import math

class character():

    def __init__(self, _charid):
        super().__init__()
        self.char = _charid
        self.status = {}
        self.tstamp = {}
        self.buffsActive = {}
        self.dicts = self.jsonLoad(r'''..\Scripts\LazyDay\json\dicts.json''')
    
    def jsonLoad(self, _file):
        with open(_file, 'r') as f:
            _data = f.read()
            return json.loads(_data)

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

    def checkBuffs(self, _template):
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

                _cost = self.dicts['spells'][_i]['mana']
                _lmc = self.status['Lower_Mana_Cost']
                if _lmc > 0:
                    _adjCost = _cost - (_cost * (_lmc/100))
                    if math.ceil(_adjCost) > self.status['mana']:
                        continue

                CastToObject(_i, Self())
                WaitForClientTargetResponse(5000);
            
    def bandageSelf(self):
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
