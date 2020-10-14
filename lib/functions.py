from py_stealth import *
from lib.unisharp import *

def InsureItem(_item):
    Wait(250)
    RequestContextMenu(Self())
    _i = 0
    for _menuItem in GetContextMenu().splitlines():
        if "Toggle Item Insurance" in _menuItem:
            SetContextMenuHook(Self(), _i)
            Wait(250)
            WaitTargetObject(_item)
            Wait(250)
            CancelMenu()
        else:
            _i += 1
            AddToSystemJournal("Couldn't find insure menu item.")
    CancelAllMenuHooks()
    CancelTarget()
    return

def InsureTheThree():
    Wait(1500)
    _lootList = NewFind([0xFFFF], [0xFFFF], [Backpack()], True)
    for _loot in _lootList:
        _tooltipRec = GetTooltipRec(_loot)
        if ClilocIDExists(_tooltipRec, 1159530) and not\
          ClilocIDExists(_tooltipRec, 1061682):
            AddToSystemJournal(f'Insuring Item: {_loot}')
            InsureItem(_loot)
    return
