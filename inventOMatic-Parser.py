import json
import time
import argparse
from os.path import exists

start_time = time.time()

item_sources = {
    "playerInventory": "inv",
    "stashInventory": "sta"
}

weapon_prefixes_to_remove = {
    # paints - TODO add missing ones
    11: "Armor Ace ",
    12: "Blackbird ",
    13: "Blue Camouflage ",
    14: "Copperhead ",
    15: "Dastardly Duo ",
    16: "Ghillie ",
    17: "Gunmetal ",
    18: "Hot Rod ",
    19: "Hot Rod Flames ",
    20: "Intergalactic ",
    21: "Inventor ",
    22: "Light Em Up ",
    23: "Lucille's Lullaby ",
    24: "M.I.N.D. ",
    25: "Matte Black ",
    26: "Nuka-Cola Classic ",
    27: "Nuka-Twist ",
    28: "Poker ",
    29: "Presidential ",
    30: "Red Viper ",
    31: "Rusted ",
    32: "Screaming Eagle Wood ",
    33: "Showstopper ",
    34: "Silver Shroud ",
    35: "Starlet Sniper ",
    36: "Tricentennial ",
    37: "Tropic Lightning ",
    38: "Valorous Alistair ",
    39: "Vault-Tec ",
    40: "All Star ",
    41: "Flames ",

    # Weapon mods - TODO add missing ones
    70: "Targeting ",
    71: "Tactical ",
    72: "Suppressed ",
    73: "Snubnosed ",
    74: "Sighted ",
    75: "Short ",
    76: "Sharpshooter's ",
    77: "Scoped ",
    78: "Focused ",
    79: "Beta Wave ",
    80: "Automatic ",
    81: "Bayoneted ",
    82: "Puncturing ",
    83: "Large ",
    84: "Electrified ",
    85: "Cursed ",
    86: "Bladed ",
    87: "Barbed ",
    88: "Recoil Compensated ",
    89: "Hardened ",
    90: "High Capacity ",
    91: "High Speed ",
    92: "Night-Vision ",
    93: "Marksman's ",
    94: "Prime ",
    95: "Compensated ",
    96: "Recon ",
    97: "Long ",
    98: "Charging ",
    99: "Scattered ",
    100: "Maximum Capacity "
}

armor_prefixes_to_remove = {
    # paints ?

    # Leather
    55: "Boiled ",
    56: "Shadowed ",
    57: "Girded ",
    58: "Treated ",
    59: "Studded ",
    # Raider
    60: "Welded ",
    61: "Tempered ",
    62: "Hardened ",
    63: "Buttressed ",
    # Combat
    64: "Reinforced ",
    65: "Fiberglass ",
    66: "Polymer ",
    67: "BOS ",
    # Metal/Robot
    68: "Painted ",
    69: "Enameled ",
    70: "Alloyed ",
    71: "Polished ",
    # Marine
    72: "Assault ",
    # Wood
    73: "Shrouded ",

    # Misc mods
    74: "Dense ",
    75: "Asbestos Lined ",
    76: "Strengthened ",
    77: "Pocketed ",
    78: "Deep Pocketed ",
    79: "Muffled ",
    80: "Cushioned ",
    81: "Custom Fit ",
    82: "Ultra-Light ",
    83: "Jet Pack "

}

armor_types = {
    "Raider Power": "Raider Power",
    #
    "Arctic Marine": "Arctic Marine",
    "Brotherhood": "Brotherhood",
    "Botsmith": "Botsmith",
    "Civil Engineer": "Civil Engineer",
    "Combat": "Combat",
    "Covert Scout": "Scout Covert",
    "Forest Scout": "Scout Forest",
    "Leather": "Leather",
    "Marine": "Marine",
    "Metal": "Metal",
    "Raider": "Raider",
    "Robot": "Robot",
    "Secret Service": "Secret Service",
    "Solar": "Solar",
    "Thorn": "Thorn",
    "Trapper": "Trapper",
    "Urban Scout": "Scout Urban",
    "Wood": "Wood",
    # Power Armor
    "Excavator": "Excavator",
    "Hellcat": "Hellcat",
    "Strangler Heart": "Strangler Heart",
    "T-45": "T-45",
    "T-51b": "T-51b",
    "T-60": "T-60",
    "T-65": "T-65",
    "Ultracite": "Ultracite",
    "Union": "Union",
    "X-01": "X-01"
}

graded_armor = {
    "Combat": {
        "CHEST": {
            "Default": {
                "50": {
                    "36/36/0": "Light",
                    "47/47/0": "Sturdy",
                    "61/61/0": "Heavy"},
                "40": {
                    "30/30/0": "Light",
                    "40/40/0": "Sturdy",
                    "52/52/0": "Heavy"},
                "30": {
                    "25/25/0": "Light",
                    "33/33/0": "Sturdy",
                    "43/43/0": "Heavy"},
                "20": {
                    "16/16/0": "Light",
                    "21/21/0": "Sturdy",
                    "27/27/0": "Heavy"}
                },
            "Reinforced":{
                "50":[10,10,0],
                "40":[8,8,0],
                "30":[6,6,0],
                "20":[4,4,0]
                },
            "Shadowed":{
                "50":[10,10,0],
                "40":[8,8,0],
                "30":[6,6,0],
                "20":[4,4,0]
                },
            "Fiberglass":{
                "50":[15,15,0],
                "40":[12,12,0],
                "30":[9,9,0],
                "20":[7,7,0]
                },
            "Polymer":{
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
            "Default": {
                "50": {
                    "12/12/0": "Light",
                    "15/15/0": "Sturdy",
                    "20/20/0": "Heavy"},
                "40": {
                    "10/10/0": "Light",
                    "13/13/0": "Sturdy",
                    "17/17/0": "Heavy"},
                "30": {
                    "8/8/0": "Light",
                    "11/11/0": "Sturdy",
                    "14/14/0": "Heavy"},
                "20": {
                    "6/6/0": "Light",
                    "8/8/0": "Sturdy",
                    "11/11/0": "Heavy"}
                },
            "Reinforced":{
                "50":[7,7,0],
                "40":[5,5,0],
                "30":[4,4,0],
                "20":[3,3,0]
                },
            "Shadowed":{
                "50":[7,7,0],
                "40":[5,5,0],
                "30":[4,4,0],
                "20":[3,3,0]
                },
            "Fiberglass":{
                "50":[10,10,0],
                "40":[8,8,0],
                "30":[6,6,0],
                "20":[5,5,0]
                },
            "Polymer":{
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
    "Leather": {
        "CHEST": {
            "Default": {
                "50": {
                    "16/45/0": "Light",
                    "21/59/0": "Sturdy",
                    "28/76/0": "Heavy"},
                "40": {
                    "14/40/0": "Light",
                    "18/52/0": "Sturdy",
                    "24/67/0": "Heavy"},
                "30": {
                    "12/35/0": "Light",
                    "16/45/0": "Sturdy",
                    "21/58/0": "Heavy"},
                "20": {
                    "10/30/0": "Light",
                    "13/39/0": "Sturdy",
                    "17/50/0": "Heavy"},
                "10": {
                    "8/25/0": "Light",
                    "11/32/0": "Sturdy",
                    "15/41/0": "Heavy"},
                "5": {
                    "6/15/0": "Light",
                    "8/20/0": "Sturdy",
                    "11/26/0": "Heavy"},
                "1": {
                    "4/10/0": "Light",
                    "5/13/0": "Sturdy",
                    "7/17/0": "Heavy"},
                },
            "Boiled":{
                "50":[5,15,0],
                "40":[4,12,0],
                "30":[3,9,0],
                "20":[2,6,0],
                "10":[1,3,0],
                "5":[1,2,0],
                "1":[1,1,0]},
            "Shadowed":{
                "50":[5,15,0],
                "40":[4,12,0],
                "30":[3,9,0],
                "20":[2,6,0],
                "10":[1,3,0],
                "5":[1,2,0],
                "1":[1,1,0]},
            "Girded":{
                "50":[10,20,0],
                "40":[8,16,0],
                "30":[6,12,0],
                "20":[4,8,0],
                "10":[2,5,0],
                "5":[1,3,0],
                "1":[1,2,0]},
            "Treated":{
                "50":[15,25,0],
                "40":[12,20,0],
                "30":[9,16,0],
                "20":[6,11,0],
                "10":[3,7,0],
                "5":[2,4,0],
                "1":[1,3,0]},
            "Studded":{
                "50":[20,30,0],
                "40":[16,24,0],
                "30":[12,19,0],
                "20":[8,14,0],
                "10":[4,8,0],
                "5":[2,6,0],
                "1":[1,4,0]}
            },
        "LIMB": {
            "Default": {
                "50": {
                    "11/21/0": "Light",
                    "17/36/0": "Sturdy",
                    "22/47/0": "Heavy"},
                "40": {
                    "9/17/0": "Light",
                    "14/30/0": "Sturdy",
                    "19/39/0": "Heavy"},
                "30": {
                    "7/13/0": "Light",
                    "11/24/0": "Sturdy",
                    "15/31/0": "Heavy"},
                "20": {
                    "5/9/0": "Light",
                    "8/17/0": "Sturdy",
                    "11/22/0": "Heavy"},
                "10": {
                    "3/5/0": "Light",
                    "5/11/0": "Sturdy",
                    "7/14/0": "Heavy"},
                "5": {
                    "2/4/0": "Light",
                    "3/7/0": "Sturdy",
                    "4/9/0": "Heavy"},
                "1": {
                    "1/2/0": "Light",
                    "2/4/0": "Sturdy",
                    "3/6/0": "Heavy"},
                },
            "Boiled":{
                "50":[1,10,0],
                "40":[1,8,0],
                "30":[1,6,0],
                "20":[1,4,0],
                "10":[1,2,0],
                "5":[1,1,0],
                "1":[1,1,0]},
            "Shadowed":{
                "50":[1,10,0],
                "40":[1,8,0],
                "30":[1,6,0],
                "20":[1,4,0],
                "10":[1,2,0],
                "5":[1,1,0],
                "1":[1,1,0]},
            "Girded":{
                "50":[5,13,0],
                "40":[4,10,0],
                "30":[3,8,0],
                "20":[2,6,0],
                "10":[1,4,0],
                "5":[1,2,0],
                "1":[1,2,0]},
            "Treated":{
                "50":[8,16,0],
                "40":[6,13,0],
                "30":[5,10,0],
                "20":[3,8,0],
                "10":[2,5,0],
                "5":[1,4,0],
                "1":[1,3,0]},
            "Studded":{
                "50":[10,30,0],
                "40":[8,24,0],
                "30":[6,19,0],
                "20":[4,14,0],
                "10":[2,8,0],
                "5":[1,6,0],
                "1":[1,4,0]}
            }
    },
    "Metal": {
        "CHEST": {
            "Default": {
                "50": {
                    "51/11/0": "Light",
                    "67/13/0": "Sturdy",
                    "87/14/0": "Heavy"},
                "40": {
                    "42/9/0": "Light",
                    "55/11/0": "Sturdy",
                    "72/12/0": "Heavy"},
                "30": {
                    "33/7/0": "Light",
                    "43/9/0": "Sturdy",
                    "56/10/0": "Heavy"},
                "20": {
                    "24/5/0": "Light",
                    "32/7/0": "Sturdy",
                    "42/7/0": "Heavy"},
                "10": {
                    "20/3/0": "Light",
                    "26/4/0": "Sturdy",
                    "34/4/0": "Heavy"}
            },
            "Painted":{
                "50":[15,3,0],
                "40":[12,2,0],
                "30":[10,2,0],
                "20":[8,1,0],
                "10":[6,1,0]
            },
            "Enameled":{
                "50":[20,4,0],
                "40":[17,3,0],
                "30":[14,2,0],
                "20":[11,2,0],
                "10":[8,1,0]
            },
            "Shadowed":{
                "50":[15,3,0],
                "40":[12,2,0],
                "30":[10,2,0],
                "20":[8,1,0],
                "10":[6,1,0]
            },
            "Alloyed":{
                "50":[25,20,0],
                "40":[21,16,0],
                "30":[17,13,0],
                "20":[13,9,0],
                "10":[10,6,0]
            },
            "Polished":{
                "50":[30,6,0],
                "40":[25,5,0],
                "30":[21,4,0],
                "20":[16,3,0],
                "10":[12,2,0]
            },
		},
        "LIMB": {
            "Default": {
                "50": {
                    "20/5/0": "Light",
                    "26/6/0": "Sturdy",
                    "34/8/0": "Heavy"},
                "40": {
                    "18/4/0": "Light",
                    "24/5/0": "Sturdy",
                    "32/7/0": "Heavy"},
                "30": {
                    "16/3/0": "Light",
                    "21/4/0": "Sturdy",
                    "27/6/0": "Heavy"},
                "20": {
                    "12/2/0": "Light",
                    "16/3/0": "Sturdy",
                    "20/4/0": "Heavy"},
                "10": {
                    "8/1/0": "Light",
                    "11/2/0": "Sturdy",
                    "14/3/0": "Heavy"}
                },
            "Painted":{
                "50":[10,1,0],
                "40":[8,1,0],
                "30":[6,1,0],
                "20":[5,1,0],
                "10":[3,1,0]
            },
            "Enameled":{
                "50":[13,2,0],
                "40":[10,1,0],
                "30":[8,1,0],
                "20":[6,1,0],
                "10":[4,1,0]
            },
            "Shadowed":{
                "50":[10,1,0],
                "40":[8,1,0],
                "30":[6,1,0],
                "20":[5,1,0],
                "10":[3,1,0]
            },
            "Alloyed":{
                "50":[15,3,0],
                "40":[12,2,0],
                "30":[10,2,0],
                "20":[8,1,0],
                "10":[6,1,0]
            },
            "Polished":{
                "50":[20,4,0],
                "40":[16,3,0],
                "30":[13,2,0],
                "20":[10,2,0],
                "10":[7,1,0]
            }
		}
	},
    "Raider": {
        "CHEST": {
            "Default": {
                "45": {
                    "42/15/0": "Light",
                    "54/19/0": "Sturdy",
                    "70/24/0": "Heavy"},
                "35": {
                    "34/12/0": "Light",
                    "44/15/0": "Sturdy",
                    "57/19/0": "Heavy"},
                "25": {
                    "26/9/0": "Light",
                    "34/11/0": "Sturdy",
                    "44/14/0": "Heavy"},
                "15": {
                    "18/6/0": "Light",
                    "24/8/0": "Sturdy",
                    "32/11/0": "Heavy"},
                "5": {
                    "10/4/0": "Light",
                    "13/6/0": "Sturdy",
                    "17/8/0": "Heavy"},
                },
            "Welded":{
                "45":[11,5,0],
                "35":[9,4,0],
                "25":[7,3,0],
                "15":[5,2,0],
                "5":[3,1,0]
			},
            "Tempered":{
                "45":[14,13,0],
                "35":[12,11,0],
                "25":[9,8,0],
                "15":[7,5,0],
                "5":[4,3,0]
			},
            "Hardened":{
                "45":[18,9,0],
                "35":[15,7,0],
                "25":[12,6,0],
                "15":[9,5,0],
                "5":[6,3,0]
			},
            "Buttressed":{
                "45":[23,11,0],
                "35":[19,9,0],
                "25":[15,7,0],
                "15":[11,6,0],
                "5":[7,4,0]
			}
		},
        "LIMB": {
            "Default": {
                "45": {
                    "17/8/0": "Light",
                    "22/10/0": "Sturdy",
                    "28/13/0": "Heavy"},
                "35": {
                    "14/7/0": "Light",
                    "18/9/0": "Sturdy",
                    "23/11/0": "Heavy"},
                "25": {
                    "11/4/0": "Light",
                    "14/6/0": "Sturdy",
                    "18/8/0": "Heavy"},
                "15": {
                    "8/3/0": "Light",
                    "10/5/0": "Sturdy",
                    "13/6/0": "Heavy"},
                "5": {
                    "5/2/0": "Light",
                    "7/3/0": "Sturdy",
                    "9/4/0": "Heavy"},
                },
            "Welded":{
                "45":[9,4,0],
                "35":[7,3,0],
                "25":[5,2,0],
                "15":[3,2,0],
                "5":[1,1,0]
			},
            "Tempered":{
                "45":[10,5,0],
                "35":[8,4,0],
                "25":[6,3,0],
                "15":[4,3,0],
                "5":[2,2,0]
			},
            "Hardened":{
                "45":[11,6,0],
                "35":[9,5,0],
                "25":[7,4,0],
                "15":[5,4,0],
                "5":[3,3,0]
			},
            "Buttressed":{
                "45":[12,7,0],
                "35":[10,6,0],
                "25":[8,5,0],
                "15":[6,5,0],
                "5":[4,4,0]
			}
		}
	},
    "Robot": {
        "CHEST": {
            "Default": {
                "50": {
                    "24/24/13": "Light",
                    "32/32/15": "Sturdy",
                    "42/42/15": "Heavy"},
                "40": {
                    "20/20/11": "Light",
                    "26/26/13": "Sturdy",
                    "34/34/13": "Heavy"},
                "30": {
                    "16/16/9": "Light",
                    "21/21/11": "Sturdy",
                    "27/27/11": "Heavy"},
                "20": {
                    "12/12/7": "Light",
                    "16/16/9": "Sturdy",
                    "20/20/9": "Heavy"},
                "10": {
                    "8/8/5": "Light",
                    "11/11/7": "Sturdy",
                    "14/14/7": "Heavy"}
                },
            "Painted":{
                "50":[13,6,0],
                "40":[10,4,0],
                "30":[8,3,0],
                "20":[6,2,0],
                "10":[4,1,0]
            },
            "Shadowed":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
            },
            "Enameled":{
                "50":[12,12,6],
                "40":[9,9,4],
                "30":[7,7,3],
                "20":[5,5,2],
                "10":[3,3,1]
            },
            "Alloyed":{
                "50":[13,13,7],
                "40":[10,10,5],
                "30":[8,8,4],
                "20":[6,6,3],
                "10":[4,4,2]
            },
            "Polished":{
                "50":[14,14,8],
                "40":[11,11,6],
                "30":[9,9,5],
                "20":[7,7,3],
                "10":[5,5,2]
            }
		},
        "ARM": {
            "Default": {
                "50": {
                    "10/10/10": "Light",
                    "13/10/13": "Sturdy",
                    "17/17/15": "Heavy"},
                "40": {
                    "9/9/9": "Light",
                    "12/9/12": "Sturdy",
                    "15/15/13": "Heavy"},
                "30": {
                    "7/7/7": "Light",
                    "9/6/9": "Sturdy",
                    "12/12/11": "Heavy"},
                "20": {
                    "5/5/5": "Light",
                    "7/5/7": "Sturdy",
                    "9/9/9": "Heavy"},
                "10": {
                    "3/3/3": "Light",
                    "5/3/5": "Sturdy",
                    "7/7/7": "Heavy"}
                },
            "Painted":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "Shadowed":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "Enameled":{
                "50":[12,12,6],
                "40":[9,9,4],
                "30":[7,7,3],
                "20":[5,5,2],
                "10":[3,3,1]
			},
            "Alloyed":{
                "50":[13,13,7],
                "40":[10,10,5],
                "30":[8,8,4],
                "20":[6,6,3],
                "10":[4,4,2]
			},
            "Polished":{
                "50":[14,14,8],
                "40":[11,11,6],
                "30":[9,9,5],
                "20":[7,7,3],
                "10":[5,5,2]
			}
		},
        "LEG": {
            "Default": {
                "50": {
                    "10/10/10": "Light",
                    "13/13/13": "Sturdy",
                    "17/17/15": "Heavy"},
                "40": {
                    "9/9/9": "Light",
                    "12/12/12": "Sturdy",
                    "15/15/13": "Heavy"},
                "30": {
                    "7/7/7": "Light",
                    "9/9/9": "Sturdy",
                    "12/12/11": "Heavy"},
                "20": {
                    "5/5/5": "Light",
                    "7/7/7": "Sturdy",
                    "9/9/9": "Heavy"},
                "10": {
                    "3/3/3": "Light",
                    "5/5/5": "Sturdy",
                    "7/7/7": "Heavy"}
                },
            "Painted":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "Shadowed":{
                "50":[10,10,5],
                "40":[8,8,4],
                "30":[6,6,3],
                "20":[4,4,2],
                "10":[2,2,1]
			},
            "Enameled":{
                "50":[12,12,6],
                "40":[9,9,4],
                "30":[7,7,3],
                "20":[5,5,2],
                "10":[3,3,1]
			},
            "Alloyed":{
                "50":[13,13,7],
                "40":[10,10,5],
                "30":[8,8,4],
                "20":[6,6,3],
                "10":[4,4,2]
			},
            "Polished":{
                "50":[14,14,8],
                "40":[11,11,6],
                "30":[9,9,5],
                "20":[7,7,3],
                "10":[5,5,2]
			}
		}
	}
}

armor_pieces = {
    "Left Arm": "LA",
    "Left Leg": "LL",
    "Right Arm": "RA",
    "Right Leg": "RL",
    "Chest Piece": "CH",
    "Torso": "CH",
    "Helmet": "HELM"
}

armor_descriptions = [
    {
        "ari": "grants up to +20 energy resistance and damage resistance, the higher",
        "ass": "15% damage from humans",
        "auto": "automatically use a stimpak",
        "bol": "grants up to +35 energy resistance and damage resistance, the lower",
        "cham": "become invisible while sneaking and not moving",
        "cloak": "being hit in melee generates a stealth field",
        "ext": "15% damage from mirelurks and insects",
        "gs": "15% damage from ghouls",
        "h": "15% damage from animals",
        "ls": "when incapacitated, gain a 50% chance to revive",
        "ms": "15% damage from super mutants",
        "mu": "10 damage resistance and energy resistance while mutated",
        "n": "damage resistance and energy resistance at night",
        "oe": "increases damage reduction up to +6%",
        "r": "0.5% heal rate",
        "tro": "15% damage from robots",
        "u": "gain up to +3 to all",
        "v": "grants up to +35 energy resistance and damage resistance, the higher",
        "w": "90% weight",
        "z": "15% damage from scorched"
    },
    {
        "int": "1 intelligence",
        "ap": "5% action point regen",
        "str": "1 strength",
        "hard": "receive 7% less explosion damage",
        "25p": "25 poison resistance",
        "25c": "25 cryo resistance",
        "25f": "25 fire resistance",
        "25r": "25 radiation resistance",
        "luck": "1 luck",
        "end": "1 endurance",
        "per": "1 perception",
        "agi": "1 agility",
        "glut": "hunger and thirst grow 10% slower",
        "cha": "1 charisma",
        "25d": "25% reduced disease chance",
    },
    {
        "wwr": "weapon weights reduced by 20%",
        "sent": "75% chance to reduce damage by 15% while not moving",
        "acrobat": "50% fall damage",
        "cav": "75% chance to reduce damage by 15% while sprinting",
        "sneak": "25% less noise while sneaking +25% reduce detection chance",
        "fwr": "food, drink, and chem weights reduced by 20%",
        "awr": "ammo weight reduced by 20%",
        "jwr": "junk item weights reduced by 20%",
        "dur": "50% slower",
        "ldr": "receive 15% less limb damage",
        "block": "15% damage taken while blocking",
        "energy": "5% chance to deal 12 energy damage per second",
        "fire": "5% chance to deal 12 fire damage per second",
        "cryo": "5% chance to deal 12 cryo damage per second",
        "poison": "5% chance to deal 12 poison damage per second",
        "doc": "effectiveness of stimpaks, radaway, and rad-x",
        "lock": "increases size of sweet-spot while picking locks",
        "rad": "0.25% radiation damage recovery",
        "aqua": "grants the ability to breathe underwater",
        "titan": "reduces damage while standing and not moving",
    }
]

weapon_descriptions = [
    {
        "aa": "50% armor penetration",
        "ari": "50% damage based on caps",
        "ass": "50% damage to humans",
        "b": "95% as health decreases",
        "ber": "50% as damage resistance decreases",
        "exe": "50% more damage when your target is below 40% health",
        "ext": "50% damage to insects",
        "f": "damage after each consecutive hit",
        "gou": "24% as you fill your hunger and thirst",
        "gs": "50% damage to ghouls",
        "h": "50% damage to animals",
        "i": "100% damage against targets with full health",
        "j": "damage increases per addiction",
        "jug": "25% as health increases",
        "med": "will heal you and your group",
        "ms": "50% damage to super mutants",
        "mu": "25% as you gain mutations",
        "n": "50% damage at night",
        "q": "300% ammo capacity",
        "st": "100% v.a.t.s. accuracy at +50%",
        "sup": "reduce your target's damage output",
        "tro": "50% damage to robots",
        "ts": "1 projectiles +25% damage",
        "v": "restore 2% health over 2 seconds",
        "z": "50% damage to scorched",
    },
    {
        "e3": "bullets explode for 3%",
        "e": "bullets explode for 20%",
        "25": "25% weapon speed",
        "50c": "50% critical damage",
        "ss": "40% weapon speed",
        "40p": "40% power attack damage",
        "ap": "replenish 15 action points",
        "25a": "25% damage while aiming",
        "50l": "50% limb damage",
        "50h": "50% chance to hit",
        "bash": "50% bash damage",
        "sent": "25% melee damage while not moving",
        "block": "50% melee damage reflection while blocking",
        "last": "the last round in a magazine",
    },
    {
        "25": "25% action point cost",
        "15r": "15% reload speed",
        "15v": "15 bonus v.a.t.s. critical charge",
        "90": "90% weight",
        "dur": "50% slower",
        "s": "1 strength",
        "p": "1 perception",
        "a": "1 agility",
        "e": "1 endurance",
        "stealth": "10% chance to generate a stealth field",
        "40": "40% damage taken while power attacking",
        "block": "15% damage taken while blocking",
        "ms": "100% faster movement speed",
        "50": "50 damage resistance while aiming",
        "250": "250 damage resistance while reloading",
    }
]

armor_effects = [
    {
        "ari": "Aristocrat's",
        "ass": "Assassin's",
        "auto": "Auto Stim",
        "bol": "Bolstering",
        "cham": "Chameleon",
        "cloak": "Cloaking",
        "ext": "Exterminator's",
        "gs": "Ghoul Slayer's",
        "h": "Hunter's",
        "ls": "Life Saving",
        "ms": "Mutant Slayer's",
        "mu": "Mutant's",
        "n": "Nocturnal",
        "oe": "Overeater's",
        "r": "Regenerating",
        "tro": "Troubleshooter's",
        "u": "Unyielding",
        "v": "Vanguard's",
        "w": "Weightless",
        "z": "Zealot's"
    },
    {
        "int": "Intelligence",
        "ap": "Powered",
        "str": "Strength",
        "hard": "Hardy",
        "25p": "Poisoner's",
        "25c": "Warming",
        "25f": "Fireproof",
        "25r": "HazMat",
        "luck": "Luck",
        "end": "Endurance",
        "per": "Perception",
        "agi": "Agility",
        "glut": "Glutton",
        "cha": "Charisma",
        "25d": "Antiseptic",
    },
    {
        "wwr": "Reduced weapon weight",
        "sent": "Sentinel's",
        "acrobat": "Acrobat's",
        "cav": "Cavalier's",
        "sneak": "Improved sneaking",
        "fwr": "Reduced food/drink/chem weight",
        "awr": "Reduced ammo weight",
        "jwr": "Reduced junk weight",
        "dur": "Durability",
        "ldr": "Reduced limn damage",
        "block": "Defender's",
        "energy": "Electrified",
        "fire": "Burning",
        "cryo": "Frozen",
        "poison": "Toxic",
        "doc": "Doctor's",
        "lock": "Safecracker's",
        "rad": "Dissipating",
        "aqua": "Diver's",
        "titan": "Titan's",
    }
]

weapon_effects = [
    {
        "aa": "Anti-armor",
        "ari": "Aristocrat's",
        "ass": "Assassin's",
        "b": "Berserker's",
        "ber": "Bloodied",
        "exe": "Executioner's",
        "ext": "Exterminator's",
        "f": "Furious",
        "gou": "Ghoul Slayer's",
        "gs": "Gourmand's",
        "h": "Hunter's",
        "i": "Instigating",
        "jug": "Juggernaut's",
        "j": "Junkie's",
        "med": "Medic's",
        "ms": "Mutant Slayer's",
        "mu": "Mutant's",
        "n": "Nocturnal",
        "q": "Quad",
        "st": "Stalker's",
        "sup": "Suppressor's",
        "tro": "Troubleshooter's",
        "ts": "Two Shot",
        "v": "Vampire's",
        "z": "Zealot's"
    },
    {
        "e3": "Explosive 3%",
        "e": "Explosive",
        "25": "Rapid",
        "50c": "Vital",
        "ss": "Melee Speed",
        "40p": "Power Attack Damage",
        "ap": "Inertial",
        "25a": "Hitman's",
        "50l": "Crippling",
        "50h": "V.A.T.S. Enhanced",
        "bash": "Basher's",
        "sent": "Steady",
        "block": "Riposting",
        "last": "Last Shot",
    },
    {
        "25": "V.A.T.S. Optimized",
        "15r": "Swift",
        "15v": "Lucky",
        "90": "Lightweight",
        "dur": "Durability",
        "s": "Strength",
        "p": "Perception",
        "a": "Agility",
        "e": "Endurance",
        "stealth": "Ghost's",
        "40": "Defender's",
        "block": "Cavalier's",
        "ms": "Nimble",
        "50": "Steadfast",
        "250": "Resilient",
    }
]

filter_flags = {
    4: "weapon",
    8: "armor",
    16: "apparel",
    32: "food/drink",
    64: "aid",
    1024: "note",
    4096: "misc",
    8192: "junk",
    16384: "mods",
    32768: "ammo",
    65536: "holo",
    266240: "misc",
    270336: "scrap"
}


def get_legendary_abbr(item_desc: str, descriptions):
    effects = 0
    item_legendary_effects = ''
    for star in range(3):
        for legendary_effect in descriptions[star]:
            if descriptions[star][legendary_effect] in item_desc:
                while effects < star:
                    effects += 1
                    item_legendary_effects += '/'
                
                item_legendary_effects += legendary_effect
                break
    return item_legendary_effects


def get_armor_type(item_text):
    for type in armor_types:
        if type in item_text:
            return armor_types[type]


def get_armor_grade(item_text):
    if str.find(item_text, 'Heavy') != -1:
        return 'Heavy'
    elif str.find(item_text, 'Sturdy') != -1:
        return 'Sturdy'
    return ''


def reduce_resistances(dr, er, rr, resistances):
    return dr - resistances[0], er - resistances[1], rr - resistances[2],


def lookup_armor_grade(armor_full_name, armor_type, armor_piece, armor_level: str, dr: int, er: int, rr: int):
    grade = ''
    if(armor_piece == 'CH'):
        piece = 'CHEST'
    elif (armor_type == 'Robot'):
        if(armor_piece in ['LA', 'RA']):
            piece = 'ARM'
        else:
            piece = 'LEG'
    else:
        piece = 'LIMB'
                
    for material in graded_armor.get(armor_type).get(piece):
        if str.find(armor_full_name, material) != -1:
            dr, er, rr = reduce_resistances(dr, er, rr, graded_armor.get(armor_type).get(piece).get(material).get(armor_level))

    resistances = '/'.join([str(dr), str(er), str(rr)])
    if armor_piece and armor_type:
        grade = graded_armor.get(armor_type).get(piece).get('Default').get(armor_level).get(resistances)
    if not grade:
        return '/'.join([str(dr), str(er), str(rr)])
    return grade


def get_armor_piece(item_text):
    for piece in armor_pieces:
        if piece in item_text:
            return armor_pieces[piece]
    return ''


def remove_prefixes(item_text: str, prefixes_to_remove):
    new_text = item_text
    for prefix in prefixes_to_remove:
        if new_text.find(prefixes_to_remove[prefix]) != -1:
            new_text = str.replace(new_text, prefixes_to_remove[prefix], '', 1).strip()
    return new_text


def main():
    parser = argparse.ArgumentParser(
        prog='InventOMatic-Parser',
        description='Script for parsing inventory dump from invent-o-matic stash for Fallout 76',
        epilog='Written by Zelia')
    parser.add_argument('-f', metavar='filename', type=str, required=True,
                        help='Path to inventory dump file')
    parser.add_argument('-s', metavar='separator', type=str, default='\t',
                        help='Optional output value separator, default is TAB')

    args = parser.parse_args()
    filename = args.f
    separator = args.s

    if not exists(filename):
        print('Invalid file path %s' % (filename))
        return
    
    with open(filename) as json_data:
        data = json.load(json_data)

    count_armor = 0
    count_weapon = 0
    count_other = 0
    item_text = ''
    item_type = ''
    item_desc = ''
    item_count = 0
    item_level = 0
    item_legendary_stars = 0
    item_effects = ['', '', '']
    item_name_short = ''

    for character_name in data['characterInventories']:
        account_name = data['characterInventories'][character_name].get('AccountInfoData').get('name')
        print('Account: %s, Character: %s' % (account_name, character_name))
        print('Item Name', 'Count', 'Item Type', 'Type', 'Armor Piece', 'Armor Grade', 
                  'Stars', 'Level', 'Abbr', 'Prefix', 'Major', 'Minor', 'Account',
                  'Char', 'Source', 'Full Item name', sep=separator)

        for item_source in item_sources:
            if not data['characterInventories'][character_name].get(item_source):
                continue

            for item in data['characterInventories'][character_name].get(item_source):
                item_text = item['text']
                item_count = item['count']
                item_desc = ''
                item_type = filter_flags.get(
                    item['filterFlag']) or filter_flags.get(
                    item['filterFlag']^0x1) or item['filterFlag'] # favourited items have 0x1 flag set

                # LEGENDARY ARMOR
                if item_type == 'armor' and item['itemLevel'] != 0:
                    armor_dr = 0
                    armor_er = 0
                    armor_rr = 0
                    item_level = str(item['itemLevel'])
                    item_legendary_stars = item['numLegendaryStars']
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
                        item_desc.lower(), armor_descriptions)
                    abbrs = item_legendary_abbr.split('/')

                    item_effects = ['', '', '']
                    for k in range(len(abbrs)):
                        if abbrs[k] != '':
                            item_effects[k] = (armor_effects[k][abbrs[k]])

                    if item_legendary_stars > 1 and abbrs[1] == '25r':
                        armor_rr -= 25
                    if str.find(item_text, 'Leaded') != -1:
                        armor_rr -= 10

                    armor_type = get_armor_type(item_text)
                    armor_piece = get_armor_piece(item_text)
                    
                    armor_grade = ''
                    if armor_type in graded_armor:
                        armor_grade = get_armor_grade(item_text)
                        if armor_grade == '' and armor_piece and armor_type:
                            armor_grade = lookup_armor_grade(item_text, armor_type, armor_piece, item_level, armor_dr, armor_er, armor_rr)

                    item_name_short = remove_prefixes(
                        item_text, armor_effects[0])
                    item_name_short = remove_prefixes(
                        item_name_short, armor_prefixes_to_remove)

                    count_armor += 1
                    print(item_name_short,
                          item_count,
                          item_type,
                          armor_type,
                          armor_piece,
                          armor_grade,
                          item_legendary_stars,
                          item_level,
                          item_legendary_abbr,
                          item_effects[0], item_effects[1], item_effects[2],
                          account_name,
                          character_name,
                          item_sources[item_source],
                          item_text,
                          sep=separator)

                # LEGENDARY WEAPONS
                elif item_type == 'weapon' and item['itemLevel'] != 0:
                    item_level = str(item['itemLevel'])
                    item_legendary_stars = item['numLegendaryStars']
                    weapon_type = 'Ranged'

                    for item_card_entry in item['ItemCardEntries']:
                        if item_card_entry['text'] == 'DESC':
                            item_desc = item_card_entry['value']
                            break
                        elif item_card_entry['text'] == '$speed':
                            weapon_type = 'Melee'

                    item_legendary_abbr = get_legendary_abbr(
                        item_desc.lower(), weapon_descriptions)
                    abbrs = item_legendary_abbr.split('/')

                    item_effects = ['', '', '']
                    for k in range(len(abbrs)):
                        if abbrs[k] != '':
                            item_effects[k] = (weapon_effects[k][abbrs[k]])

                    item_name_short = remove_prefixes(
                        item_text, weapon_effects[0])
                    item_name_short = remove_prefixes(
                        item_name_short, weapon_prefixes_to_remove)

                    count_weapon += 1
                    print(item_name_short,
                          item_count,
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
                          item_text,
                          sep=separator)

                # LEGENDARY APPAREL
                elif item_type == 'apparel' and item_legendary_stars != 0:
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
                    print(item_text,
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
                          item_text,
                          sep=separator)

                # Apparel, aid, food/drink, mods, notes, misc, junk, ammo...
                else:
                    count_other += 1
                    print(item_text, item_count, item_type, sep=separator)


    print('\nItems processed: %s armor, %s weapon, %s other, %s items total'
          % (count_armor, count_weapon, count_other, count_other + count_weapon + count_armor))
    print('Process finished in %s seconds' % (time.time() - start_time))
    print('Written by Zelia')


main()
