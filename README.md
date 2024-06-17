# Script for parsing inventory dump from Invent-O-Matic Stash for Fallout 76

[View on NexusMods](https://www.nexusmods.com/fallout76/mods/2285)

> [!NOTE]
> I have no previous professional experience with python, if you want optimized or clean code you are free to do it yourself

> [!IMPORTANT]
> Currently there is only translation for ENGLISH, SPANISH and POLISH version, other versions need translating

### Legendary effects
- Removed effects will just show as empty string, e.g. /ss/s, v//25, //90
- Shotgun explosive effect (3% explosive) is displayed as e3, otherwise it's 20% explosive (e.g. legacy dragon)

### Armor
- TYPE and PIECE are extracted from item name - DOES NOT WORK for renamed armor pieces
- GRADE is extracted from item name (Heavy/Sturdy) and from damage/energy/radiation resistances - Combat, Leather, Metal, Raider and Robot armor
  - if unable to detect, resistances will be displayed in format dr/er/rr

### Apparel
- Legendary effects are extracted and displayed the same way as armor effects

### Other
- Displays only item name, count and item type (apparel/food/drink/aid/misc...)

### Price checking [-pc]
- Uses [fed76.info/pricing](https://fed76.info/pricing) for price checking, pass -pc argument
- Significantly increases processing time (100-200ms or more per item), could take few minutes for large lists


## Usage
```
InventOMatic-Parser -h

InventOMatic-Parser -f filename [-s separator='\t'] [-l language='en'] [-e encoding='utf8'] [-pc]
```

Print to new file
```
InventOMatic-Parser. -f filename > output.txt
```

Append to the end of existing file
```
InventOMatic-Parser.py -f filename >> output.txt
```

### Invent O Matic Stash
https://www.nexusmods.com/fallout76/mods/698


### Invent O Matic Stash (Unofficial) Update for latest game version
https://www.nexusmods.com/fallout76/mods/2335
