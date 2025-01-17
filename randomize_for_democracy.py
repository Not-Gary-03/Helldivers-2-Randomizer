"""Helldivers Equipment Randomizer
Gary Hayden May, 2025/01/08, Personal Project

NEXT PROBLEM TO SOLVE:
when randomizing equipment from a list and ensuring no duplicates, some members have access
to a larger list than others that should contain everything from the original list plus the
new content they have access to. This new content should still be removed from the list when
it is selected, so multiple members that have access to extra content still won't get
duplicates.

WEIGHTED RANDOMIZATION:
This is my favorite idea. I will rework the randomization algorithm so that instead of generating
a random integer in the range of a list, it will randomly select a list based upon a weight.
--weight ideas:
the weight of a given list is its length, or rather, how many items is in it. These weights
are summed and a random number is generated between 0 and the sum - 1. Then the program checks
this result against the weights of the lists in order, first selecting the list whose range
the random number falls into, and then reducing the sum by the weights of the lists that
precede the chosen list, allowing the sum to be used as the index of the chosen item.

EXAMPLE:
LIST_OF_EVERYTHING = [\
    [list1, list2, list3],\
    [item1, item2, item3],\
    [obj1, obj2, obj3]]

def sum_lists(l: list[list], indexes: list[int]) -> int:
    returns the sum of the length of the specified nested lists
        
def randomization_func(list of players, nested list of options to choose from, nums: number of options to give each player) -> string:
    iterate through list of players:
        make list that holds "weight" of the options available to the player
        weight_sum = sum of weights in the weight list
        loop nums times:
            select = random number between 0 and (weight_sum - 1)
            iterate through weight list:
                if select is less than sum of weight lists up to and including current list:
                    reduce select by sum of weight lists up to and *not* including current list
                    add select of current list to options
"""

import random
import pyperclip
import groups

#Stratagems:
CHEMICAL_AGENTS, URBAN_LEGENDS = 6, 7
ALL_STRATAGEMS = [["Machine Gun", "Anti-Material Rifle", "Stalwart", "Expendable Anti Tank",\
                "Recoilless Rifle", "Flamethrower", "Autocannon", "Heavy Machine Gun",\
                "Airburst Rocket Launcher", "Commando", "Railgun", "Spear", "WASP Launcher",\
                "!!!LIBERTY!!!"],\
                \
                ["Orbital Gatling Barrage", "Orbital Airburst Strike", "Orbital 120mm HE Barrage",\
                "Orbital 380mm HE Barrage", "Orbital Walking Barrage", "Orbital Laser",\
                "Orbital Napalm Barrage", "Orbital Railcannon Strike"],\
                \
                ["Eagle Strafing Run", "Eagle Airstrike", "Eagle Cluster Bomb",\
                "Eagle Napalm Airstrike", "LIFT-850 Jump Pack", "Eagle Smoke",\
                "Eagle 110mm Rocket Pods", "Eagle 500kg Bomb", "M-102 Fast Recon Vehicle"],\
                \
                ["Orbital Precision Strike", "Orbital Gas Strike", "Orbital EMS Strike",\
                "Orbital Smoke Strike", "E/MG-101 HMG Emplacement", "FX-12 Shield Generator Relay",\
                "A/ARC-3 Tesla Tower"],\
                \
                ["MD-6 Anti-Personnel Minefield", "B-1 Supply Pack", "GL-21 Grenade Launcher",\
                "LAS-98 Laser Cannon", "Incendiary Minefield", "Guard Dog 'Rover'",\
                "Ballistic Shield", "Arc Thrower", "Anti-Tank Minefield", "Quasar Cannon",\
                "Shield Generator Pack"],\
                \
                ["Machine Gun Sentry", "Gatling Sentry", "Mortar Sentry", "Guard Dog (Regular)", \
                "Autocannon Sentry", "Rocket Sentry", "EMS Mortar Sentry", "Patriot Exosuit", \
                "Emancipator Exosuit"],\
                \
                ["Sterilizer", "Guard Dog (Gas)"],\
                \
                ["Directional Shield", "Flame Sentry", "Anti-Tank Emplacement"]]
RED_STRATAGEMS = [["Orbital Gatling Barrage", "Orbital Airburst", "Orbital 120mm HE Barrage",\
                "Orbital 380mm HE Barrage", "Orbital Walking Barrage", "Orbital Laser",\
                "Orbital Napalm Barrage", "Orbital Railcannon", "Eagle Strafing Run",\
                "Eagle Airstrike", "Eagle Cluster", "Eagle Napalm", "Eagle Smoke",\
                "Eagle Rocket Pods", "Eagle 500KG Bomb", "Orbital Precision Strike",\
                "Orbital Gas Strike", "Orbital EMS Strike", "Orbital Smoke Strike"],\
                \
                [],\
                \
                []]
BLUE_STRATAGEMS = [["Machine Gun", "Anti-Material Rifle", "Stalwart", "Expendable Anti Tank",\
                "Recoilless Rifle", "Flamethrower", "Autocannon", "Heavy Machine Gun",\
                "Airburst Rocket Launcher", "Commando", "Railgun", "Spear", "WASP Launcher",\
                "Jump Pack", "Fast Recon Vehicle", "Supply Pack", "Grenade Launcher",\
                "Laser Cannon", "Guard Dog 'Rover'", "Ballistic Shield", "Arc Thrower",\
                "Quasar Cannon", "Shield Generator Pack", "Guard Dog (Regular)",\
                "Patriot Exosuit", "Emancipator Exosuit"],\
                \
                ["Sterilizer", "Guard Dog (Gas)"],\
                \
                ["Directional Shield"]]
GREEN_STRATAGEMS = [["HMG Emplacement", "Shield Generator Relay", "Tesla Tower",\
                "Anti-Personnel Minefield", "Incendiary Minefield", "Anti-Tank Minefield",\
                "Machine Gun Sentry", "Gatling Sentry", "Mortar Sentry", "Autocannon Sentry",\
                "Rocket Sentry", "EMS Mortar Sentry"],\
                \
                [],\
                \
                ["Flame Sentry", "Anti-Tank Emplacement"]]

DEBUG_LIST = [['OBJ ONE', 'OBJ TWO'],\
            ['THING ONE', 'THING TWO'],\
            ['FOO ONE', 'FOO TWO'],\
            ['BAR ONE', 'BAR TWO'],\
            ['CAN ONE', 'CAN TWO'],\
            ['HAN ONE', 'HAN TWO'],\
            ['SPECIAL'],\
            ['OTHER']]

#Weapons & Armor:
STARTING, HM, KXCO, SV, CE = 0, 1, 2, 3, 4
DD, PP, VC, FF, CA, TE, UL = 5, 6, 7, 8, 9, 10, 11
SUPER_CITIZEN = 12
SUPER_STORE = 13
PRE_ORDER = 14
ALL_PRIMARY =[\
    #STARTING: starting equipment, including Liberty Day rewards and
    # other content given to all players for free
    ["AR-23 Liberator", "R2124 Constitution"],\
    #HM: Helldivers Mobilize
    ["AR-23P Liberator Penetrator", "R-63 Diligence", "R-63CS Diligence Counter Sniper",\
    "SMG-37 Defender", "SG-8 Punisher", "SG-8S Slugger", "SG-225 Breaker",\
    "SG-225SP Breaker Spray & Pray", "LAS-5 Scythe", "PLAS-1 Scorcher"],\
    #KXCO: Killzone cross-over free rewards
    ["PLAS-39 Accelerator Rifle", "StA-11 SMG"],\
    #SV: Steeled Veterans
    ["AR-23C Liberator Concussive", "SG-225IE Breaker Incendiary", "JAR-5 Dominator"],\
    #CE: Cutting Edge
    ["SG-8P Punisher Plasma", "ARC-12 Blitzer", "LAS-16 Sickle"],\
    #DD: Democratic Detonation
    ["BR-14 Adjudicator", "CB-9 Exploding Crossbow", "R-36 Eruptor"],\
    #PP: Polar Patriots
    ["AR-61 Tenderizer", "SMG-72 Pummeler", "PLAS-101 Purifier"],\
    #VC: Viper Commandos
    ["AR-23A Liberator Carbine"],\
    #FF: Freedom's Flame
    ["SG-451 Cookout", "FLAM-66 Torcher"],\
    #CA: Chemical Agents
    [],\
    #TE: Truth Enforcers
    ["SMG-32 Reprimand", "SG-20 Halt"],\
    #UL: Urban Legends
    [],\
    #End Warbonds
    #SUPER_CITIZEN:
    ["MP-98 Knight"],\
    #SUPER_STORE:
    ["StA-52 Assault Rifle"],\
    #PRE_ORDER:
    []]
ALL_SECONDARY = [\
    #STARTING: starting equipment, including Liberty Day rewards and
    # other content given to all players for free
    ["R-2 Peacemaker"],\
    #HM: Helldivers Mobilize
    ["P-19 Redeemer"],\
    #KXCO: Killzone cross-over free rewards
    [],\
    #SV: Steeled Veterans
    ["P-4 Senator"],\
    #CE: Cutting Edge
    ["LAS-7 Dagger"],\
    #DD: Democratic Detonation
    ["GP-31 Grenade Pistol"],\
    #PP: Polar Patriots
    ["P-113 Verdict"],\
    #VC: Viper Commandos
    ["SG-22 Bushwhacker"],\
    #FF: Freedom's Flame
    ["P-72 Crisper"],\
    #CA: Chemical Agents
    ["P-11 Stim Pistol"],\
    #TE: Truth Enforcers
    ["PLAS-15 Loyalist"],\
    #UL: Urban Legends
    ["CQC-19 Stun Lance"],\
    #End Warbonds
    #SUPER_CITIZEN:
    [],\
    #SUPER_STORE:
    ["CQC-30 Stun Baton"],\
    #PRE_ORDER:
    []]
ALL_THROWABLE = [\
    #STARTING: starting equipment, including Liberty Day rewards and
    # other content given to all players for free
    ["G-12 High Explosive"],\
    #HM: Helldivers Mobilize
    ["G-6 Frag", "G-16 Impact", "G-3 Smoke"],\
    #KXCO: Killzone cross-over free rewards
    [],\
    #SV: Steeled Veterans
    ["G-10 Incendiary"],\
    #CE: Cutting Edge
    ["G-23 Stun"],\
    #DD: Democratic Detonation
    ["G-123 Thermite"],\
    #PP: Polar Patriots
    ["G-13 Incendiary Impact"],\
    #VC: Viper Commandos
    ["K-2 Throwing Knife"],\
    #FF: Freedom's Flame
    [],\
    #CA: Chemical Agents
    ["G-4 Gas"],\
    #TE: Truth Enforcers
    [],\
    #UL: Urban Legends
    [],\
    #End Warbonds
    #SUPER_CITIZEN:
    [],\
    #SUPER_STORE:
    [],\
    #PRE_ORDER:
    []]
ALL_BOOSTERS = [\
    #STARTING: starting equipment, including Liberty Day rewards and
    # other content given to all players for free
    [],\
    #HM: Helldivers Mobilize
    ["Hellpod Space Optimization", "Vitality Enhancement", "UAV Recon Booster",\
    "Stamina Enhancement", "Muscle Enhancement", "Increased Reinforcement Budget"],\
    #KXCO: Killzone cross-over free rewards
    [],\
    #SV: Steeled Veterans
    ["Flexible Reinforcement Budget"],\
    #CE: Cutting Edge
    ["Localization Confusion"],\
    #DD: Democratic Detonation
    ["Expert Extraction Pilot"],\
    #PP: Polar Patriots
    ["Motivational Shocks"],\
    #VC: Viper Commandos
    ["Experimental Infusion"],\
    #FF: Freedom's Flame
    ["Firebomb Hellpods"],\
    #CA: Chemical Agents
    [],\
    #TE: Truth Enforcers
    ["Dead Sprint"],\
    #UL: Urban Legends
    ["Armed Resupply Pods"],\
    #End Warbonds
    #SUPER_CITIZEN:
    [],\
    #SUPER_STORE:
    [],\
    #PRE_ORDER:
    []]
ALL_ARMOR = [\
    #STARTING: starting equipment, including Liberty Day rewards and
    # other content given to all players for free
    ["B-01 Tactical", "B-01 Tactical", "B-01 Tactical", "B-01 Tactical",\
    "DP-00 Tactical", "TR-40 Gold Eagle", "TR-117 Alpha Commander"],\
    #HM: Helldivers Mobilize
    ["SC-34 Infiltrator", "SC-30 Trailblazer Scout", "CE-35 Trench Engineer", "CM-09 Bonesnapper",\
    "DP-40 Hero of the Federation", "SA-04 Combat Technician", "CM-14 Physician",\
    "DP-11 Champion of the People", "FS-05 Marksman", "FS-23 Battle Master"],\
    #KXCO: Killzone cross-over free rewards
    ["AC-2 Obedient"],\
    #SV: Steeled Veterans
    ["SA-25 Steel Trooper", "SA-12 Servo Assisted", "SA-32 Dynamo"],\
    #CE: Cutting Edge
    ["EX-00 Prototype X", "EX-03 Prototype 3", "EX-15 Prototype 16"],\
    #DD: Democratic Detonation
    ["CE-07 Demolition Specialist", "CE-27 Ground Breaker", "FS-55 Devastator"],\
    #PP: Polar Patriots
    ["CW-4 Arctic Ranger", "CW-36 Winter Warrior", "CW-22 Kodiak"],\
    #VC: Viper Commandos
    ["PH-9 Predator", "PH-202 Twigsnapper"],\
    #FF: Freedom's Flame
    ["I-09 Heatseeker", "I-102 Draconaught"],\
    #CA: Chemical Agents
    ["AF-50 Noxious Ranger", "AF-02 Haz-Master"],\
    #TE: Truth Enforcers
    ["UF-16 Inspector", "UF-50 Bloodhound"],\
    #UL: Urban Legends
    ["SR-24 Street Scout", "SR-18 Roadblock"],\
    #End Warbonds
    #SUPER_CITIZEN:
    ["DP-53 Savior of the Free"],\
    #SUPER_STORE:
    ["CS-37 Legionnaire", "CE-74 Breaker", "FS-38 Eradicator", "B-08 Light Gunner",\
    "CM-21 Trench Paramedic", "CE-67 Titan", "FS-37 Ravager",\
    "SC-15 Drone Master", "B-24 Enforcer", "CE-81 Juggernaut", "FS-34 Exterminator",\
    "CM-10 Clinician", "CW-9 White Wolf", "PH-56 Jaguar", "I-92 Fire Fighter",\
    "AF-91 Field Chemist", "UF-84 Doubt Killer", "AC-1 Dutiful",\
    "B-27 Fortified Commando", "FS-61 Dreadnought", "FS-11 Executioner",\
    "CM-17 Butcher", "CE-64 Grenadier", "CE-101 Guerilla Gorilla", "I-44 Salamander",\
    "AF-52 Lockdown", "SR-64 Cinderblock"],\
    #PRE_ORDER:
    ["TR-7 Ambassador of the Brand", "TR-9 Cavalier of Democracy", "TR-62 Knight"]]
ALL_CAPES = [\
    #STARTING: starting equipment, including Liberty Day rewards and
    # other content given to all players for free
    ["Foesmasher"],\
    #HM: Helldivers Mobilize
    ["Independence Bringer", "Liberty's Herald", "Tideturner",\
    "The Cape of Stars and Suffrage", "Unblemished Allegiance", "Judgement Day",\
    "Cresting Honor", "Mantle of True Citizenship", "Blazing Samaritan",\
    "Light of Eternal Liberty", "Fallen Hero's Vengeance"],\
    #KXCO: Killzone cross-over free rewards
    ["Defender of Our Dream"],\
    #SV: Steeled Veterans
    ["Tyrant Hunter", "Cloak of Posterity's Gratitude",\
    "Drape of Glory", "Bastion of Integrity"],\
    #CE: Cutting Edge
    ["Botslayer", "Martyris Rex", "Agent of Oblivion"],\
    #DD: Democratic Detonation
    ["Harbinger of True Equality", "Eagle's Fury", "Freedom's Tapestry"],\
    #PP: Polar Patriots
    ["Dissident's Nightmare", "Pinions of Everlasting Glory",\
    "Order of the Venerated Ballot"],\
    #VC: Viper Commandos
    ["Mark of the Crimson Fang", "Executioner's Canopy"],\
    #FF: Freedom's Flame
    ["Purifying Eclipse", "The Breach"],\
    #CA: Chemical Agents
    ["Standard of Safe Distance", "Patient Zero's Remembrance"],\
    #TE: Truth Enforcers
    ["Pride of the Whistleblower", "Proof of Faultless Virtue"],\
    #UL: Urban Legends
    ["Greatcloak of Rebar Resolve", "Holder of the Yellow Line"],\
    #End Warbonds
    #SUPER_CITIZEN:
    ["Will of the People"],\
    #SUPER_STORE:
    ["Cover of Darkness", "Stone-Wrought Perseverance"],\
    #PRE_ORDER:
    []]

WEIGHTS = [10, 9, 9, 9, 9, 9, 2, 3]

#Whether or not to randomize armor
EXTRA = False
#Whether or not to run program for debugging or usage
DEBUG = False

def sum_lists(l: list[int | list], options: list[int]) -> int:
    """returns sum of specified nested lists"""
    sums = 0
    for _, selection in enumerate(options):
        if isinstance(l[selection], list):
            sums += len(l[selection])
        else:
            sums += l[selection]
    return sums

def randomize_options(players: list[groups.Possessions], options: list,\
                          nums: int, extra: bool) -> str:
    """randomize equipment and stratagem loadouts for players"""
    assert nums >= 1, "Error in randomize_options_str: nums must be 1 or greater"

    results = []
    string = ""
    names_len = len(players)
    for i in range(0, names_len):
        for c in range(0, nums):
            selection = random.randint(0, (len(options) - 1))
            results.append(options[selection].pop(random.randint(0, (len(options[selection]) - 1))))
            if len(options[selection]) == 0:
                del options[selection]
    for i in range(0, names_len):
        string += f"{players[i].randomize_loadout_weapons()}\n"
        if extra:
            string += f"{players[i].randomize_loadout_other()}\n"
        string += f"{players[i].name}'s Stratagems: "
        for c in range(0, (nums-1)):
            string += f"{results[i*nums+c]}, "
        string += f"{results[i*nums+nums-1]}\n\n"
    return string

def randomize_options_new(players: list[groups.Possessions], opt: list,\
                          nums: int, weights: list[int]) -> str:
    """randomize equipment and stratagem loadouts for players"""
    assert nums >= 1, "Error in randomize_options_str: nums must be 1 or greater"

    options = opt
    string = ""
    names_len = len(players)
    weight_list = weights
    expended_lists = 0
    #emptied_lists = []
    # for every player:
    for i in range(0, names_len):
        string += f"{players[i].name}'s Stratagems: "
        results = []
        contents = players[i].strat_content
        for _ in range(expended_lists):
            del contents[len(contents)-1]
        #if len(emptied_lists) > 0:
            #for l in emptied_lists:
                #if l in contents:
                    #del contents[l]
        # for number of options to generate per player
        for _ in range(nums):
            select = random.randint(0, sum_lists(weight_list, contents) - 1)
            if select < weight_list[contents[0]]:
                select = random.randint(0, len(options[contents[0]]) - 1)
                results.append(options[contents[0]].pop(select))
                if len(options[contents[0]]) == 0:
                    del contents[len(contents)-1], weight_list[0], options[0]
                    expended_lists += 1
                    #emptied_lists.append(contents[0])
            else:
                for z in range(1, len(contents)):
                    if select < sum_lists(weight_list, contents[:(z+1)]):
                        # select -= sum_lists(options, contents[:z])
                        select = random.randint(0, len(options[contents[z]]) - 1)
                        results.append(options[contents[z]].pop(select))
                        if len(options[contents[z]]) == 0:
                            del contents[len(contents)-1], weight_list[z], options[z]
                            expended_lists += 1
                            #emptied_lists.append(contents[z])
                        break
        string += f"{str(results)}\n"
    return string

def randomize_options_new_new(players: list[groups.Possessions], opt: list,\
                          nums: int, weights: list[int]) -> str:
    """randomize equipment and stratagem loadouts for players"""
    assert nums >= 1, "Error in randomize_options_str: nums must be 1 or greater"

    options = opt
    string = ""
    names_len = len(players)
    weight_list = weights
    # expended_lists = 0
    emptied_lists = []
    # for every player:
    for i in range(0, names_len):
        string += f"{players[i].name}'s Stratagems: "
        results = []
        contents = players[i].strat_content
        # for _ in range(expended_lists):
            # del contents[len(contents)-1]
        if len(emptied_lists) > 0:
            for l in emptied_lists:
                if l in contents:
                    del contents[l]
        # for number of options to generate per player
        for _ in range(nums):
            select = random.randint(0, sum_lists(weight_list, contents) - 1)
            if select < weight_list[contents[0]]:
                select = random.randint(0, len(options[contents[0]]) - 1)
                results.append(options[contents[0]].pop(select))
                if len(options[contents[0]]) == 0:
                    del contents[len(contents)-1], weight_list[0]#, options[0]
                    # expended_lists += 1
                    emptied_lists.append(contents[0])
            else:
                for z in range(1, len(contents)):
                    if select < sum_lists(weight_list, contents[:(z+1)]):
                        # select -= sum_lists(options, contents[:z])
                        select = random.randint(0, len(options[contents[z]]) - 1)
                        results.append(options[contents[z]].pop(select))
                        if len(options[contents[z]]) == 0:
                            del contents[len(contents)-1], weight_list[z]#, options[z]
                            # expended_lists += 1
                            emptied_lists.append(contents[z])
                        break
        string += f"{str(results)}\n"
    return string

def randomize_results(options: list, nums: int) -> str:
    """FIXME"""
    string = ""
    for _ in range(0, nums - 1):
        selection = random.randint(0, (len(options) - 1))
        string += str(options[selection].pop(random.randint(0, (len(options[selection]) - 1))))
    selection = random.randint(0, (len(options) - 1))
    string += str(options[selection].pop(random.randint(0, (len(options[selection]) - 1))))

if __name__ == "__main__":
    print()
    example = groups.Possessions("name", [STARTING, HM, KXCO],\
                                [],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)

    robert = groups.Possessions("Robert", [STARTING, HM, KXCO, CE, DD],\
                                [],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)
    jamison = groups.Possessions("Jamison", [STARTING, HM, KXCO, CE, DD],\
                                [],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)
    caleb = groups.Possessions("Caleb", [STARTING, HM, KXCO, DD, CA],\
                                [CHEMICAL_AGENTS],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)
    tiernan = groups.Possessions("Tiernan", [STARTING, HM, KXCO, PP, UL],\
                                [URBAN_LEGENDS],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)
    josh = groups.Possessions("Josh", [STARTING, HM, KXCO],\
                                [],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)
    hayden = groups.Possessions("Hayden", [STARTING, HM, KXCO, SV, CE, DD, PP, VC, FF, UL],\
                                [URBAN_LEGENDS],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)
    wilson = groups.Possessions("Wilson", [STARTING, HM, KXCO, CE, DD, SUPER_CITIZEN],\
                                [],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)

    loadout = groups.Possessions("Loadout", [STARTING, HM, KXCO],\
                                [],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)

    almight = groups.Possessions("Almight", [STARTING, HM, KXCO, SV, CE, DD, PP, VC, FF, CA, TE, UL,\
                                             SUPER_CITIZEN, SUPER_STORE, PRE_ORDER],\
                                [CHEMICAL_AGENTS, URBAN_LEGENDS],\
                                ALL_PRIMARY, ALL_SECONDARY, ALL_THROWABLE, ALL_STRATAGEMS,\
                                ALL_BOOSTERS, ALL_ARMOR, ALL_CAPES)

    if DEBUG:
        divers = [robert, hayden]
        stratagems = DEBUG_LIST[:8]
        output = randomize_options_new(divers, stratagems, 4, WEIGHTS)
        print(output)

    if not DEBUG:
        divers = [robert, hayden, caleb, tiernan]
        # divers = [loadout, loadout]
        stratagems = ALL_STRATAGEMS[:8]
        output = randomize_options_new(divers, stratagems, 4, WEIGHTS)
        pyperclip.copy(output)
        print(output)
