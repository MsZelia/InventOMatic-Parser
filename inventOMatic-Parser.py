import sys
import asyncio
import aiohttp
import json
import time
import argparse
import numbers
from os.path import exists, getmtime
import pandas as pd

start_time = time.time()


graded_armor = {
    "COMBAT": {
        "CHEST": {
            "DEFAULT": {
                "50": {
                    "36/36/0": "LIGHT",
                    "47/47/0": "STURDY",
                    "61/61/0": "HEAVY"},
                "40": {
                    "30/30/0": "LIGHT",
                    "40/40/0": "STURDY",
                    "52/52/0": "HEAVY"},
                "30": {
                    "25/25/0": "LIGHT",
                    "33/33/0": "STURDY",
                    "43/43/0": "HEAVY"},
                "20": {
                    "16/16/0": "LIGHT",
                    "21/21/0": "STURDY",
                    "27/27/0": "HEAVY"}
                },
            "REINFORCED":{
                "50":[10,10,0],
                "40":[8,8,0],
                "30":[6,6,0],
                "20":[4,4,0]
                },
            "SHADOWED":{
                "50":[10,10,0],
                "40":[8,8,0],
                "30":[6,6,0],
                "20":[4,4,0]
                },
            "FIBERGLASS":{
                "50":[15,15,0],
                "40":[12,12,0],
                "30":[9,9,0],
                "20":[7,7,0]
                },
            "POLYMER":{
                "50":[20,20,0],
                "40":[16,16,0],
                "30":[13,13,0],
                "20":[9,9,0]
                },
            "BOS":{
                "50":[25,25,0],
                "40":[20,20,0],
                "30":[16,16,0],
                "20":[12,12,0]
                }
            },
        "LIMB": {
            "DEFAULT": {
                "50": {
                    "12/12/0": "LIGHT",
                    "15/15/0": "STURDY",
                    "20/20/0": "HEAVY"},
                "40": {
                    "10/10/0": "LIGHT",
                    "13/13/0": "STURDY",
                    "17/17/0": "HEAVY"},
                "30": {
                    "8/8/0": "LIGHT",
                    "11/11/0": "STURDY",
                    "14/14/0": "HEAVY"},
                "20": {
                    "6/6/0": "LIGHT",
                    "8/8/0": "STURDY",
                    "11/11/0": "HEAVY"}
                },
            "REINFORCED":{
                "50":[7,7,0],
                "40":[5,5,0],
                "30":[4,4,0],
                "20":[3,3,0]
                },
            "SHADOWED":{
                "50":[7,7,0],
                "40":[5,5,0],
                "30":[4,4,0],
                "20":[3,3,0]
                },
            "FIBERGLASS":{
                "50":[10,10,0],
                "40":[8,8,0],
                "30":[6,6,0],
                "20":[5,5,0]
                },
            "POLYMER":{
                "50":[13,13,0],
                "40":[10,10,0],
                "30":[8,8,0],
                "20":[6,6,0],
                },
            "BOS":{
                "50":[15,25,0],
                "40":[12,20,0],
                "30":[10,16,0],
                "20":[8,12,0]
                }
            }
    },
    "LEATHER": {
        "CHEST": {
            "DEFAULT": {
                "50": {
                    "16/45/0": "LIGHT",
                    "21/59/0": "STURDY",
                    "28/76/0": "HEAVY"},
                "40": {
                    "14/40/0": "LIGHT",
                    "18/52/0": "STURDY",
                    "24/67/0": "HEAVY"},
                "30": {
                    "12/35/0": "LIGHT",
                    "16/45/0": "STURDY",
                    "21/58/0": "HEAVY"},
                "20": {
                    "10/30/0": "LIGHT",
                    "13/39/0": "STURDY",
                    "17/50/0": "HEAVY"},
                "10": {
                    "8/25/0": "LIGHT",
                    "11/32/0": "STURDY",
                    "15/41/0": "HEAVY"},
                "5": {
                    "6/15/0": "LIGHT",
                    "8/20/0": "STURDY",
                    "11/26/0": "HEAVY"},
                "1": {
                    "4/10/0": "LIGHT",
                    "5/13/0": "STURDY",
                    "7/17/0": "HEAVY"},
                },
            "BOILED":{
                "50":[5,15,0],
                "40":[4,12,0],
                "30":[3,9,0],
                "20":[2,6,0],
                "10":[1,3,0],
                "5":[1,2,0],
                "1":[1,1,0]},
            "SHADOWED":{
                "50":[5,15,0],
                "40":[4,12,0],
                "30":[3,9,0],
                "20":[2,6,0],
                "10":[1,3,0],
                "5":[1,2,0],
                "1":[1,1,0]},
            "GIRDED":{
                "50":[10,20,0],
                "40":[8,16,0],
                "30":[6,12,0],
                "20":[4,8,0],
                "10":[2,5,0],
                "5":[1,3,0],
                "1":[1,2,0]},
            "TREATED":{
                "50":[15,25,0],
                "40":[12,20,0],
                "30":[9,16,0],
                "20":[6,11,0],
                "10":[3,7,0],
                "5":[2,4,0],
                "1":[1,3,0]},
            "STUDDED":{
                "50":[20,30,0],
                "40":[16,24,0],
                "30":[12,19,0],
                "20":[8,14,0],
                "10":[4,8,0],
                "5":[2,6,0],
                "1":[1,4,0]}
            },
        "LIMB": {
            "DEFAULT": {
                "50": {
                    "11/21/0": "LIGHT",
                    "17/36/0": "STURDY",
                    "22/47/0": "HEAVY"},
                "40": {
                    "9/17/0": "LIGHT",
                    "14/30/0": "STURDY",
                    "19/39/0": "HEAVY"},
                "30": {
                    "7/13/0": "LIGHT",
                    "11/24/0": "STURDY",
                    "15/31/0": "HEAVY"},
                "20": {
                    "5/9/0": "LIGHT",
                    "8/17/0": "STURDY",
                    "11/22/0": "HEAVY"},
                "10": {
                    "3/5/0": "LIGHT",
                    "5/11/0": "STURDY",
                    "7/14/0": "HEAVY"},
                "5": {
                    "2/4/0": "LIGHT",
                    "3/7/0": "STURDY",
                    "4/9/0": "HEAVY"},
                "1": {
                    "1/2/0": "LIGHT",
                    "2/4/0": "STURDY",
                    "3/6/0": "HEAVY"},
                },
            "BOILED":{
                "50":[1,10,0],
                "40":[1,8,0],
                "30":[1,6,0],
                "20":[1,4,0],
                "10":[1,2,0],
                "5":[1,1,0],
                "1":[1,1,0]},
            "SHADOWED":{
                "50":[1,10,0],
                "40":[1,8,0],
                "30":[1,6,0],
                "20":[1,4,0],
                "10":[1,2,0],
                "5":[1,1,0],
                "1":[1,1,0]},
            "GIRDED":{
                "50":[5,13,0],
                "40":[4,10,0],
                "30":[3,8,0],
                "20":[2,6,0],
                "10":[1,4,0],
                "5":[1,2,0],
                "1":[1,2,0]},
            "TREATED":{
                "50":[8,16,0],
                "40":[6,13,0],
                "30":[5,10,0],
                "20":[3,8,0],
                "10":[2,5,0],
                "5":[1,4,0],
                "1":[1,3,0]},
            "STUDDED":{
                "50":[10,30,0],
                "40":[8,24,0],
                "30":[6,19,0],
                "20":[4,14,0],
                "10":[2,8,0],
                "5":[1,6,0],
                "1":[1,4,0]}
            }
    },
    "METAL": {
        "CHEST": {
            "DEFAULT": {
                "50": {
                    "51/11/0": "LIGHT",
                    "67/13/0": "STURDY",
                    "87/14/0": "HEAVY"},
                "40": {
                    "42/9/0": "LIGHT",
                    "55/11/0": "STURDY",
                    "72/12/0": "HEAVY"},
                "30": {
                    "33/7/0": "LIGHT",
                    "43/9/0": "STURDY",
                    "56/10/0": "HEAVY"},
                "20": {
                    "24/5/0": "LIGHT",
                    "32/7/0": "STURDY",
                    "42/7/0": "HEAVY"},
                "10": {
                    "20/3/0": "LIGHT",
                    "26/4/0": "STURDY",
                    "34/4/0": "HEAVY"}
            },
            "PAINTED":{
                "50":[15,3,0],
                "40":[12,2,0],
                "30":[10,2,0],
                "20":[8,1,0],
                "10":[6,1,0]
            },
            "ENAMELED":{
                "50":[20,4,0],
                "40":[17,3,0],
                "30":[14,2,0],
                "20":[11,2,0],
                "10":[8,1,0]
            },
            "SHADOWED":{
                "50":[15,3,0],
                "40":[12,2,0],
                "30":[10,2,0],
                "20":[8,1,0],
                "10":[6,1,0]
            },
            "ALLOYED":{
                "50":[25,20,0],
                "40":[21,16,0],
                "30":[17,13,0],
                "20":[13,9,0],
                "10":[10,6,0]
            },
            "POLISHED":{
                "50":[30,6,0],
                "40":[25,5,0],
                "30":[21,4,0],
                "20":[16,3,0],
                "10":[12,2,0]
            },
		},
        "LIMB": {
            "DEFAULT": {
                "50": {
                    "20/5/0": "LIGHT",
                    "26/6/0": "STURDY",
                    "34/8/0": "HEAVY"},
                "40": {
                    "18/4/0": "LIGHT",
                    "24/5/0": "STURDY",
                    "32/7/0": "HEAVY"},
                "30": {
                    "16/3/0": "LIGHT",
                    "21/4/0": "STURDY",
                    "27/6/0": "HEAVY"},
                "20": {
                    "12/2/0": "LIGHT",
                    "16/3/0": "STURDY",
                    "20/4/0": "HEAVY"},
                "10": {
                    "8/1/0": "LIGHT",
                    "11/2/0": "STURDY",
                    "14/3/0": "HEAVY"}
                },
            "PAINTED":{
                "50":[10,1,0],
                "40":[8,1,0],
                "30":[6,1,0],
                "20":[5,1,0],
                "10":[3,1,0]
            },
            "ENAMELED":{
                "50":[13,2,0],
                "40":[10,1,0],
                "30":[8,1,0],
                "20":[6,1,0],
                "10":[4,1,0]
            },
            "SHADOWED":{
                "50":[10,1,0],
                "40":[8,1,0],
                "30":[6,1,0],
                "20":[5,1,0],
                "10":[3,1,0]
            },
            "ALLOYED":{
                "50":[15,3,0],
                "40":[12,2,0],
                "30":[10,2,0],
                "20":[8,1,0],
                "10":[6,1,0]
            },
            "POLISHED":{
                "50":[20,4,0],
                "40":[16,3,0],
                "30":[13,2,0],
                "20":[10,2,0],
                "10":[7,1,0]
            }
		}
	},
    "RAIDER": {
        "CHEST": {
            "DEFAULT": {
                "45": {
                    "42/15/0": "LIGHT",
                    "54/19/0": "STURDY",
                    "70/24/0": "HEAVY"},
                "35": {
                    "34/12/0": "LIGHT",
                    "44/15/0": "STURDY",
                    "57/19/0": "HEAVY"},
                "25": {
                    "26/9/0": "LIGHT",
                    "34/11/0": "STURDY",
                    "44/14/0": "HEAVY"},
                "15": {
                    "18/6/0": "LIGHT",
                    "24/8/0": "STURDY",
                    "32/11/0": "HEAVY"},
                "5": {
                    "10/4/0": "LIGHT",
                    "13/6/0": "STURDY",
                    "17/8/0": "HEAVY"},
                },
            "WELDED":{
                "45":[11,5,0],
                "35":[9,4,0],
                "25":[7,3,0],
                "15":[5,2,0],
                "5":[3,1,0]
			},
            "TEMPERED":{
                "45":[14,13,0],
                "35":[12,11,0],
                "25":[9,8,0],
                "15":[7,5,0],
                "5":[4,3,0]
			},
            "HARDENED":{
                "45":[18,9,0],
                "35":[15,7,0],
                "25":[12,6,0],
                "15":[9,5,0],
                "5":[6,3,0]
			},
            "BUTTRESSED":{
                "45":[23,11,0],
                "35":[19,9,0],
                "25":[15,7,0],
                "15":[11,6,0],
                "5":[7,4,0]
			}
		},
        "LIMB": {
            "DEFAULT": {
                "45": {
                    "17/8/0": "LIGHT",
                    "22/10/0": "STURDY",
                    "28/13/0": "HEAVY"},
                "35": {
                    "14/7/0": "LIGHT",
                    "18/9/0": "STURDY",
                    "23/11/0": "HEAVY"},
                "25": {
                    "11/4/0": "LIGHT",
                    "14/6/0": "STURDY",
                    "18/8/0": "HEAVY"},
                "15": {
                    "8/3/0": "LIGHT",
                    "10/5/0": "STURDY",
                    "13/6/0": "HEAVY"},
                "5": {
                    "5/2/0": "LIGHT",
                    "7/3/0": "STURDY",
                    "9/4/0": "HEAVY"},
                },
            "WELDED":{
                "45":[9,4,0],
                "35":[7,3,0],
                "25":[5,2,0],
                "15":[3,2,0],
                "5":[1,1,0]
			},
            "TEMPERED":{
                "45":[10,5,0],
                "35":[8,4,0],
                "25":[6,3,0],
                "15":[4,3,0],
                "5":[2,2,0]
			},
            "HARDENED":{
                "45":[11,6,0],
                "35":[9,5,0],
                "25":[7,4,0],
                "15":[5,4,0],
                "5":[3,3,0]
			},
            "BUTTRESSED":{
                "45":[12,7,0],
                "35":[10,6,0],
                "25":[8,5,0],
                "15":[6,5,0],
                "5":[4,4,0]
			}
		}
	},
    "ROBOT": {
        "CHEST": {
            "DEFAULT": {
                "50": {
                    "24/24/13": "LIGHT",
                    "32/32/15": "STURDY",
                    "42/42/15": "HEAVY"},
                "40": {
                    "20/20/11": "LIGHT",
                    "26/26/13": "STURDY",
                    "34/34/13": "HEAVY"},
                "30": {
                    "16/16/9": "LIGHT",
                    "21/21/11": "STURDY",
                    "27/27/11": "HEAVY"},
                "20": {
                    "12/12/7": "LIGHT",
                    "16/16/9": "STURDY",
                    "20/20/9": "HEAVY"},
                "10": {
                    "8/8/5": "LIGHT",
                    "11/11/7": "STURDY",
                    "14/14/7": "HEAVY"}
                },
            "PAINTED":{
                "50":[13,6,0],
                "40":[10,4,0],
                "30":[8,3,0],
                "20":[6,2,0],
                "10":[4,1,0]
            },
            "SHADOWED":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
            },
            "ENAMELED":{
                "50":[12,12,6],
                "40":[9,9,4],
                "30":[7,7,3],
                "20":[5,5,2],
                "10":[3,3,1]
            },
            "ALLOYED":{
                "50":[13,13,7],
                "40":[10,10,5],
                "30":[8,8,4],
                "20":[6,6,3],
                "10":[4,4,2]
            },
            "POLISHED":{
                "50":[14,14,8],
                "40":[11,11,6],
                "30":[9,9,5],
                "20":[7,7,3],
                "10":[5,5,2]
            }
		},
        "ARM": {
            "DEFAULT": {
                "50": {
                    "10/10/10": "LIGHT",
                    "13/10/13": "STURDY",
                    "17/17/15": "HEAVY"},
                "40": {
                    "9/9/9": "LIGHT",
                    "12/9/12": "STURDY",
                    "15/15/13": "HEAVY"},
                "30": {
                    "7/7/7": "LIGHT",
                    "9/6/9": "STURDY",
                    "12/12/11": "HEAVY"},
                "20": {
                    "5/5/5": "LIGHT",
                    "7/5/7": "STURDY",
                    "9/9/9": "HEAVY"},
                "10": {
                    "3/3/3": "LIGHT",
                    "5/3/5": "STURDY",
                    "7/7/7": "HEAVY"}
                },
            "PAINTED":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "SHADOWED":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "ENAMELED":{
                "50":[12,12,6],
                "40":[9,9,4],
                "30":[7,7,3],
                "20":[5,5,2],
                "10":[3,3,1]
			},
            "ALLOYED":{
                "50":[13,13,7],
                "40":[10,10,5],
                "30":[8,8,4],
                "20":[6,6,3],
                "10":[4,4,2]
			},
            "POLISHED":{
                "50":[14,14,8],
                "40":[11,11,6],
                "30":[9,9,5],
                "20":[7,7,3],
                "10":[5,5,2]
			}
		},
        "LEG": {
            "DEFAULT": {
                "50": {
                    "10/10/10": "LIGHT",
                    "13/13/13": "STURDY",
                    "17/17/15": "HEAVY"},
                "40": {
                    "9/9/9": "LIGHT",
                    "12/12/12": "STURDY",
                    "15/15/13": "HEAVY"},
                "30": {
                    "7/7/7": "LIGHT",
                    "9/9/9": "STURDY",
                    "12/12/11": "HEAVY"},
                "20": {
                    "5/5/5": "LIGHT",
                    "7/7/7": "STURDY",
                    "9/9/9": "HEAVY"},
                "10": {
                    "3/3/3": "LIGHT",
                    "5/5/5": "STURDY",
                    "7/7/7": "HEAVY"}
                },
            "PAINTED":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "SHADOWED":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "ENAMELED":{
                "50":[12,12,6],
                "40":[9,9,4],
                "30":[7,7,3],
                "20":[5,5,2],
                "10":[3,3,1]
			},
            "ALLOYED":{
                "50":[13,13,7],
                "40":[10,10,5],
                "30":[8,8,4],
                "20":[6,6,3],
                "10":[4,4,2]
			},
            "POLISHED":{
                "50":[14,14,8],
                "40":[11,11,6],
                "30":[9,9,5],
                "20":[7,7,3],
                "10":[5,5,2]
			}
		}
	}
}


fed76_weapon_abbrs = [
    {},
    {
        "44_PISTOL": "44revolver",
        "50_CAL": "50cal",
        "10MM_PISTOL": "10mm",
        "10MM_SUBMACHINE": "10mmsub",
        "ALIEN_BLASTER": "alien",
        "ASSAULT_RIFLE": "assault",
        "AUTO_GRENADE": "autolauncher",
        "BLUNDERBUSS": "blunderbuss",
        "POWDER_PISTOL": "powderpistol",
        "POWDER_RIFLE": "powderrifle",
        "BROADSIDER": "broadsider",
        "COMBAT_RIFLE": "combatrifle",
        "COMBAT_SHOTGUN": "combatshotgun",
        "COMPOUND": "compound",
        "CROSSBOW": "crossbow",
        "BOW": "bow",
        "CRYOLATOR": "cryolator",
        "DOUBLE_BARREL": "doublebarrel",
        "ENCLAVE_PLASMA": "enclave",
        "FAT_MAN": "fatman",
        "FLAMER": "flamer",
        "NAPALMER": "flamer",
        "GAMMA": "gamma",
        "GATLING_GUN": "gatling",
        "GATLING_LASER": "gatlaser",
        "GATLING_PLASMA": "gatplasma",
        "GAUSS_RIFLE": "gauss",
        "HANDMADE": "handmade",
        "HARPOON": "harpoon",
        "HUNTING_RIFLE": "hunting",
        "LASER_PISTOL": "laser",
        "LASER_RIFLE": "laser",
        "LASER_SNIPER_RIFLE": "laser",
        "LEVER_ACTION": "lever",
        "LIGHT_MACHINE_GUN": "lmg",
        "M79": "grenadelauncher",
        "MINIGUN": "minigun",
        "MISSILE_LAUNCHER": "misslelauncher",
        "PEPPER_SHAKER": "pepper",
        "PIPE_BOLT_ACTION": "pipebolt",
        "PIPE_PISTOL": "pipe",
        "PIPE_RIFLE": "pipe",
        "PIPE_REVOLVER": "piperevolver",
        "PLASMA_PISTOL": "plasma",
        "PLASMA_RIFLE": "plasma",
        "PLASMA_SNIPER_RIFLE": "plasma",
        "PLASMA_THROWER": "plasma",
        "PLASMA_SHOTGUN": "plasma",
        "PUMP_ACTION_SHOTGUN": "pump",
        "RADIUM_": "radium",
        "RAILWAY": "railway",
        "ASSAULTRON_HEAD": "assaulthead",
        "SINGLE_ACTION_REVOLVER": "singlerevolver",
        "SUBMACHINE_GUN": "submachine",
        "TESLA": "tesla",
        "DRAGON": "dragon",
        "FIXER": "fixer",
        "ULTRACITE_GATLING_LASER": "ultragatling",
        "ULTRACITE_LASER": "ultralaser",
        "WESTERN_REVOLVER": "western",
        "ASSAULTRON_BLADE": "assaultblade",
        "BASEBALL_BAT": "baseball",
        "BATON": "baton",
        "BEAR_ARM": "bear",
        "BOARD": "board",
        "BONE_CLUB": "boneclub",
        "BONE_HAMMER": "bonehammer",
        "BOWIE_KNIFE": "bowie",
        "BOXING_GLOVE": "box",
        "CHAINSAW": "chainsaw",
        "CHINESE_OFFICER_SWORD": "chinesesword",
        "COMBAT_KNIFE": "combatknife",
        "CULTIST_BLADE": "cultistblade",
        "CULTIST_DAGGER": "cultistdagger",
        "TAMBO": "tambo",
        "DEATHCLAW_GAUNTLET": "deathclaw",
        "DRILL": "drill",
        "FIRE_AXE": "fireaxe",
        "GOLF_CLUB": "golfclub",
        "GROGNAKS_AXE": "grognak",
        "GUITAR_SWORD": "guitarsword",
        "HATCHET": "hatchet",
        "KNUCKLES": "knuckles",
        "LEAD_PIPE": "leadpipe",
        "MACHETE": "machete",
        "MEAT_HOOK": "meathook",
        "MOLE_MINER_GAUNTLET": "molegauntlet",
        "BUZZ_BLADE": "buzzblade",
        "MULTI_PURPOSE_AXE": "multiaxe",
        "PICKAXE": "pickaxe",
        "PIPE_WRENCH": "pipewrench",
        "PITCHFORK": "pitchfork",
        "POLE_HOOK": "polehook",
        "POOL_CUE": "pool",
        "POWER_FIST": "powerfist",
        "REVOLUTIONARY_SWORD": "revolutionarysword",
        "RIPPER": "ripper",
        "ROLLING_PIN": "rollingpin",
        "SHEPHERDS_CROOK": "shepherdscrook",
        "SHEEPSQUATCH_CLUB": "sheepclub",
        "SHEEPSQUATCH_STAFF": "sheepstaff",
        "SHISHKEBAB": "shishkebab",
        "SHOVEL": "shovel",
        "SICKLE": "sickle",
        "SKI_SWORD": "skisword",
        "SLEDGEHAMMER": "sledgehammer",
        "SPEAR": "spear",
        "SUPER_SLEDGE": "supersledge",
        "SWITCHBLADE": "switchblade",
        "THE_TENDERIZER": "Tender",
        "TIRE_IRON": "tireiron",
        "WALKING_CANE": "walkingcane",
        "WAR_DRUM": "wardrum"
    },
    {
        "aa": "aa",
        "ari": "ari",
        "ass": "a",
        "b": "b",
        "ber": "br",
        "exe": "exe",
        "ext": "ext",
        "f": "f",
        "gou": "gour",
        "gs": "gs",
        "h": "h",
        "i": "i",
        "jug": "jug",
        "j": "j",
        "med": "m",
        "ms": "mutslayer",
        "mu": "mu",
        "n": "n",
        "q": "q",
        "st": "st",
        "sup": "su",
        "tro": "t",
        "ts": "ts",
        "v": "v",
        "z": "z"
    },
    {
        "e3": "e",
        "e": "e",
        "25": "ffr",
        "50c": "50",
        "ss": "ss",
        "40p": "40p",
        "ap": "ine",
        "25a": "hit",
        "50l": "50l",
        "50h": "50h",
        "bash": "50b",
        "sent": "ste",
        "block": "50r",
        "last": "last"
    },
    {
        "25": "25",
        "15r": "15r",
        "15v": "15v",
        "90": "90",
        "dur": "dur",
        "s": "str",
        "p": "per",
        "a": "agi",
        "e": "end",
        "stealth": "gho",
        "40": "40",
        "block": "15b",
        "ms": "ms",
        "50": "50dr",
        "250": "250"
    }
]


fed76_armor_abbrs = [
    {},
    {
        "COMBAT": "combat",
        "LEATHER": "leather",
        "MARINE": "marine",
        "METAL": "metal",
        "RAIDER": "raider",
        "ROBOT": "robot",
        "URBAN_SCOUT": "scout",
        "FOREST_SCOUT": "scout",
        "TRAPPER": "trapper",
        "WOOD": "wood"
    },
    {
        "ari":"ari",
        "ass": "assn",
        "auto": "autostim",
        "bol": "bolst",
        "cham": "cham",
        "cloak": "cloak",
        "ext": "ext",
        "gs": "ghoulslayer",
        "h": "hunter",
        "ls": "lifesaving",
        "ms": "mutslayer",
        "mu": "mut",
        "n": "noct",
        "oe": "over",
        "r": "regen",
        "tro": "troubleshooter",
        "u": "uny",
        "v": "vang",
        "w": "weightless",
        "z": "zealot"
    },
    {
        "int": "int",
        "ap": "ap",
        "str": "str",
        "hard": "hard",
        "25p": "poison",
        "25c": "warm",
        "25f": "fire",
        "25r": "rad",
        "luck": "lck",
        "end": "end",
        "per": "per",
        "agi": "agi",
        "glut": "glut",
        "cha": "cha",
        "25d": "env"
    },
    {
        "wwr": "wpn",
        "sent": "sent",
        "acrobat": "acrobat",
        "cav": "cav",
        "sneak": "sneak",
        "fwr": "food",
        "awr": "ammo",
        "jwr": "junk",
        "dur": "dur",
        "ldr": "limb",
        "block": "blocker",
        "energy": "ele",
        "fire": "burn",
        "cryo": "icy",
        "poison": "tox",
        "doc": "doc",
        "lock": "safe",
        "rad": "diss",
        "aqua": "aqua"
    }
]


filter_flags = {
    4: "WEAPON",
    8: "ARMOR",
    16: "APPAREL",
    32: "FOOD_DRINK",
    64: "AID",
    1024: "NOTE",
    4096: "MISC",
    8192: "JUNK",
    16384: "MODS",
    32768: "AMMO",
    65536: "HOLO",
    266240: "MISC",
    270336: "SCRAP"
}


def get_legendary_abbr(item_desc: str, descriptions):
    desc = item_desc.lower().replace('\n', '').replace('â¬', '').replace('¬', '')
    effects = 0
    item_legendary_effects = ''
    for star in range(3):
        for legendary_effect in descriptions[star]:
            if descriptions[star][legendary_effect].lower() in desc:
                while effects < star:
                    effects += 1
                    item_legendary_effects += '/'
                
                item_legendary_effects += legendary_effect
                break
    return item_legendary_effects


def get_armor_type(item_text):
    for i, (k, v) in enumerate(armor_types.items()):
        if v.lower() in item_text.lower():
            return k
    return ''
    

def get_armor_grade(item_text):
    if armor_grades['HEAVY'] in item_text:
        return 'HEAVY'
    if armor_grades['STURDY'] in item_text:
        return 'STURDY'
    return ''


def reduce_resistances(dr, er, rr, resistances):
    return dr - resistances[0], er - resistances[1], rr - resistances[2],


def lookup_armor_grade(armor_full_name, armor_type, armor_piece, armor_level: str, dr: int, er: int, rr: int):
    grade = ''
    if(armor_piece == 'CHEST_PIECE'):
        piece = 'CHEST'
    elif (armor_type == 'ROBOT'):
        if(armor_piece in ['LEFT_ARM', 'RIGHT_ARM']):
            piece = 'ARM'
        else:
            piece = 'LEG'
    else:
        piece = 'LIMB'
                
    for material in graded_armor[armor_type][piece]:
        if material != 'DEFAULT' and armor_prefixes[material] in armor_full_name:
            dr, er, rr = reduce_resistances(dr, er, rr, graded_armor.get(armor_type).get(piece).get(material).get(armor_level))

    resistances = '/'.join([str(dr), str(er), str(rr)])
    if armor_piece and armor_type:
        grade = graded_armor.get(armor_type).get(piece).get('DEFAULT').get(armor_level).get(resistances)
    if not grade:
        return '/'.join([str(dr), str(er), str(rr)])
    return grade


def get_armor_piece(item_text):
    for i, (k, v) in enumerate(armor_pieces.items()):
        if any((_v in item_text.lower()) for _v in v.lower().split('||')):
            return k
    return ''


def get_armor_piece_abbr(item_text):
    for i, (k, v) in enumerate(armor_pieces.items()):
        if any((_v in item_text.lower()) for _v in v.lower().split('||')):
            return armor_pieces_abbr.get(k)
    return ''


def remove_prefixes(item_text: str, prefixes_to_remove):
    new_text = item_text
    for i, (k, v) in enumerate(prefixes_to_remove.items()):
        if v in new_text:
            new_text = str.replace(new_text, v, '', 1).strip()
    return new_text


def get_item_name_short(item_text: str, item_names):
    text = item_text.lower()
    for i, (k, v) in enumerate(item_names.items()):
        if v.lower() in text:
            if k == 'RAIDER' and item_names['RAIDER_POWER'].lower() in text:
                return item_names['RAIDER_POWER']
            elif k == 'MARINE' and item_names['ARCTIC_MARINE'].lower() in text:
                return item_names['ARCTIC_MARINE']
            elif k == 'ROBOT' and item_names['BOTSMITH'].lower() in text:
                return item_names['BOTSMITH']
            return v
    return ''
    

def format_for_pricecheck(item_text: str, item_legendary_abbr, fed76_abbrs, armor_grade: str = None, armor_piece: str = None):
    if item_text == 'RAIDER_POWER':
        return ''
    item_arg = ''
    for i, (k, v) in enumerate(fed76_abbrs[0].items()):
        if armor_grade:
            if k in item_text:
                item_arg = fed76_abbrs[1][k]
                break
        elif v.lower() in item_text.lower():
            item_arg = fed76_abbrs[1][k]
            break
    
    if not item_arg:
        return ''
    
    abbr_arg = ''
    for k in range(len(item_legendary_abbr)):
        if not item_legendary_abbr[k]:
            break
        
        if abbr_arg:
            abbr_arg = abbr_arg + '%2F'
            
        if item_legendary_abbr[k] in fed76_abbrs[k + 2]:
            abbr_arg = abbr_arg + fed76_abbrs[k + 2][item_legendary_abbr[k]]
        else:
            abbr_arg = abbr_arg + item_legendary_abbr[k]

    if armor_grade:
        return item_arg + '&effects=' + abbr_arg + '&grade=' + armor_grade.title() + '&piece=' + armor_piece
    else:
        return item_arg + '&effects=' + abbr_arg


def format_plan_prices(plan):
    if(not plan or len(plan) < 18 or plan[15] == '' or not plan[17] or len(plan[17]) < 1):
        return
    
    temp_price = str.replace(plan[17], '**Estimate:**', '', 1).strip()
    temp_price = str.replace(temp_price, 'Available from NPC vendors for', '', 1).strip()
    temp_price = str.replace(temp_price, 'caps', '', 1).strip()
    prices = str.split(temp_price, '-', 1)
    if(len(prices) == 2):
        low = prices[0].strip()
        high = prices[1].strip()
        plan.append(low)
        plan.append(high)
    
    if(str.find(plan[17], 'NPC') != -1):
        plan[17] = npc_vendors
    elif(len(plan) == 20):
        plan[17] = ''
    else:
        plan[17] = temp_price


def load_translation(lang:dict):
    global column_names
    global item_sources
    global filter_flag_names
    global armor_grades
    global armor_pieces
    global armor_pieces_abbr
    global armor_types
    global armor_effects
    global armor_descriptions
    global weapon_effects
    global weapon_descriptions
    global armor_prefixes
    global armor_mod_leaded
    global weapon_type_melee
    global weapon_type_ranged
    global npc_vendors
    column_names = lang['COLUMN_NAMES']
    item_sources = lang['ITEM_SOURCES']
    filter_flag_names = lang['FILTER_FLAGS']
    armor_grades = lang['ARMOR_GRADES']
    armor_pieces = lang['ARMOR_PIECES']
    armor_pieces_abbr = lang['ARMOR_PIECES_ABBREVIATED']
    armor_types = lang['ARMOR_TYPES']
    fed76_weapon_abbrs[0] = lang['WEAPONS']
    armor_effects = lang['LEGENDARY_ARMOR']['EFFECTS']
    armor_descriptions = lang['LEGENDARY_ARMOR']['DESCRIPTIONS']
    weapon_effects = lang['LEGENDARY_WEAPON']['EFFECTS']
    weapon_descriptions = lang['LEGENDARY_WEAPON']['DESCRIPTIONS']
    armor_prefixes = lang['ARMOR_PREFIXES']
    armor_mod_leaded = lang['MISC']['ARMOR_MOD_LEADED']
    weapon_type_melee = lang['MISC']['WEAPON_TYPE_MELEE']
    weapon_type_ranged = lang['MISC']['WEAPON_TYPE_RANGED']
    npc_vendors = lang['MISC']['NPC_VENDORS']
    for i, (k, v) in enumerate(fed76_armor_abbrs[1].items()):
        if k in lang['ARMOR_TYPES']:
            fed76_armor_abbrs[0][k] = lang['ARMOR_TYPES'][k]
        

def printLocalized(values: object, sep: str | None = ' '):
    if len(values) > 2 and values[2] in filter_flag_names:
        values[2] = filter_flag_names[values[2]]
    if len(values) > 3 and values[3] in armor_types:
        values[3] = armor_types[values[3]]
    if len(values) > 5 and values[5] in armor_grades:
        values[5] = armor_grades[values[5]]
    
    print(sep.join(map(str, values)))


def main():
    parser = argparse.ArgumentParser(
        prog='InventOMatic-Parser',
        description='Script for parsing inventory dump from invent-o-matic stash for Fallout 76',
        epilog='Version 1.3.5, Written by Zelia')
    parser.add_argument('-f', metavar='filename', type=str, required=True,
                        help='Path to inventory dump file')
    parser.add_argument('-l', metavar='language', type=str, default='en',
                        help='Optional translation language, default is English')
    parser.add_argument('-s', metavar='separator', type=str, default='\t',
                        help='Optional output value separator, default is TAB')
    parser.add_argument('-e', metavar='encoding', type=str, default='utf8',
                        help='Optional encoding for input/output, default is utf8')
    parser.add_argument('-pc', action='store_true',
                        help='Request price checks from fed76.info \
                        (significantly increases processing time)')

    args = parser.parse_args()
    filename = args.f
    separator = args.s
    lang = args.l
    encoding = args.e
    is_pricecheck = args.pc
    language_filename = "lang_" + lang + ".json"
    pricecheck_api_url = "https://fed76.info/pricing-api/?item="
    pricecheck_plans_api_url = "https://fed76.info/plan-api/?id="
    plan_database_url = r"https://docs.google.com/spreadsheets/d/1Ul78ln8sBzFVTcaNL42aWea6j9v6CXA7nMWnM6O56rk/export?format=xlsx"
    plan_database_file = "PlanList.xlsx";
    plan_database_file_cache_time = 3600
    
    sys.stdout.reconfigure(encoding=encoding)
    sys.stdin.reconfigure(encoding=encoding)
    sys.stderr.reconfigure(encoding=encoding)

    if not exists(filename):
        print('Invalid file path %s' % (filename))
        return
    
    if not exists(language_filename):
        print('Invalid language file path %s' % (language_filename))
        return
    
    with open(filename, encoding=encoding) as json_data:
        data = json.load(json_data)

    with open(language_filename, encoding=encoding) as json_lang_data:
        lang_data = json.load(json_lang_data)
        load_translation(lang_data)
    
    account_name = ''
    count_armor = 0
    count_weapon = 0
    count_plan = 0
    count_other = 0
    count_duplicate = 0
    count_duplicate_pc = 0
    count_plan_pc = 0
    item_text = ''
    item_type = ''
    item_desc = ''
    item_count = 0
    item_level = 0
    item_legendary_stars = 0
    item_effects = ['', '', '']
    item_name_short = ''
    items = {}
    plan_db_cached = -1
    pricecheck_urls = {}
    pricecheck_plans = {}

    for character_name in data['characterInventories']:
        account_name = data['characterInventories'][character_name].get('AccountInfoData').get('name')
        # print('Account: %s, Character: %s' % (account_name, character_name))
        print(
            column_names['ITEM_NAME'],
            column_names['COUNT'],
            column_names['ITEM_TYPE'],
            column_names['TYPE'],
            column_names['ARMOR_PIECE'],
            column_names['ARMOR_GRADE'],
            column_names['STARS'],
            column_names['LEVEL'],
            column_names['ABBR'],
            column_names['PREFIX'],
            column_names['MAJOR'],
            column_names['MINOR'],
            column_names['ACCOUNT'],
            column_names['CHAR'],
            column_names['SOURCE'],
            column_names['FULL_ITEM_NAME'],
            column_names['FED76_PRICE'],
            column_names['QUICKSALE'],
            column_names['LOW'],
            column_names['HIGH'],
            column_names['NICHE'],
            sep=separator)

        for item_source in item_sources:
            if not data['characterInventories'][character_name].get(item_source):
                continue

            for item in data['characterInventories'][character_name].get(item_source):
                item_text = item['text']
                item_count = item['count']
                item_desc = ''
                existing_count = 0
                item_legendary_stars = item['numLegendaryStars']

                item_type = filter_flags.get(
                    item['filterFlag']) or filter_flags.get(
                    item['filterFlag']^0x1) or item['filterFlag'] # favourited items have 0x1 flag set

                # LEGENDARY ARMOR
                if item_type == 'ARMOR' and item['itemLevel'] != 0:
                    armor_dr = 0
                    armor_er = 0
                    armor_rr = 0
                    is_pricecheck_abbr_valid = True
                    item_level = str(item['itemLevel'])
                    for item_card_entry in item['ItemCardEntries']:
                        if item_card_entry['text'] == 'DESC':
                            item_desc = item_card_entry['value']
                        elif item_card_entry['text'] == '$dr':
                            if item_card_entry['damageType'] == 1:
                                armor_dr = int(item_card_entry['value'])
                            elif item_card_entry['damageType'] == 4:
                                armor_er = int(item_card_entry['value'])
                            elif item_card_entry['damageType'] == 6:
                                armor_rr = int(item_card_entry['value'])

                    item_legendary_abbr = get_legendary_abbr(
                        item_desc, armor_descriptions)
                    abbrs = item_legendary_abbr.split('/')

                    item_effects = ['', '', '']
                    for k in range(len(abbrs)):
                        if abbrs[k] != '':
                            item_effects[k] = (armor_effects[k][abbrs[k]])
                        else:
                            is_pricecheck_abbr_valid = False

                    if item_legendary_stars > 1 and len(abbrs) > 1 and abbrs[1] == '25r':
                        armor_rr -= 25
                    if armor_mod_leaded in item_text:
                        armor_rr -= 10

                    item_name_no_prefix = remove_prefixes(item_text, armor_effects[0])
                    armor_type = get_armor_type(item_name_no_prefix)
                    armor_piece_long = get_armor_piece(item_name_no_prefix)
                    armor_piece_abbr = get_armor_piece_abbr(item_name_no_prefix)

                    armor_grade = ''
                    if armor_type in graded_armor:
                        armor_grade = get_armor_grade(item_name_no_prefix)
                        if armor_grade == '' and armor_piece_abbr and armor_type:
                            armor_grade = lookup_armor_grade(item_name_no_prefix, armor_type, armor_piece_long, item_level, armor_dr, armor_er, armor_rr)
                    
                    if bool(armor_piece_long) and bool(item_name_short):
                        lookup_name = get_item_name_short(item_name_no_prefix, armor_types)
                        lookup_grade = '' if '/' in armor_grade or not bool(armor_grade) else (armor_grades[armor_grade] + ' ')
                        if not bool(lookup_name):
                            item_name_short = item_name_no_prefix
                        else:
                            item_name_short = str.format('%s%s%s' % (
                                lookup_grade,
                                lookup_name + ' ',
                                armor_pieces[get_armor_piece(item_name_no_prefix)].split('||')[0]))
                    else:
                        item_name_short = item_name_no_prefix

                    count_armor += 1
                    if (is_pricecheck
                        and armor_type
                        and int(item_level) >= 45
                        and is_pricecheck_abbr_valid
                        and armor_grade.find('/') == -1):
                        pricecheck_arg = format_for_pricecheck(armor_type, abbrs, fed76_armor_abbrs, armor_grade or 'STURDY', armor_piece_abbr)
                        url = pricecheck_api_url + pricecheck_arg
                        if pricecheck_arg and url in pricecheck_urls:
                            existing_count = pricecheck_urls[url][1]
                            count_duplicate_pc += 1
                        if pricecheck_arg:
                            pricecheck_urls[url] = [item_name_short,
                                item_count + existing_count,
                                item_type,
                                armor_type,
                                armor_piece_abbr,
                                armor_grade,
                                item_legendary_stars,
                                item_level,
                                item_legendary_abbr,
                                item_effects[0], item_effects[1], item_effects[2],
                                account_name,
                                character_name,
                                item_sources[item_source],
                                item_text]
                            continue
                    item_id = str.format('%s %s %s %s %s %s' % (item_name_short, armor_type, armor_grade, armor_piece_abbr, item_legendary_abbr, item_level))
                    if item_id in items:
                        existing_count = items[item_id][1]
                        count_duplicate += 1
                    items[item_id] = [item_name_short,
                        item_count,
                        item_type,
                        armor_type,
                        armor_piece_abbr,
                        armor_grade,
                        item_legendary_stars,
                        item_level,
                        item_legendary_abbr,
                        item_effects[0], item_effects[1], item_effects[2],
                        account_name,
                        character_name,
                        item_sources[item_source],
                        item_text]

                # LEGENDARY WEAPONS
                elif item_type == 'WEAPON' and item['itemLevel'] != 0:
                    is_pricecheck_abbr_valid = True
                    item_level = str(item['itemLevel'])
                    weapon_type = weapon_type_ranged

                    for item_card_entry in item['ItemCardEntries']:
                        if item_card_entry['text'] == 'DESC':
                            item_desc = item_card_entry['value']
                            break
                        elif item_card_entry['text'] == '$speed':
                            weapon_type = weapon_type_melee

                    item_legendary_abbr = get_legendary_abbr(
                        item_desc.lower(), weapon_descriptions)
                    abbrs = item_legendary_abbr.split('/')

                    item_effects = ['', '', '']
                    for k in range(len(abbrs)):
                        if abbrs[k] != '':
                            item_effects[k] = (weapon_effects[k][abbrs[k]])
                        else:
                            is_pricecheck_abbr_valid = False

                    item_name_short = get_item_name_short(item_text, fed76_weapon_abbrs[0])
                    if not bool(item_name_short):
                        item_name_short = remove_prefixes(item_text, weapon_effects[0])
                    
                    count_weapon += 1
                    if (is_pricecheck
                        and item['itemLevel'] >= 45
                        and is_pricecheck_abbr_valid):
                        pricecheck_arg = format_for_pricecheck(item_text, abbrs, fed76_weapon_abbrs)
                        url = pricecheck_api_url + pricecheck_arg
                        if url in pricecheck_urls:
                            existing_count = pricecheck_urls[url][1]
                            count_duplicate_pc += 1
                        if pricecheck_arg:
                            pricecheck_urls[url] = [item_name_short,
                                item_count + existing_count,
                                item_type,
                                weapon_type,
                                '', '',
                                item_legendary_stars,
                                item_level,
                                item_legendary_abbr,
                                item_effects[0], item_effects[1], item_effects[2],
                                account_name,
                                character_name,
                                item_sources[item_source],
                                item_text]
                            continue
                    item_id = str.format('%s %s %s' % (item_name_short, item_legendary_abbr, item_level))
                    if item_id in items:
                        existing_count = items[item_id][1]
                        count_duplicate += 1
                    items[item_id] = [item_name_short,
                            item_count + existing_count,
                            item_type,
                            weapon_type,
                            '', '',
                            item_legendary_stars,
                            item_level,
                            item_legendary_abbr,
                            item_effects[0], item_effects[1], item_effects[2],
                            account_name,
                            character_name,
                            item_sources[item_source],
                            item_text]

                # LEGENDARY APPAREL
                elif item_type == 'APPAREL' and item_legendary_stars != 0:
                    item_level = str(item['itemLevel'])
                    item_legendary_stars = item['numLegendaryStars']
                    for item_card_entry in item['ItemCardEntries']:
                        if item_card_entry['text'] == 'DESC':
                            item_desc = item_card_entry['value']
                    
                    item_legendary_abbr = get_legendary_abbr(
                        item_desc.lower(), armor_descriptions)
                    abbrs = item_legendary_abbr.split('/')

                    item_effects = ['', '', '']
                    for k in range(len(abbrs)):
                        if abbrs[k] != '':
                            item_effects[k] = (armor_effects[k][abbrs[k]])
                            
                    count_other += 1
                    printLocalized([item_text,
                          item_count,
                          item_type,
                          '', '', '',
                          item_legendary_stars,
                          item_level,
                          item_legendary_abbr,
                          item_effects[0], item_effects[1], item_effects[2],
                          account_name,
                          character_name,
                          item_sources[item_source],
                          item_text],
                          sep=separator)

                # PLANS/RECIPES
                elif item_type == 'NOTE':
                    count_plan += 1
                    if (is_pricecheck and item['isTradable']):
                        if item_text in pricecheck_plans:
                            existing_count = pricecheck_plans[item_text][1]
                            count_duplicate += 1
                        pricecheck_plans[item_text] = [item_text,
                          item_count + existing_count,
                          item_type,
                          '', '', '', '', '', '', '', '', '',
                          account_name,
                          character_name,
                          item_sources[item_source]]
                        continue
                    
                    if item_text in items:
                        existing_count = items[item_text][1]
                        count_duplicate += 1
                    items[item_text] = [item_text, item_count + existing_count, item_type,
                                        '', '', '', '', '', '', '', '', '',
                                        account_name, character_name, item_sources[item_source]]
                    
                # Apparel, aid, food/drink, mods, notes, misc, junk, ammo...
                else:
                    count_other += 1
                    if item_text in items:
                        existing_count = items[item_text][1]
                    items[item_text] = [item_text, item_count + existing_count, item_type,
                                        '', '', '', '', '', '', '', '', '',
                                        account_name, character_name, item_sources[item_source]]

    parse_time = time.time()

    if is_pricecheck:
        # LEGENDARY PRICE CHECKING
        conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
        PARALLEL_REQUESTS = 6
        results = {}

        async def gather_with_concurrency(n):
            semaphore = asyncio.Semaphore(n)
            session = aiohttp.ClientSession(connector=conn)

            async def get(url):
                async with semaphore:
                    async with session.get(url, ssl=False) as response:
                        obj = json.loads(await response.read())
                        if response.status == 200:
                            results[url] = obj
                        else:
                            print('Error pricechecking %s' % url)
            await asyncio.gather(*(get(url) for url in pricecheck_urls))
            await session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(gather_with_concurrency(PARALLEL_REQUESTS))
        conn.close()

        for result in results:
            price = results[result]['price']
            if isinstance(price, numbers.Number):
                price = int(price)
            pricecheck_urls[result].append(price)
            pricecheck_urls[result].append(results[result]['review']['details']['vendor'])
            pricecheck_urls[result].append(results[result]['review']['details']['market-low'])
            pricecheck_urls[result].append(results[result]['review']['details']['market-high'])
            pricecheck_urls[result].append(results[result]['review']['details']['niche'])

        legendary_pricecheck_time = time.time()
        
        # PLANS & RECIPES PRICE CHECKING
        if(not exists(plan_database_file) or (time.time() - getmtime(plan_database_file)) > plan_database_file_cache_time):
            df = pd.read_excel(plan_database_url)
            df.to_excel(plan_database_file)
        else:
            plan_db_cached = int(1 + (time.time() - getmtime(plan_database_file)) / 60)
        
        df = pd.read_excel(plan_database_file, skiprows=9)
        
        fetch_plan_database_time = time.time()
        
        df_selected = df[['formid', 'name']]
        empty_pref = '00000000'
        for row in range(int(df_selected.size / 2)):
            df_selected.values[row][1] = str.lower(df_selected.values[row][1])
            df_selected.values[row][1] = str.replace(df_selected.values[row][1], 'plan:', '', 1).strip()
            df_selected.values[row][1] = str.replace(df_selected.values[row][1], 'recipe:', '', 1).strip()
            if(len(str(df_selected.values[row][0])) < 8):
                df_selected.values[row][0] = str(empty_pref + str(df_selected.values[row][0]))[-8:]
        
        for plan in pricecheck_plans:
            plan_l = str.lower(plan)
            for row in range(int(df_selected.size / 2)):
                index =  str.find(plan_l, df_selected.values[row][1])
                if(index != -1 and (index + len(df_selected.values[row][1])) == len(plan_l)):
                    pricecheck_plans[plan].append(df_selected.values[row][0])
                    count_plan_pc += 1
                    break
        
        conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
        async def gather_with_concurrency(n):
            semaphore = asyncio.Semaphore(n)
            session = aiohttp.ClientSession(connector=conn)

            async def get(plan):
                async with semaphore:
                    if(len(plan) > 15 and plan[15] != ''):
                        async with session.get(pricecheck_plans_api_url + plan[15], ssl=False) as response:
                            obj = json.loads(await response.read())
                            if response.status == 200:
                                plan.append(obj['price'])
                                plan.append(obj['verdict'])
                            else:
                                plan.append('Error pricechecking')
            
            await asyncio.gather(*(get(pricecheck_plans[plan]) for plan in pricecheck_plans))
            await session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(gather_with_concurrency(PARALLEL_REQUESTS))
        conn.close()
        
        plan_pricecheck_time = time.time()
        
        for url in pricecheck_urls:
            printLocalized(pricecheck_urls[url], sep=separator)
        
        for plan in pricecheck_plans:
            format_plan_prices(pricecheck_plans[plan])
            printLocalized(pricecheck_plans[plan], sep=separator)

    for item in items:
        printLocalized(items[item], sep=separator)

    print()
    print('Inventory file loaded: ' + filename)
    print('Language file loaded: ' + language_filename)
    if is_pricecheck:
        print('Prices checked: %s legendary, %s plans (%s duplicates)' % (len(pricecheck_urls), count_plan_pc, count_duplicate_pc))
        print('Plan database fetched in %s seconds %s' % (f'{fetch_plan_database_time - legendary_pricecheck_time:.4g}',
                                                          '(cached %s min ago)' % plan_db_cached if plan_db_cached > 0 else '(url fetch)'))
        print('Price check legendary done in %s seconds' % (f'{legendary_pricecheck_time - parse_time:.4g}'))
        print('Price check plan/recipe done in %s seconds' % (f'{plan_pricecheck_time - fetch_plan_database_time:.4g}'))

    print('Items processed: %s armor, %s weapon, %s plans, %s other, %s items total (%s duplicates)'
          % (count_armor, count_weapon, count_plan, count_other, count_other + count_weapon + count_armor + count_plan,
             count_duplicate + count_duplicate_pc))
    print('File parsed in %s seconds' % (f'{parse_time - start_time:.4g}'))
    print('Process finished in %s seconds' % (f'{time.time() - start_time:.4g}'))
    print('Written by Zelia')


main()
