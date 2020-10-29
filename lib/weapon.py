from py_stealth import *
from datetime import datetime
import json
from json import JSONEncoder
import math
from pathlib import Path


class Weapon:

    def __init__(self, _id):
        super().__init__()
        self.ID = _id
        self.Tooltip = GetTooltip(_id)
        self.TooltipRec = GetTooltipRec(_id)
        self.ItemName = self.Tooltip.split('|')[0]
        self.Brittle = self.ClilocIDExists(1116209)
        self.Antique = self.ClilocIDExists(1152714)
        self.Cursed = self.ClilocIDExists(1049643)
        self.Splintering = self.GetParam(1112857)
        self.HitLowerAttack = self.GetParam(1060424)
        self.HitLowerDefense = self.GetParam(1060425)
        self.HitSpell = self.CalcHitSpell()
        self.HitArea = self.CalcHitArea()
        self.HitLeech = self.CalcHitLeech()
        self.SpellChanneling = self.ClilocIDExists(1060482)
        self.Balanced = self.ClilocIDExists(1072792)
        self.UseBestWeaponSkill = self.ClilocIDExists(1060400)
        self.MageWeapon = self.GetParam(1060438)
        self.BloodDrinker = self.ClilocIDExists(1113591)
        self.Velocity = self.GetParam(1072793)
        self.BattleLust = self.ClilocIDExists(1113710)
        self.DI = self.GetParam(1060402)
        self.SSI = self.GetParam(1060486)
        self.FC = self.GetParam(1060413)
        self.FCR = self.GetParam(1060412)
        self.LMC = self.GetParam(1060433)
        self.LRC = self.GetParam(1060434)
        self.SDI = self.GetParam(1060483)
        self.RPD = self.GetParam(1060442)
        self.DCI = self.GetParam(1060408)
        self.HCI = self.GetParam(1060415)
        self.Strength = self.GetParam(1060485)
        self.Dexterity = self.GetParam(1060409)
        self.Intelligence = self.GetParam(1060432)
        self.HitPointBonus = self.GetParam(1060431)
        self.StaminaBonus = self.GetParam(1060484)
        self.ManaBonus = self.GetParam(1060439)
        self.HitPointRegen = self.GetParam(1060444)
        self.StaminaRegen = self.GetParam(1060443)
        self.ManaRegen = self.GetParam(1060440)
        self.EnhancePotions = self.GetParam(1060411)
        self.Luck = self.GetParam(1060436)
        self.WeaponType = GetType(_id)
        self.ElementalDamage = self.CalcElementalDamage()
        # self.SkillType = GetParam(self.ToolTipRec, 1112857)

    def GetParam(self, _clilocID):
        for _tooltip in self.TooltipRec:
            if _tooltip['Cliloc_ID'] == _clilocID:
                return int(_tooltip['Params'][0])
        return 0

    def ClilocIDExists(self, _clilocID):
        for _tooltip in self.TooltipRec:
            if _tooltip['Cliloc_ID'] == _clilocID:
                return True
        return False

    def CalcHitLeech(self):
        _hitLeech = ""
        if self.ClilocIDExists(1060422):
            _hitLeech += f"Hit Life Leech: {self.GetParam(1060422)}, "
        if self.ClilocIDExists(1060430):
            _hitLeech += f"Hit Stamina Leech: {self.GetParam(1060430)}, "
        if self.ClilocIDExists(1060427):
            _hitLeech += f"Hit Mana Leech: {self.GetParam(1060427)}"
        return _hitLeech.strip(", ")

    def CalcHitArea(self):
        _hitArea = ""
        if self.ClilocIDExists(1060416):
            _hitArea += f"Hit Cold Area: {self.GetParam(1060416)}, "
        if self.ClilocIDExists(1060418):
            _hitArea += f"Hit Energy Area: {self.GetParam(1060418)}, "
        if self.ClilocIDExists(1060419):
            _hitArea += f"Hit Fire Area: {self.GetParam(1060419)}, "
        if self.ClilocIDExists(1060428):
            _hitArea += f"Hit Physical Area: {self.GetParam(1060428)}"
        return _hitArea.strip(", ")

    def CalcHitSpell(self):
        _hitSpell = ""
        if self.ClilocIDExists(1113699):
            _hitSpell += f"Hit Mana Drain: {self.GetParam(1113699)}, "
        if self.ClilocIDExists(1113712):
            _hitSpell += f"Hit Curse: {self.GetParam(1113712)}, "
        if self.ClilocIDExists(1113700):
            _hitSpell += f"Hit Fatigue: {self.GetParam(1113700)}, "
        if self.ClilocIDExists(1060421):
            _hitSpell += f"Hit Harm: {self.GetParam(1060421)}, "
        if self.ClilocIDExists(1060417):
            _hitSpell += f"Hit Dispel: {self.GetParam(1060417)}, "
        if self.ClilocIDExists(1060423):
            _hitSpell += f"Hit Lightning: {self.GetParam(1060423)}, "
        if self.ClilocIDExists(1060420):
            _hitSpell += f"Hit Fireball: {self.GetParam(1060420)}, "
        if self.ClilocIDExists(1060426):
            _hitSpell += f"Hit Magic Arrow: {self.GetParam(1060426)}"
        return _hitSpell.strip(", ")

    def CalcElementalDamage(self):
        _elementalDamage = ""
        if self.ClilocIDExists(1060403):
            _elementalDamage += f"Physical Damage {self.GetParam(1060403)} "
        if self.ClilocIDExists(1060404):
            _elementalDamage += f"Fire Damage {self.GetParam(1060404)} "
        if self.ClilocIDExists(1060405):
            _elementalDamage += f"Cold  Damage {self.GetParam(1060405)} "
        if self.ClilocIDExists(1060406):
            _elementalDamage += f"Poison  Damage {self.GetParam(1060406)} "
        if self.ClilocIDExists(1060407):
            _elementalDamage += f"Energy  Damage {self.GetParam(1060407)} "
        return _elementalDamage

    def Encoder(self):
        return {
            "ID": str(self.ID),
            "Name": self.ItemName,
            "Brittle": str(self.Brittle),
            "Antique": str(self.Antique),
            "Cursed": str(self.Cursed),
            "ElementalDamage": str(self.ElementalDamage),
            "Splintering": str(self.Splintering),
            "HitLowerAttack": str(self.HitLowerAttack),
            "HitLowerDefense": str(self.HitLowerDefense),
            "HitSpell": str(self.HitSpell),
            "HitArea": str(self.HitArea),
            "HitLeech": str(self.HitLeech),
            "SpellChanneling": str(self.SpellChanneling),
            "Balanced": str(self.Balanced),
            "UseBestWeaponSkill": str(self.UseBestWeaponSkill),
            "MageWeapon": str(self.MageWeapon),
            "BloodDrinker": str(self.BloodDrinker),
            "Velocity": str(self.Velocity),
            "BattleLust": str(self.BattleLust),
            "DCI": str(self.DCI),
            "HCI": str(self.HCI),
            "DI": str(self.DI),
            "SSI": str(self.SSI),
            "FC": str(self.FC),
            "FCR": str(self.FCR),
            "LMC": str(self.LMC),
            "LRC": str(self.LRC),
            "SDI": str(self.SDI),
            "RPD": str(self.RPD),
            "Strength": str(self.Strength),
            "Intelligence": str(self.Intelligence),
            "HitPointBonus": str(self.HitPointBonus),
            "StaminaBonus": str(self.StaminaBonus),
            "ManaBonus": str(self.ManaBonus),
            "HitPointRegen": str(self.HitPointRegen),
            "StaminaRegen": str(self.StaminaRegen),
            "ManaRegen": str(self.ManaRegen),
            "EnhancePotions": str(self.EnhancePotions),
            "Luck": str(self.Luck),
            "WeaponType": str(self.WeaponType)
        }
