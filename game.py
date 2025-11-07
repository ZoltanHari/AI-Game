# -*- coding: utf-8 -*-
"""
TF2: The Text Adventure
A text-based RPG in Python based on Team Fortress 2.
"""

import random
import time
import sys

# ### Helper Functions ###

def print_slow(text, speed=0.03):
    """Prints text one character at a time for a dramatic effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print() # Newline after message

def clear_screen():
    """Prints 50 newlines to simulate clearing the screen."""
    print("\n" * 50)

def get_input(prompt):
    """
    Wrapper for input() to standardize grabbing user commands.
    Handles 'quit', 'stats', and 'inventory' as global commands.
    """
    while True:
        choice = input(f"\n{prompt}\n> ").strip().lower()
        if choice == 'quit':
            print_slow("See you on the battlefield, mercenary.")
            sys.exit()
        return choice

# ### Data Definitions (Classes, Weapons, Enemies) ###

# Weapons: 'damage' (min, max), 'accuracy' (0-100), 'desc' (flavor text)
# 'utility': True marks non-damaging items for special combat handling
WEAPONS = {
    # --- Universal ---
    'shotgun': {'name': 'Shotgun', 'damage': (40, 70), 'accuracy': 85, 'desc': 'Reliable crowd control.'},
    'pistol': {'name': 'Pistol', 'damage': (10, 20), 'accuracy': 90, 'desc': 'A trusty sidearm.'},

    # --- Scout ---
    'scattergun': {'name': 'Scattergun', 'damage': (60, 100), 'accuracy': 85, 'desc': 'High-damage at close range.'},
    'force_a_nature': {'name': 'Force-A-Nature', 'damage': (70, 110), 'accuracy': 80, 'desc': 'Packs a punch, and a knockback.'},
    'bonk': {'name': 'Bonk! Atomic Punch', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Grants 100% dodge for one turn.', 'utility': True},
    'bat': {'name': 'Bat', 'damage': (30, 40), 'accuracy': 95, 'desc': 'It\'s a bat.'},
    'sandman': {'name': 'Sandman', 'damage': (25, 35), 'accuracy': 95, 'desc': 'Slower, but has a cool logo.'},

    # --- Soldier ---
    'rocket_launcher': {'name': 'Rocket Launcher', 'damage': (70, 110), 'accuracy': 80, 'desc': 'Deals Explosive damage.'},
    'direct_hit': {'name': 'Direct Hit', 'damage': (90, 125), 'accuracy': 70, 'desc': 'High-speed, high-damage rocket.'},
    'buff_banner': {'name': 'Buff Banner', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Next attack deals 2x damage.', 'utility': True},
    'shovel': {'name': 'Shovel', 'damage': (55, 75), 'accuracy': 95, 'desc': 'For digging graves.'},
    'equalizer': {'name': 'Equalizer', 'damage': (50, 70), 'accuracy': 95, 'desc': 'Deals more damage as you get hurt.'},

    # --- Pyro ---
    'flamethrower': {'name': 'Flamethrower', 'damage': (70, 100), 'accuracy': 90, 'desc': 'Deals Fire damage. Mphm!'},
    'backburner': {'name': 'Backburner', 'damage': (80, 110), 'accuracy': 90, 'desc': 'Guaranteed crits from behind.'},
    'flare_gun': {'name': 'Flare Gun', 'damage': (25, 35), 'accuracy': 85, 'desc': 'Lights \'em up from a distance.'},
    'fire_axe': {'name': 'Fire Axe', 'damage': (55, 75), 'accuracy': 95, 'desc': 'For chopping... things.'},
    'axtinguisher': {'name': 'Axtinguisher', 'damage': (40, 50), 'accuracy': 95, 'desc': 'Crits burning targets.'},

    # --- Demoman ---
    'grenade_launcher': {'name': 'Grenade Launcher', 'damage': (80, 120), 'accuracy': 75, 'desc': 'Deals Explosive damage. Bouncy.'},
    'loch_n_load': {'name': 'Loch-n-Load', 'damage': (100, 130), 'accuracy': 70, 'desc': 'Fast-moving, direct-hit pills.'},
    'sticky_launcher': {'name': 'Stickybomb Launcher', 'damage': (70, 110), 'accuracy': 70, 'desc': 'Set traps and control areas.'},
    'chargin_targe': {'name': 'Chargin\' Targe', 'damage': (40, 50), 'accuracy': 90, 'desc': 'Grants passive resistances.'},
    'bottle': {'name': 'Bottle', 'damage': (55, 75), 'accuracy': 95, 'desc': 'Smash!' },
    'eyelander': {'name': 'Eyelander', 'damage': (60, 80), 'accuracy': 95, 'desc': 'A haunted sword that demands heads.'},

    # --- Heavy ---
    'minigun': {'name': 'Minigun', 'damage': (100, 140), 'accuracy': 75, 'desc': 'Costs $400,000 to fire for 12 seconds.'},
    'natascha': {'name': 'Natascha', 'damage': (90, 130), 'accuracy': 80, 'desc': 'Slows enemies on hit.'},
    'sandvich': {'name': 'Sandvich', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Heals 75 HP.', 'utility': True},
    'fists': {'name': 'Fists', 'damage': (60, 80), 'accuracy': 95, 'desc': 'These are my weapons.'},
    'kgb': {'name': 'K.G.B.', 'damage': (60, 80), 'accuracy': 95, 'desc': 'Killing Gloves of Boxing.'},

    # --- Engineer ---
    'frontier_justice': {'name': 'Frontier Justice', 'damage': (50, 80), 'accuracy': 85, 'desc': 'Crits based on Sentry kills.'},
    'wrench': {'name': 'Wrench', 'damage': (55, 75), 'accuracy': 95, 'desc': 'Builds, repairs, and whacks.'},
    'gunslinger': {'name': 'Gunslinger', 'damage': (40, 50), 'accuracy': 95, 'desc': 'Replaces Sentry with a Mini-Sentry.'},
    'pda_build': {'name': 'Build PDA', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Builds Dispensers, Sentries, and more.', 'utility': True},
    'pda_destroy': {'name': 'Destroy PDA', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Destroys your buildings.', 'utility': True},

    # --- Medic ---
    'syringe_gun': {'name': 'Syringe Gun', 'damage': (10, 20), 'accuracy': 85, 'desc': 'Fires a stream of needles.'},
    'blutsauger': {'name': 'Blutsauger', 'damage': (10, 20), 'accuracy': 85, 'desc': 'Heals you on-hit.'},
    'medigun': {'name': 'Medigun', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Heals 50 HP in combat.', 'utility': True},
    'kritzkrieg': {'name': 'Kritzkrieg', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Heals 30 HP and grants 1.5x damage next turn.', 'utility': True},
    'bonesaw': {'name': 'Bonesaw', 'damage': (55, 75), 'accuracy': 95, 'desc': 'The default melee.'},
    'ubersaw': {'name': 'Ubersaw', 'damage': (55, 75), 'accuracy': 95, 'desc': 'Grants Uber on-hit.'},

    # --- Sniper ---
    'sniper_rifle': {'name': 'Sniper Rifle', 'damage': (50, 150), 'accuracy': 70, 'desc': 'High-risk, high-reward. Aim for the head.'},
    'huntsman': {'name': 'Huntsman', 'damage': (40, 120), 'accuracy': 75, 'desc': 'A bow and arrow. Be a man.'},
    'smg': {'name': 'SMG', 'damage': (10, 25), 'accuracy': 85, 'desc': 'For close-quarters panic.'},
    'jarate': {'name': 'Jarate', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Enemy takes 1.5x damage next turn.', 'utility': True},
    'kukri': {'name': 'Kukri', 'damage': (55, 75), 'accuracy': 95, 'desc': 'A big knife.'},
    'bushwacka': {'name': 'Bushwacka', 'damage': (55, 75), 'accuracy': 95, 'desc': 'Crits when it would mini-crit.'},

    # --- Spy ---
    'revolver': {'name': 'Revolver', 'damage': (30, 50), 'accuracy': 90, 'desc': 'A very fancy sidearm.'},
    'ambassador': {'name': 'Ambassador', 'damage': (40, 60), 'accuracy': 80, 'desc': 'Rewards accuracy with headshots.'},
    'knife': {'name': 'Knife', 'damage': (35, 45), 'accuracy': 95, 'desc': 'For backstabbing. (Story-based)'},
    'your_eternal_reward': {'name': 'Your Eternal Reward', 'damage': (35, 45), 'accuracy': 95, 'desc': 'Instantly disguise on a backstab.'},
    'sapper': {'name': 'Sapper', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Disables and destroys enemy buildings. (Story-based)', 'utility': True},
    'invis_watch': {'name': 'Invisibility Watch', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Grants a very high chance to flee combat.', 'utility': True},
    'disguise_kit': {'name': 'Disguise Kit', 'damage': (0, 0), 'accuracy': 100, 'desc': 'Utility: Blend in with the enemy. (Story-based)', 'utility': True},
}

# Defines the weapon *options* for each class slot
WEAPON_CHOICES = {
    'scout': {
        'primary': ['scattergun', 'force_a_nature'],
        'secondary': ['pistol', 'bonk'],
        'melee': ['bat', 'sandman']
    },
    'soldier': {
        'primary': ['rocket_launcher', 'direct_hit'],
        'secondary': ['shotgun', 'buff_banner'],
        'melee': ['shovel', 'equalizer']
    },
    'pyro': {
        'primary': ['flamethrower', 'backburner'],
        'secondary': ['shotgun', 'flare_gun'],
        'melee': ['fire_axe', 'axtinguisher']
    },
    'demoman': {
        'primary': ['grenade_launcher', 'loch_n_load'],
        'secondary': ['sticky_launcher', 'chargin_targe'],
        'melee': ['bottle', 'eyelander']
    },
    'heavy': {
        'primary': ['minigun', 'natascha'],
        'secondary': ['shotgun', 'sandvich'],
        'melee': ['fists', 'kgb']
    },
    'engineer': {
        'primary': ['shotgun', 'frontier_justice'],
        'secondary': ['pistol'],
        'melee': ['wrench', 'gunslinger'],
        'pda': ['pda_build', 'pda_destroy'] # Purely cosmetic for loadout
    },
    'medic': {
        'primary': ['syringe_gun', 'blutsauger'],
        'secondary': ['medigun', 'kritzkrieg'],
        'melee': ['bonesaw', 'ubersaw']
    },
    'sniper': {
        'primary': ['sniper_rifle', 'huntsman'],
        'secondary': ['smg', 'jarate'],
        'melee': ['kukri', 'bushwacka']
    },
    'spy': {
        'primary': ['revolver', 'ambassador'],
        'melee': ['knife', 'your_eternal_reward'],
        'pda': ['invis_watch', 'disguise_kit'] # Sapper is granted by default
    },
}

# Classes define starting health, speed (for fleeing)
CLASSES = {
    'scout': {'name': 'Scout', 'health': 125, 'speed': 133},
    'soldier': {'name': 'Soldier', 'health': 200, 'speed': 80},
    'pyro': {'name': 'Pyro', 'health': 175, 'speed': 100},
    'demoman': {'name': 'Demoman', 'health': 175, 'speed': 93},
    'heavy': {'name': 'Heavy', 'health': 300, 'speed': 77},
    'engineer': {'name': 'Engineer', 'health': 125, 'speed': 100},
    'medic': {'name': 'Medic', 'health': 150, 'speed': 107},
    'sniper': {'name': 'Sniper', 'health': 125, 'speed': 100},
    'spy': {'name': 'Spy', 'health': 125, 'speed': 107},
}

# Enemies define their stats and attacks
# Health values adjusted to compensate for higher player damage
ENEMIES = {
    'scout_bot': {'name': 'BLU Scout Bot', 'health': 100, 'damage': (10, 20), 'accuracy': 75},
    'soldier_bot': {'name': 'BLU Soldier Bot', 'health': 180, 'damage': (20, 40), 'accuracy': 80},
    'heavy_bot': {'name': 'BLU Heavy Bot', 'health': 300, 'damage': (30, 50), 'accuracy': 70},
    'sentry_gun_boss': {'name': 'BLU Sentry Nest', 'health': 400, 'damage': (25, 35), 'accuracy': 95, 'special': 'boss'},
    'sniper_bot': {'name': 'BLU Sniper Bot', 'health': 100, 'damage': (20, 60), 'accuracy': 65},
}


# ### Core Game Classes ###

class Entity:
    """Base class for both Player and Enemy."""
    def __init__(self, name, health):
        self.name = name
        self.max_health = health
        self.current_health = health

    def take_damage(self, amount):
        """Reduces health by amount and handles death."""
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
        print(f"  {self.name} takes {amount} damage! ({self.current_health}/{self.max_health} HP remaining)")
        if self.current_health == 0:
            print_slow(f"  {self.name} has been defeated!")
            return 'dead'
        return 'alive'

    def heal(self, amount):
        """Heals entity for amount, capped at max_health."""
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        print(f"  {self.name} heals for {amount} HP! ({self.current_health}/{self.max_health} HP remaining)")

    def is_alive(self):
        """Checks if the entity's health is above 0."""
        return self.current_health > 0

class Player(Entity):
    """Stores all player-specific data and actions."""
    def __init__(self, name):
        super().__init__(name, 100) # Initial health, will be overwritten
        self.player_class = None
        self.class_key = None # e.g., 'scout'
        self.speed = 100
        self.inventory = [] # Will hold weapon dictionaries
        self.ammo = {'primary': 20, 'secondary': 36, 'sapper': 1}
        self.sentry_built = False # For Engi special
        # Special property flags set by loadout
        self.has_invis_watch = False
        self.combat_buff = None # For Buff Banner, Kritz, Jarate
        self.is_dodging = False # For Bonk

    def choose_class(self):
        """Displays class options and sets up the player."""
        print_slow("The Administrator needs you. Choose your class:")
        class_list = list(CLASSES.keys())
        for i, class_name in enumerate(class_list):
            cls = CLASSES[class_name]
            print(f"  {i+1}. {cls['name']} (HP: {cls['health']}, Speed: {cls['speed']})")

        choice = 0
        while choice not in range(1, len(class_list) + 1):
            try:
                choice = int(get_input(f"Enter a number (1-{len(class_list)}):"))
            except ValueError:
                print("That's not a valid number.")

        self.class_key = class_list[choice - 1]
        self.player_class = CLASSES[self.class_key]
        
        # Set stats from class data
        self.name = f"{self.name} the {self.player_class['name']}"
        self.max_health = self.player_class['health']
        self.current_health = self.max_health
        self.speed = self.player_class['speed']
        
        # Spy always gets a Sapper for story events
        if self.class_key == 'spy':
            self.inventory.append(WEAPONS['sapper'])


    def equip_loadout(self):
        """Allows the player to choose their weapons from available options."""
        print_slow(f"\nTime to gear up, {self.player_class['name']}.");
        
        # Get weapon choices for the player's class
        choices = WEAPON_CHOICES[self.class_key]
        
        # Loop through Primary, Secondary, Melee, and PDA slots
        for slot in ['primary', 'secondary', 'melee', 'pda']:
            weapon_keys = choices.get(slot, [])
            
            # Skip if class has no weapons for this slot
            if not weapon_keys:
                continue
                
            print_slow(f"\nChoose your **{slot.upper()}** weapon:")
            
            # If only one option, auto-equip it
            if len(weapon_keys) == 1:
                weapon_data = WEAPONS[weapon_keys[0]]
                print_slow(f"  You equip your {weapon_data['name']}. ({weapon_data['desc']})")
                self.inventory.append(weapon_data)
                continue
                
            # Present options
            for i, key in enumerate(weapon_keys):
                weapon_data = WEAPONS[key]
                print(f"  {i+1}. {weapon_data['name']} - ({weapon_data['desc']})")

            # Get user choice
            choice = 0
            while choice not in range(1, len(weapon_keys) + 1):
                try:
                    choice = int(get_input(f"Enter a number (1-{len(weapon_keys)}):"))
                except ValueError:
                    print("That's not a valid number.")
                    
            chosen_key = weapon_keys[choice - 1]
            chosen_weapon = WEAPONS[chosen_key]
            self.inventory.append(chosen_weapon)
            print(f"  {chosen_weapon['name']} equipped.")
            
            # Set special flags based on loadout
            if chosen_key == 'invis_watch':
                self.has_invis_watch = True
        
        print_slow("\nLoadout confirmed. Get to the front!")


    def show_stats(self):
        """Displays the player's current status."""
        print("\n--- YOUR STATS ---")
        print(f"  Class: {self.player_class['name']}")
        print(f"  Health: {self.current_health} / {self.max_health}")
        print(f"  Speed Rating: {self.speed}")
        print("------------------\n")

    def show_inventory(self):
        """Displays the player's weapons and their stats."""
        print("\n--- YOUR INVENTORY ---")
        if not self.inventory:
            print("  You have no weapons!")
            return
            
        for i, weapon in enumerate(self.inventory):
            print(f"  {i+1}. {weapon['name']}")
            print(f"     - Damage: {weapon['damage'][0]}-{weapon['damage'][1]} | Accuracy: {weapon['accuracy']}%")
            print(f"     - Desc: {weapon['desc']}")
        print("----------------------\n")
        
    def find_item(self, item_type, amount):
        """Logic for picking up items found on the map."""
        if item_type == 'health':
            print_slow(f"You found a health pack! You patch yourself up.")
            self.heal(amount)
        elif item_type == 'ammo':
            print_slow(f"You found an ammo crate! Resupplied.")
            # Simplified: just reset ammo counts
            self.ammo['primary'] = 20
            self.ammo['secondary'] = 36


class Enemy(Entity):
    """Stores enemy-specific data and attack logic."""
    def __init__(self, key):
        self.enemy_data = ENEMIES[key]
        super().__init__(self.enemy_data['name'], self.enemy_data['health'])
        self.damage = self.enemy_data['damage']
        self.accuracy = self.enemy_data['accuracy']
        self.is_boss = 'special' in self.enemy_data
        self.is_confused = False # For Pyro airblast
        self.debuff_turns = 0 # For Jarate

    def attack(self, target):
        """Enemy's turn to attack the player."""
        print_slow(f"{self.name} attacks you!")
        
        # Check for status effects
        if self.is_confused:
            print_slow(f"{self.name} is confused and misses its turn!")
            self.is_confused = False # Wears off
            return 'alive'

        # Roll to hit
        roll = random.randint(1, 100)
        if roll <= self.accuracy:
            dmg = random.randint(self.damage[0], self.damage[1])
            print_slow(f"{self.name} hits you for {dmg} damage!")
            return target.take_damage(dmg)
        else:
            print_slow(f"{self.name}'s attack misses!")
            return 'alive'


# ### Combat System ###

class Combat:
    """Handles the turn-based combat loop."""
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.sentry_turns = 0 # For Engi special

    def start(self):
        """Main loop for the combat encounter."""
        print_slow(f"\n--- BATTLE START ---")
        print_slow(f"A wild {self.enemy.name} appears!")
        
        # Reset any lingering combat buffs
        self.player.combat_buff = None
        self.player.is_dodging = False
        self.enemy.debuff_turns = 0

        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1
            print(f"\n--- Turn {self.turn} ---")
            print(f"Your HP: {self.player.current_health}/{self.player.max_health}")
            print(f"Enemy HP: {self.enemy.current_health}/{self.enemy.max_health}")

            # 1. Player Turn
            if self.player_turn() == 'fled':
                return 'fled'
            
            if not self.enemy.is_alive():
                break # Player won

            # 2. Enemy Turn
            if self.enemy.is_alive():
                if self.enemy_turn() == 'dead':
                    break # Enemy won

        # 3. End of Combat
        if not self.player.is_alive():
            print_slow("You have been defeated.")
            return 'dead'
        elif not self.enemy.is_alive():
            print_slow(f"You have defeated the {self.enemy.name}!")
            return 'won'

    def player_turn(self):
        """Handles all logic for the player's action."""
        
        # Reset buffs that last one turn
        self.player.is_dodging = False 

        print("\nWhat will you do?")
        print("  1. Attack")
        print("  2. Check Stats / Inventory")
        print("  3. Flee")

        choice = get_input("Choose an action (1-3):")
        
        if choice == '1': # Attack
            self.player_attack()
        elif choice == '2': # Stats
            self.player.show_stats()
            self.player.show_inventory()
            return self.player_turn() # Re-do turn
        elif choice == '3': # Flee
            return self.player_flee()
        else:
            print("That's not a valid command.")
            return self.player_turn() # Re-do turn

    def player_attack(self):
        """Player chooses a weapon and attacks OR uses a utility."""
        print("Choose your weapon:")
        
        # Filter out non-combat items unless they are utility
        combat_items = [w for w in self.player.inventory if not w.get('utility') or w['name'] in ['Bonk! Atomic Punch', 'Buff Banner', 'Sandvich', 'Medigun', 'Kritzkrieg', 'Jarate']]
        
        for i, weapon in enumerate(combat_items):
            print(f"  {i+1}. {weapon['name']} (Dmg: {weapon['damage'][0]}-{weapon['damage'][1]}, Acc: {weapon['accuracy']}%)")
        
        try:
            choice = int(get_input(f"Enter weapon number (1-{len(combat_items)}):"))
            if not 1 <= choice <= len(combat_items):
                raise ValueError
        except ValueError:
            print("Invalid weapon choice.")
            return self.player_attack() # Re-prompt
            
        weapon = combat_items[choice - 1]
        
        # --- Handle Utility Items ---
        if weapon.get('utility'):
            print_slow(f"You use your {weapon['name']}!")
            if weapon['name'] == 'Sandvich':
                self.player.heal(75)
            elif weapon['name'] == 'Bonk! Atomic Punch':
                print_slow("You're invincible!")
                self.player.is_dodging = True
            elif weapon['name'] == 'Medigun':
                self.player.heal(50)
            elif weapon['name'] == 'Kritzkrieg':
                self.player.heal(30)
                print_slow("Your next attack will be a mini-crit!")
                self.player.combat_buff = 'mini-crit'
            elif weapon['name'] == 'Buff Banner':
                print_slow("Your next attack will be a mini-crit!")
                self.player.combat_buff = 'mini-crit'
            elif weapon['name'] == 'Jarate':
                print_slow(f"The {self.enemy.name} is soaked! They will take extra damage.")
                self.enemy.debuff_turns = 2 # Lasts for this turn and next
            return 'used_utility' # Ends turn
            
        # --- Handle Standard Attack ---
        print_slow(f"You attack with your {weapon['name']}!")
        
        # Roll to hit
        roll = random.randint(1, 100)
        if roll <= weapon['accuracy']:
            # Calculate damage
            dmg = random.randint(weapon['damage'][0], weapon['damage'][1])
            
            # Check for buffs/debuffs
            if self.player.combat_buff == 'mini-crit':
                print_slow("Mini-Crit!")
                dmg = int(dmg * 1.5)
                self.player.combat_buff = None # Use up buff
                
            if self.enemy.debuff_turns > 0:
                print_slow("Jarate damage!")
                dmg = int(dmg * 1.5)
            
            # Critical hit chance (10%)
            if random.randint(1, 100) <= 10:
                print_slow("CRITICAL HIT!")
                dmg *= 2 # Crits override mini-crits
                
            self.enemy.take_damage(dmg)
        else:
            print_slow("Your attack missed!")
            
        # Clear buff even on miss
        if self.player.combat_buff:
            self.player.combat_buff = None


    def player_flee(self):
        """Player attempts to flee. Chance based on player speed and items."""
        print_slow("You try to run away...")
        
        flee_chance = 50 + (self.player.speed - 100) # Base 50%, adjusted by speed
        
        if self.player.has_invis_watch:
            flee_chance += 40 # Huge bonus for invis watch
            print_slow("You use your Invisibility Watch to cloak...")
            
        if random.randint(1, 100) <= flee_chance:
            print_slow("You successfully escaped!")
            return 'fled'
        else:
            print_slow("You couldn't get away!")
            return 'failed_flee'

    def enemy_turn(self):
        """Handles all logic for the enemy's action."""
        if self.player.is_dodging:
            print_slow(f"The {self.enemy.name} attacks, but you dodge it with Bonk!")
            self.player.is_dodging = False # Dodge is used up
            return 'alive'
        
        # Decrement debuff counter
        if self.enemy.debuff_turns > 0:
            self.enemy.debuff_turns -= 1
            
        return self.enemy.attack(self.player)


# ### Story & Map Data ###

MAP_DUSTBOWL = {
    'start': {
        'description': "You're at the RED spawn for Dustbowl, Stage 1. The first control point is just ahead, past a narrow hallway.",
        'options': {
            '1': ("Charge through the main hallway.", 'hallway'),
            '2': ("Try the side route through the small building.", 'side_route'),
        }
    },
    # --- Main Path ---
    'hallway': {
        'description': "You push into the main chokepoint. It's a meatgrinder! A BLU Soldier Bot spots you!",
        'encounter': 'soldier_bot',
        'on_win': 'hallway_clear',
        'on_flee': 'start'
    },
    'hallway_clear': {
        'description': "You clear the hallway. You can see the control point ahead. You spot a small health pack in the corner.",
        'item': ('health', 25),
        'options': {
            '1': ("Push onto the control point.", 'point_a'),
            '2': ("Fall back to spawn to regroup.", 'start') # Go back
        }
    },
    
    # --- Side Path ---
    'side_route': {
        'description': "You sneak into the side building. It's quiet... too quiet. You see a BLU Scout Bot zip past the exit.",
        'options': {
            '1': ("Ambush the Scout.", 'side_ambush'),
            '2': ("Wait for him to leave.", 'side_wait'),
            '3': ("Go back to the main hallway.", 'hallway')
        }
    },
    'side_ambush': {
        'description': "You jump out at the Scout Bot!",
        'encounter': 'scout_bot',
        'on_win': 'side_exit',
        'on_flee': 'side_route'
    },
    'side_wait': {
        'description': "You wait a moment. The coast seems clear. You emerge right next to the control point.",
        'options': {
            '1': ("Push onto the control point.", 'point_a')
        }
    },
    'side_exit': {
        'description': "You defeated the Scout. The path is clear and you emerge near the control point. You find an ammo pack.",
        'item': ('ammo', 50),
        'options': {
            '1': ("Push onto the control point.", 'point_a')
        }
    },
    
    # --- The Point & Endings ---
    'point_a': {
        'description': "You're on the control point! But it's not undefended. A massive BLU Sentry Nest is firing at you, and a Heavy Bot is protecting it!",
        'encounter': 'heavy_bot',
        'on_win': 'point_a_sentry',
        'on_flee': 'hallway' # Flee back to the choke
    },
    'point_a_sentry': {
        'description': "The Heavy is down, but that Sentry is still active! It swivels and locks onto you!",
        'encounter': 'sentry_gun_boss',
        'on_win': 'ENDING_WIN',
        'on_flee': 'hallway'
    },
    
    # --- Game Endings ---
    'GAME_OVER_LOSE': {
        'ending': "You fought well, but the BLU team was too much. You collapse as the world fades to black...\n\n--- DEFEAT ---"
    },
    'ENDING_WIN': {
        'ending': "You smash the Sentry Nest to pieces! The control point is yours! The Administrator is pleased.\n\n--- VICTORY ---"
    },
    'ENDING_WIN_SAPPER': {
        'ending': "You deftly slap your Sapper onto the Sentry. It sputters, sparks, and dies in a pathetic heap. The point is yours!\n\n--- VICTORY (SPY) ---"
    },
    'ENDING_FLEE_FINAL': {
        'description': "You decide this fight isn't for you. You run all the way back to spawn and lock the door.",
        'ending': "You may have survived, but you failed the mission. Better luck next time, mercenary.\n\n--- COWARD'S ENDING ---"
    }
}


# ### Main Game Logic ###

def main():
    """Main function to run the game."""
    global player # Make player global for get_input to access
    
    clear_screen()
    print_slow("========================================")
    print_slow("   Welcome to TF2: The Text Adventure   ", 0.02)
    print_slow("========================================", 0.02)

    try:
        player = Player("New Merc")
        player.choose_class()
        player.equip_loadout() # New step: Choose weapons
        player.show_stats()
        player.show_inventory()
        print_slow("\n(Type 'stats' or 'inventory' at most prompts to check your status.)")

        # Simple map choice for now, just loads Dustbowl
        print_slow("\nLoading map: pl_dustbowl (Stage 1)...")
        current_map = MAP_DUSTBOWL
        current_location_key = 'start'
        
        # Add a "flee" option to the start
        current_map['start']['options']['3'] = ("This is too much for me. I quit!", 'ENDING_FLEE_FINAL')

        game_over = False

        while not game_over:
            
            # Handle player death
            if not player.is_alive():
                current_location_key = 'GAME_OVER_LOSE'
            
            # Get data for current location
            try:
                location = current_map[current_location_key]
            except KeyError:
                print(f"Error: Map key '{current_location_key}' not found. Defaulting to 'start'.")
                current_location_key = 'start'
                location = current_map[current_location_key]

            clear_screen()
            print("----------------------------------------")

            # --- *** FIX IS HERE *** ---
            # CHECK FOR AN ENDING *BEFORE* PRINTING DESCRIPTION
            if 'ending' in location:
                # If the ending node ALSO has a description (like the flee ending), print it.
                if 'description' in location:
                    print_slow(location['description'])
                
                # Print the actual ending text
                print_slow(location['ending'])
                game_over = True
                continue # Skip the rest of the loop, game is over
            # --- *** END OF FIX *** ---

            # If it's not an ending, print the description
            print_slow(location['description'])

            # Check for an item
            if 'item' in location:
                player.find_item(location['item'][0], location['item'][1])
                # Remove item after pickup
                del location['item']

            # Check for an encounter
            if 'encounter' in location:
                enemy = Enemy(location['encounter'])
                combat = Combat(player, enemy)
                result = combat.start()
                
                if result == 'won':
                    current_location_key = location['on_win']
                elif result == 'dead':
                    current_location_key = 'GAME_OVER_LOSE'
                elif result == 'fled':
                    current_location_key = location['on_flee']
                
                continue # Move to the next loop iteration

            # Handle player choices
            if 'options' in location:
                # Create a temporary copy of options for this instance
                current_options = location['options'].copy()
                class_name = player.player_class['name']
                
                # --- Add Class-Specific Options ---
                
                # Spy Sapper option
                if current_location_key == 'point_a_sentry' and class_name == 'Spy':
                    current_options['s'] = ("(Spy) Use your Sapper to disable the Sentry!", 'ENDING_WIN_SAPPER')
                
                # Spy Invis option
                if current_location_key == 'hallway' and class_name == 'Spy':
                    current_options['s'] = ("(Spy) Use your Invis Watch to sneak past the Soldier.", 'hallway_clear') # Bypass fight
                
                # Soldier/Demo Jump option
                if current_location_key == 'start' and (class_name == 'Soldier' or class_name == 'Demoman'):
                    current_options['j'] = (f"({class_name}) Explosive jump over the side building.", 'side_exit') # Shortcut!
                
                # --- End Class-Specific Options ---
                
                print("\nWhat do you do?")
                valid_choices = current_options.keys()
                for key, value in current_options.items():
                    print(f"  {key}. {value[0]}")
                
                # Get validated input
                while True:
                    player_choice = get_input("Enter your choice:")
                    
                    if player_choice == 'stats':
                        player.show_stats()
                        continue # Re-show prompt
                    if player_choice == 'inventory':
                        player.show_inventory()
                        continue # Re-show prompt
                        
                    if player_choice in valid_choices:
                        current_location_key = current_options[player_choice][1]
                        break # Valid choice, exit input loop
                    else:
                        print("That's not a valid command.")
                        
    except (KeyboardInterrupt, EOFError):
        print_slow("\nGame interrupted. Exiting.")
        sys.exit()

# Global player variable needed for the helper function
player = None
if __name__ == "__main__":
    main()