from py_stealth import *
from lib.unisharp import *
from datetime import datetime
import json
import math
from pathlib import Path
import re

class character():

    def __init__(self, _charid):
        super().__init__()
        self.char = _charid
        self.status = {}
        self.party = {}
        self.pets = {}
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
        # checks if healing skill or veterinary 'buff' is active.
        if any(_b for _b in self.buffsActive \
          if _b['ClilocID1'] == 1151311\
          or _b['ClilocID1'] == 1044099):
            return True
        else:
            return False

    def __setHPPercent(self):
        if GetHP(self.char) > 0 and\
          GetMaxHP(self.char) > 0:
            return round(GetHP(self.char) / GetMaxHP(self.char), 2)
        else:
            return 0

    def __reqCheck(self, _condition, _target=False):
        if _condition == 'rhand':
            if not ObjAtLayer(RhandLayer()):
                return False

        if _condition == 'war':
            if not self.status['war']:
                return False

        if _condition == 'peace':
            if self.status['war']:
                return False
        
        if _condition == 'undamaged':
            if self.status['damaged']:
                return False

        # self less than % hp check
        _r = re.search(r'(?<=self_under)[0-9]+(?=\%hp)', _condition)
        if _r:
            _per = float(_r.group(0)) / 100
            if not self.status['hp_per'] < _per:
                return False
        
        # self more than % hp check
        _r = re.search(r'(?<=self_over)[0-9]+(?=\%hp)', _condition)
        if _r:
            _per = float(_r.group(0)) / 100
            if not self.status['hp_per'] > _per:
                return False

        # pet less than % hp check
        _r = re.search(r'(?<=pet_under)[0-9]+(?=\%hp)', _condition)
        if _r:
            _per = float(_r.group(0)) / 100
            if not self.pets[_target].status['hp_per'] < _per:
                return False
 
        # pet more than % hp check
        _r = re.search(r'(?<=pet_over)[0-9]+(?=\%hp)', _condition)
        if _r:
            _per = float(_r.group(0)) / 100
            if not self.pets[_target].status['hp_per'] > _per:
                return False
 
        # party less than % hp check
        _r = re.search(r'(?<=party_under)[0-9]+(?=\%hp)', _condition)
        if _r:
            _per = float(_r.group(0)) / 100
            if not self.party[_target].status['hp_per'] < _per:
                return False
 
        # party more than % hp check
        _r = re.search(r'(?<=party_over)[0-9]+(?=\%hp)', _condition)
        if _r:
            _per = float(_r.group(0)) / 100
            if not self.party[_target].status['hp_per'] > _per:
                return False
       
        return True

    def __lmcCheck(self, _spell):
        _cost = self.dicts['spells'][_spell]['mana']
        _lmc = self.status['Lower_Mana_Cost']
        if _lmc > 0:
            _adjCost = _cost - (_cost * (_lmc/100))
            if math.ceil(_adjCost) > self.status['mana']:
                return False

        return True

    def setStats(self):
        self.status = {
            'name': GetName(self.char),
            'str': GetStr(self.char),
            'dex': GetDex(self.char),
            'int': GetInt(self.char),
            'hp': GetHP(self.char),
            'hp_max': GetMaxHP(self.char),
            'hp_per': self.__setHPPercent(),
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
            self.status['pet_count'] = PetsCurrent()
            self.status['inparty'] = InParty()

            if self.status['pet_count'] > 0:
                # always start with no pets
                # only add pet if it exists locally
                self.pets = {}
                
                Ignore(Self())
                FindNotoriety(-1,2)
                _guilded = GetFoundList()
                for _g in _guilded:
                    if GetType(_g) not in self.dicts['player_types']:
                        self.pets[_g] = character(_g)

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
                _cast = True

                # Check if each condition of this spell is met.
                if len(self.dicts['spells'][_i]['reqs']) > 0:
                    for _req in self.dicts['spells'][_i]['reqs']:
                        if not self.__reqCheck(_req):
                            _cast = False 

                # Check if char has enough mana, after LMC adjustment
                if not self.__lmcCheck(_i):
                    _cast = False

                if _cast:
                    CastToObject(_i, Self())
                    WaitForClientTargetResponse(5000);

    def applyBandage(self, _target):
        BandageTypes = [0x0E21] 
        if _target.status['damaged'] or\
          _target.status['poisoned'] or\
          _target.status['mortal_strike'] and\
          _target.status['dead'] == False:
            _bandages = NewFind(BandageTypes, [0xFFFF], [Backpack()], True)
            if len(_bandages) == 0:
                AddToSystemJournal('Out of bandages...') 
                return
            else:
                AddToSystemJournal('Bandaging other...')
                UseObject(_bandages[0])
                WaitTargetObject(_target.char) 
                return

    def bandageSelf(self):
        self.setStats()

        if self.isHealing():
            return
            
        self.applyBandage(self)

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

            _bandage = True 
            for _req in self.dicts['actions']['bandage party']['reqs']:
                if not self.__reqCheck(_req, _m):
                    _bandage = False 

            if _bandage:
                self.applyBandage(_party[_m])

    def bandagePets(self):
        self.setStats()

        if len(self.pets) == 0:
            return

        if self.isHealing():
            return

        # sort pets by hit points. lowest -> greatest
        # requires python 3.6+
        _pets = {k: v for k, v in sorted(self.pets.items(), key=lambda item: item[1].status['hp'])}
            
        # check distance between self and each party member
        for _p in _pets:
            _x = abs(self.status['x'] - _pets[_p].status['x'])
            _y = abs(self.status['y'] - _pets[_p].status['y'])
            # skip pet if not within 1 tile
            if _x > 1 or _y > 1:
                continue  

            _bandage = True 
            for _req in self.dicts['actions']['bandage pet']['reqs']:
                if not self.__reqCheck(_req, _p):
                    _bandage = False 

            if _bandage:
                self.applyBandage(_pets[_p])
