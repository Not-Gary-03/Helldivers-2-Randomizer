"""Helldivers Equipment Randomizer
Gary Hayden May, 2025/01/10, Personal Project

////2025-12-13 PLANS FOR EXPANSION////
- add function for adding new content from user input, automatically updating data files and
    the ACQUISITIONS and STRAT_TITLES lists

////2025-12-17 TODO////
- update killzone collab content to reflect recent changes
- make priority list option play nice with new warbonds

////2025-12-08 TODO////
- update input menu with more options:
    - add tag(s) to item(s) including collection items
    - add/remove item(s) from collection(s)
    - save player collections in text files for easier updating and saving

potential example of menu:
[A]: Randomize!
[B]: Modify Content
[X]: Exit

-> [A] Randomize Menu:
[1]: Choose Divers
[2]: Choose Weight Option
[3]: Randomize!
[X]: Back to Main Menu

    -> [1] Choose Divers Menu:
    Diver Names:
    # this'll be saved to a list, if there were items in the list already they'll be replaced

    -> [2] Choose Weight Option Menu:
    [a: fully random]
    [b: priority list]
    [c: random category weights]
    [X: cancel]

    -> [3] Randomize Menu:
    [a: get loadouts]
    [b: refresh collections]
    [X: back to main menu]

-> [B] Modify Content Menu:
[1]: Add New Warbond
[2]: Modify Collection or Item
[X]: Back to Main Menu

    -> [1] Add New Warbond Menu:
    Warbond Name:
    Item Type?
    [a: armor] [b: booster] [c: cape]
    [d: helmet] [e: primary] [f: secondary]
    [g: stratagem] [h: throwable]
    [X: finish]
    # repeat item add until finish is selected, saving each item to corresponding data file

    -> [2] Modify Collection or Item Menu:
    # display list of viable collections and items with index numbers
    Choose Index: 
    -> once index is chosen:
    #if item:
    [a: add tag]
    [b: remove tag]
    [c: change weight]
    [X: back]
    # repeat until back is selected
    #if collection:
    [a: add item]
    [b: remove item]
    [c: add tag to collection]
    [d: remove tag from collection]
    [e: add tag to all items in collection]
    [f: remove tag from all items in collection]
    [g: change weight]
    [X: back]

////2025-12-25 TODO////
- make new randomize functions using weight instead of item removal

////2025-12-30 TODO////
- COMPLETED new rand_equipment function. It now operates by modifying weights instead of removing items.
- next task: update weight options

////2026-01-03 TODO////
- update priority weight options; better way of aggregating for stratagems/etc.
"""

import random
import csv
import pyperclip
import ast

from item import Item
from collection import Collection
from manager import Manager

DEBUG = False

ACQUISITIONS = ["starting equipment","killzone cross over","Helldivers Mobilize",\
            "Steeled Veterans","Cutting Edge","Democratic Detonation","Polar Patriots",\
            "Viper Commandos","Freedom's Flame","Chemical Agents","Truth Enforcers",\
            "Urban Legends","Servants of Freedom","Borderline Justice","Masters of Ceremony",\
            "Dust Devils","Obedient Democracy Support Troopers","Control Group",\
            "Force of Law","Python Commandos",\
            "Super Store","Super Citizen Edition","pre order"]
STRAT_TITLES = ["Patriotic Administration Center","Hangar","Bridge",\
            "Robotics Workshop","Engineering Bay","Orbital Cannons",\
            "Chemical Agents","Urban Legends","Servants of Freedom",\
            "Borderline Justice","Masters of Ceremony","Dust Devils",\
            "Control Group","Force of Law","Python Commandos",\
            "Obedient Democracy Support Troopers"]

#region function definitions

def read_items_from_csv(filename) -> list:
    """reads from text file and returns list of Item objects"""
    items = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            tags_field = row['tags']
            # Remove surrounding quotes if present
            if tags_field.startswith('"') and tags_field.endswith('"'):
                tags_field = tags_field[1:-1]
            try:
                tags = ast.literal_eval(tags_field)
                if not isinstance(tags, list):
                    tags = []
            except Exception:
                tags = []
            items.append(Item(name, tags))
    return items

def read_divers_from_csv(filename, base_stratagem_names=None, base_content_unlocked=None) -> list:
    """Reads divers from a CSV file and returns a list of Item objects.
    Each diver will have the base stratagem names and base content unlocked tags appended.
    Skips rows with empty or 'Example' name."""
    divers = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get('name','').strip()
            if not name or name.lower() == 'example':
                continue
            tags_raw = row.get('tags','')
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
            # append base tags if provided
            base_tags = []
            if base_stratagem_names:
                base_tags.extend(base_stratagem_names)
            if base_content_unlocked:
                base_tags.extend(base_content_unlocked)
            tags = [*base_tags, *tags]
            try:
                weight = int(row.get('weight','1')) if row.get('weight') else 1
            except ValueError:
                weight = 1
            divers.append(Item(name, tags, weight))
    return divers

def rand_weights(base_col: Collection,l_range: int,u_range: int) -> str:
    # Randomly modifies the weights of each Item in a Collection
    output = ""
    for i,item in enumerate(base_col.items):
        new_weight = random.randint(l_range,u_range)
        base_col.alter_weight(i,new_weight)
        if new_weight > 0:
            output += f"{item.name} weight: {item.weight}\n"
    return output

def rand_weights_priority_list(base_col: Collection,weight_list: list) -> str:
    # Randomly modifies the weights of each Item in a Collection
    assert len(weight_list) <= len(base_col.items), "Error, length of weight list must be less than or equal to length of item list"

    while len(weight_list) < len(base_col.items):
        weight_list.append(0)

    output = ""
    for _,item in enumerate(base_col.items):
        selection = random.randint(0, len(weight_list)-1)
        item.weight = weight_list[selection]
        if weight_list[selection] > 0:
            output += f"{item.name} weight: {item.weight}\n"
        del weight_list[selection]
    return output

def create_col_list_or(name: str,base: Collection, categories: list) -> Collection:
    """creates a Collection containing a list of collections, each with a single associated tag"""
    lst = []
    mn = Manager()
    for _,category in enumerate(categories):
        buffer = mn.aggregate_or(base,[category])
        buffer.name = category
        buffer.tags = [category]
        buffer.weight = len(buffer.items)
        lst.append(buffer)
    result = Collection(name,categories,items=lst)
    result.refresh_weight() #FIXME band-aid solution, make this better
    return result

def rand_equipment(base_col: Collection, player_tag_item: Item, destructive=False) -> str:
    """Returns the name of one item randomly selected from base_col using weighted selection.
    SIDE EFFECT: modifies weight of items in base_col.
    base_col: the collection of items that we will be selecting from
    player_tag_item: item object identifying the player, their name, and tags indicating the content
      they own
    destructive: determines if selected item will have its weight set to zero. False by default
    """

    # Get viable collections that contain at least one of the tag_item's tags
    print(f"[DEBUG] rand_equipment: Searching for tags {player_tag_item.tags} in base_col '{base_col.name}' with {len(base_col.items)} items.")
    viables = base_col.aggregate_or(player_tag_item.tags, recursive=True)
    print(f"[DEBUG] rand_equipment: Found {len(viables.items)} viable items: {[item.name for item in viables.items]}")

    if DEBUG:
        print(viables)

    if not viables.items:
        raise ValueError(f"No viable items found for diver '{player_tag_item.name}' with tags {player_tag_item.tags} in collection '{base_col.name}'")

    # Randomly select an item from viables
    selected_item = viables.rand_select_item()
    if destructive: # if destructive, set selected item weight to zero in base_col
        base_col.remove_i_weight(selected_item)

    return f"[{selected_item.name}]"

def team_loadouts(divers: list[Collection],content: list,ds=False) -> str:
    """randomly create full loadout for each diver
    divers: list of Item objects representing the divers, their names, and tags indicating the content they own
    content: list of Collection objects representing all of the equipment in the game
    ds: boolean indicating if destructive selection is enabled
    """
    output = ""
    for diver in divers:
        output += f"{diver.name}'s Stratagems: "
        output += f"{rand_equipment(content[0],diver,ds)} "
        output += f"{rand_equipment(content[0],diver,ds)} "
        output += f"{rand_equipment(content[0],diver,ds)} "
        output += f"{rand_equipment(content[0],diver,ds)}\n"
        output += f"{diver.name}'s Armor: {rand_equipment(content[1],diver,ds)} "
        output += f"Primary: {rand_equipment(content[2],diver,ds)} "
        output += f"Secondary: {rand_equipment(content[3],diver,ds)}\n"
        output += f"{diver.name}'s Throwable: {rand_equipment(content[4],diver,ds)} "
        output += f"Booster: {rand_equipment(content[5],diver,ds)}\n\n"
        # appends fully randomized loadout for a single diver to the output string, repeats for
        # each Item in the divers list
    return output.strip()

def priority_list_weights(col: Collection) -> str:
    """modifies weights of items in col based on a list of qualifying tags and a list of integer weights,
    assigning items of a given tag the corresponding weight from the weight list.
    col: Collection object containing items to modify
    SIDE EFFECT: modifies weights of items in col, sets all item weights to base_weight before other modifications
    
    PSEUDOCODE:

    prompt user for list of tags, should include option to choose common categories
        Common categories include: base stratagem categories plus warbonds, rgb stratagems
    
    prompt user for list of integer weights, separated by spaces
    if list length is less than number of tags, append base_weight until lengths match

    prompt user for new base weight
    set weight of every item in col to new base weight

    for each tag in tag list:
        randomly select weight from weight list and remove it from the list
        aggregate collection for items with this tag
        assign each item from the base collection that is in the aggregated collection the new weight

    """
    print("Tag selection options:\n[1: base stratagem categories]\n[2: rgb stratagems]")
    tag_option = input("[3: warbond titles]\n[4: custom tags]\nInput selection: ").strip()
    tags = None
    match tag_option:
        case '1':
            tags = ["Patriotic Administration Center","Hangar","Bridge",\
            "Robotics Workshop","Engineering Bay","Orbital Cannons","warbond"]
        case '2':
            tags = ["red","green","blue"]
        case '3':
            tags = ["Steeled Veterans","Cutting Edge","Democratic Detonation","Polar Patriots",\
            "Viper Commandos","Freedom's Flame","Chemical Agents","Truth Enforcers",\
            "Urban Legends","Servants of Freedom","Borderline Justice","Masters of Ceremony",\
            "Dust Devils","Obedient Democracy Support Troopers","Control Group",\
            "Force of Law","Python Commandos"]
        case '4':
            tags = list(map(str, input("Input tag list, separated by spaces: ").split()))

    weights = list(map(int, input("Input weight list, separated by spaces: ").split()))

    base_weight = input("new base weight? [Y/N]: ").strip().upper()
    if base_weight == 'Y':
        base_weight = input("Input new base weight for all items: ")
        col.set_weights(base_weight)

    if len(weights) < len(tags):
        while len(weights) < len(tags):
            weights.append(0)

    str_output = ""

    for _,tag in enumerate(tags):
        selection = random.choice(weights)
        weights.remove(selection)
        str_output += f"{tag} weight: {selection}\n"
        # agg_col = col.aggregate_or([tag], recursive=True)
        # print(f"aggregated collection for tag '{tag}':\n{agg_col}\n")
        # for _,item in enumerate(agg_col.items):
        #     print(f"{col.items[item]} found in aggregated collection, its weight is currently {col.items[item].weight}, setting to {selection}\n")
        #     col.items[item].weight = selection
        #     print(f"new weight: {col.items[item].weight}\n")
        for _,item in enumerate(col.items):
            if tag in item.tags:
                print(f"{item} has tag '{tag}', its weight is currently {item.weight}, setting to {selection}\n")
                item.weight = selection
                print(f"new weight: {item.weight}\n")
            
    
    return str_output

#endregion

# read all equipment from a single data file
equipment_items = read_items_from_csv("data\\all_equipment.txt")

# Initialize collections from the single equipment source so the module can be imported and used
# by other code without needing to run the interactive main loop.
equipment_col = Collection("everything",["everything_col"],1,equipment_items)

# derive type-specific collections as views onto equipment_col (share Item objects)
stratagem_col = equipment_col.aggregate_or(["stratagem"], recursive=True)
stratagem_col.name = "stratagems"
stratagem_col.tags = ["stratagems_col"]
stratagem_col.refresh_weight()

armor_col = equipment_col.aggregate_or(["armor"], recursive=True)
armor_col.name = "armor"
armor_col.tags = ["armor_col"]
armor_col.refresh_weight()

primary_col = equipment_col.aggregate_or(["primary"], recursive=True)
primary_col.name = "primary"
primary_col.tags = ["primary_col"]
primary_col.refresh_weight()

secondary_col = equipment_col.aggregate_or(["secondary"], recursive=True)
secondary_col.name = "secondary"
secondary_col.tags = ["secondary_col"]
secondary_col.refresh_weight()

throwable_col = equipment_col.aggregate_or(["throwable"], recursive=True)
throwable_col.name = "throwable"
throwable_col.tags = ["throwable_col"]
throwable_col.refresh_weight()

booster_col = equipment_col.aggregate_or(["booster"], recursive=True)
booster_col.name = "booster"
booster_col.tags = ["booster_col"]
booster_col.refresh_weight()


# Keep all_* collections for other uses, but use flat collections for randomization
all_stratagems = create_col_list_or("Stratagems",stratagem_col, STRAT_TITLES)
all_armor = create_col_list_or("Armor",armor_col,ACQUISITIONS)
all_primaries = create_col_list_or("Primaries",primary_col,ACQUISITIONS)
all_secondaries = create_col_list_or("Secondaries",secondary_col,ACQUISITIONS)
all_throwables = create_col_list_or("Throwables",throwable_col,ACQUISITIONS)
all_boosters = create_col_list_or("Boosters",booster_col,ACQUISITIONS)

base_stratagem_names = ["Patriotic Administration Center","Hangar","Bridge",\
                        "Robotics Workshop","Engineering Bay","Orbital Cannons"]
base_content_unlocked = ["starting equipment","Helldivers Mobilize","killzone cross over"]

# Use flat collections for randomization
content = [stratagem_col, armor_col, primary_col, secondary_col, throwable_col, booster_col]

if __name__ == "__main__":
    #region Collection initialization
    # Use single equipment collection as parent and derive other collections from it
    equipment_col = Collection("everything",["everything_col"],1,equipment_items)

    # derive type-specific collections as views onto equipment_col (share Item objects)
    stratagem_col = equipment_col.aggregate_or(["stratagem"], recursive=True)
    stratagem_col.name = "stratagems"
    stratagem_col.tags = ["stratagems_col"]
    stratagem_col.refresh_weight()

    armor_col = equipment_col.aggregate_or(["armor"], recursive=True)
    armor_col.name = "armor"
    armor_col.tags = ["armor_col"]
    armor_col.refresh_weight()

    primary_col = equipment_col.aggregate_or(["primary"], recursive=True)
    primary_col.name = "primary"
    primary_col.tags = ["primary_col"]
    primary_col.refresh_weight()

    secondary_col = equipment_col.aggregate_or(["secondary"], recursive=True)
    secondary_col.name = "secondary"
    secondary_col.tags = ["secondary_col"]
    secondary_col.refresh_weight()

    throwable_col = equipment_col.aggregate_or(["throwable"], recursive=True)
    throwable_col.name = "throwable"
    throwable_col.tags = ["throwable_col"]
    throwable_col.refresh_weight()

    booster_col = equipment_col.aggregate_or(["booster"], recursive=True)
    booster_col.name = "booster"
    booster_col.tags = ["booster_col"]
    booster_col.refresh_weight()

    if DEBUG:
        print(f"equipment_col:\n{equipment_col}\n")
        print(f"stratagem_col:\n{stratagem_col}\n")
        print(f"armor_col:\n{armor_col}\n")
        print(f"primary_col:\n{primary_col}\n")
        print(f"secondary_col:\n{secondary_col}\n")
        print(f"throwable_col:\n{throwable_col}\n")
        print(f"booster_col:\n{booster_col}\n")

    all_stratagems = create_col_list_or("Stratagems",stratagem_col, STRAT_TITLES)
    all_armor = create_col_list_or("Armor",armor_col,ACQUISITIONS)
    all_primaries = create_col_list_or("Primaries",primary_col,ACQUISITIONS)
    all_secondaries = create_col_list_or("Secondaries",secondary_col,ACQUISITIONS)
    all_throwables = create_col_list_or("Throwables",throwable_col,ACQUISITIONS)
    all_boosters = create_col_list_or("Boosters",booster_col,ACQUISITIONS)

    base_stratagem_names = ["Patriotic Administration Center","Hangar","Bridge",\
                            "Robotics Workshop","Engineering Bay","Orbital Cannons"]
    base_content_unlocked = ["starting equipment","Helldivers Mobilize","killzone cross over"]

    #content = [all_stratagems,all_armor,all_primaries,all_secondaries,all_throwables,\
    #           all_boosters]
    content = [stratagem_col,armor_col,primary_col,secondary_col,throwable_col,\
               booster_col]
    
    #endregion

    #region PLAYER OPTIONS
    # Load divers from data\divers.txt so player options are configurable outside the program
    DIVERS = read_divers_from_csv("data\\divers.txt", base_stratagem_names, base_content_unlocked)
    # For backward compatibility allow referencing divers as globals by name
    for diver in DIVERS:
        globals()[diver.name] = diver

    #endregion

    INPUT_MODE = True
    ACTIVE = True

    #region Base Input Mode
    while ACTIVE:
        if INPUT_MODE:
            d_input = list(map(str, input("Who's diving? ").split()))
                # expects diver names separated by spaces
            # perform case-insensitive lookup against DIVERS list
            name_map = {d.name.lower(): d for d in DIVERS}
            divers = [name_map[name.lower()] for name in d_input if name.lower() in name_map]
                # creates list of Item objects based on diver names input by user
                # ignores invalid names

            weight_option = int(input("Weight options [0: none][1: priority list][2: rand weights]\nChoose an option: "))
            if weight_option < 0 or weight_option > 2:
                weight_option = 0
        else:
            # default team when input mode is off — use first four divers from DIVERS file
            divers = DIVERS[:4]

            weight_option = 0

        if weight_option == 1:      #PRIOITY LIST RANDOMIZATION
            weights = priority_list_weights(stratagem_col)
            """all_stratagems = everything_col.aggregate_or(["stratagem"], recursive=True)
            all_armor = everything_col.aggregate_or(["armor"], recursive=True)
            all_primaries = everything_col.aggregate_or(["primary"], recursive=True)
            all_secondaries = everything_col.aggregate_or(["secondary"], recursive=True)
            all_throwables = everything_col.aggregate_or(["throwable"], recursive=True)
            all_boosters = everything_col.aggregate_or(["booster"], recursive=True)"""
            content = [stratagem_col,all_armor,all_primaries,all_secondaries,all_throwables,\
               all_boosters]
            
        elif weight_option == 2:    #NORMAL WEIGHT RANDOMIZATION
            weights = rand_weights(all_stratagems,0,3)

        output = team_loadouts(divers,content, True)
        # divers is a list of Item objects representing each diver
        # content is a list of Collection objects representing all of the equipment in the game,
        # organized by type (stratagems, armor, primary, secondary, throwable, booster)

        if weight_option != 0:
            output += f"\n\n{weights}"

        print(output)
        pyperclip.copy(output)
        if INPUT_MODE:
            temp = input("Again? [Y/N]: ")
            print('\n')
            if temp.lower() != 'y':
                ACTIVE = False
        else:
            ACTIVE = False
    #endregion"""

    #region New Input Mode

    ACTIVE = False

    divers = []
    weight_option = 0
    weights = None

    while ACTIVE:
        print("[A]: Randomize!\n[B]: Modify Content\n[X]: Exit")
        d_input = input("Choose: ").strip().upper()
        # get user input
        # .strip() removes leading and trailing whitespaces
        # .upper() makes all characters uppercase

        match d_input:
            case 'A': #Randomize!
                #region Randomize Menu
                print("[1]: Choose Divers\n[2]: Choose Weight Option\n[3]: Randomize!\n[X]: Back to Main Menu")
                d_input = input("Choose: ").strip().upper()
                    # get user input
                    # .strip() removes leading and trailing whitespaces
                    # .upper() makes all characters uppercase
                match d_input:
                    case '1': #Choose Divers
                        d_input = list(map(str, input("Who's diving? ").split()))
                            # expects diver names separated by spaces
                            # FIXME: comment explain how this works
                        divers = [globals().get(name) for name in d_input if globals().get(name) is not None]
                            # creates list of Item objects based on diver names input by user
                            # ignores invalid names
                            # FIXME: comment explain how this works

                    case '2': #Choose Weight Option
                        print("[a: fully random]\n[b: priority list]\n[c: random category weights]\n[X: cancel]")
                        d_input = input("Choose: ").strip().upper()
                            # get user input
                            # .strip() removes leading and trailing whitespaces
                            # .upper() makes all characters uppercase
                        match d_input:
                            case 'A': #fully random
                                weight_option = 0
                            case 'B': #priority list
                                weight_option = 1
                            case 'C': #random category weights
                                weight_option = 2
                            case 'X': #cancel
                                pass

                    case '3': #Randomize!
                        print("[a: get loadouts]\n[b: refresh collections]\n[X: back to main menu]")
                        d_input = input("Choose: ").strip().upper()
                            # get user input
                            # .strip() removes leading and trailing whitespaces
                            # .upper() makes all characters uppercase
                        match d_input:
                            case 'A': #get loadouts
                                output = team_loadouts(divers,content)
                                # divers is a list of Item objects representing each diver
                                # content is a list of Collection objects representing all of the equipment in the game,
                                # organized by type (stratagems, armor, primary, secondary, throwable, booster)

                                if weight_option != 0:
                                    output += f"\n\n{weights}"

                                print(output)
                                pyperclip.copy(output)

                            case 'B': #refresh collections
                                pass
                            case 'X': #back to main menu
                                pass
                    case 'X': #Back to Main Menu
                        # Back to Main Menu
                        pass
                #endregion

            case 'B': #Modify Content
                #region Modify Content Menu
                print("[1]: Add New Warbond\n[2]: Modify Collection or Item\n[X]: Back to Main Menu")
                d_input = input("Choose: ").strip().upper()
                    # get user input
                    # .strip() removes leading and trailing whitespaces
                    # .upper() makes all characters uppercase
                match d_input:
                    case '1': #Add New Warbond
                        warbond_name = input("Warbond Name: ").strip()
                        loop = True
                        while loop:
                            print("Item Type?")
                            print("[a: armor] [b: booster] [c: cape]")
                            print("[d: helmet] [e: primary] [f: secondary]")
                            print("[g: stratagem] [h: throwable]")
                            print("[X: finish]")
                            item_type = input("Choose: ").strip().upper()
                            match item_type:
                                case 'A': #armor
                                    pass
                                case 'B': #booster
                                    pass
                                case 'C': #cape
                                    pass
                                case 'D': #helmet
                                    pass
                                case 'E': #primary
                                    pass
                                case 'F': #secondary
                                    pass
                                case 'G': #stratagem
                                    pass
                                case 'H': #throwable
                                    pass
                                case 'X': #finish
                                    loop = False
                    case '2': #Modify Collection or Item
                        # display list of viable collections and items with index numbers
                        # choose index, get different options based on if collection or item
                        pass
                    case 'X': #Back to Main Menu
                        pass
                #endregion

            case 'X': #Exit
                ACTIVE = False

            case 'D': #Debug
                testlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                weightlist = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0]
                output = random.choices(testlist, weights=weightlist, k=50)
                print(output)
                output = []
                for _ in range(50):
                    output.append(f"{random.choice(testlist)} ")
                print(output)
    #endregion"""
