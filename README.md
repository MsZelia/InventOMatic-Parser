# Script for parsing inventory dump from Invent-O-Matic Stash for Fallout 76

> [!NOTE]
> I have no previous professional experience with python, if you want optimized or clean code you can do it yourself

> [!NOTE]
> WORKS ONLY FOR ENGLISH VERSION OF GAME

### Legendary effects
- Removed effects will just show as empty string, e.g. /ss/s, v//25, //90
- Shotgun explosive effect (3% explosive) is displayed as e3, otherwise it's 20% explosive (e.g. legacy dragon)

### Armor
- TYPE and PIECE are extracted from item name - DOES NOT WORK for renamed armor pieces
- GRADE is extracted from item name (Heavy/Sturdy) and from damage/energy/radiation resistances - Combat, Leather, Metal, Raider and Robot armor

### Apparel
- Legendary effects are extracted and displayed the same way as armor effects

### Other
Displays only item name, count and item type (apparel/food/drink/aid/misc...)



## Usage
Default separator is TAB
```
InventOMatic-Parser -f filename [-s separator]
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
