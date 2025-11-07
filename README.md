# TF2: The Text Adventure

##  mercenariesConcept

Welcome to the RED team, mercenary! **TF2: The Text Adventure** is a single-player, text-based role-playing game where you take on the role of one of the nine iconic classes from *Team Fortress 2*.

Your mission is to fight your way through a classic map, battle BLU team bots, manage your health and ammo, and capture the enemy intelligence. The game features fast-paced, turn-based combat, class-specific stats, and branching paths that lead to different outcomes.

## 🚀 Features

* **9 Playable Classes:** Choose from Scout, Soldier, Pyro, Demoman, Heavy, Engineer, Medic, Sniper, or Spy. Stats are visible at class selection.
* **Full Custom Loadouts:** Choose your Primary, Secondary, Melee, and even PDA slot weapons at the start! At least 2 options per slot.
* **Fast-Paced Combat:** No more "Special" button! Choose any weapon from your loadout to attack. Damage is high and combat is quick, just like in the real game.
* **Utility Items:** Weapons like the Sandvich, Bonk! Atomic Punch, and Mediguns are used in combat as utility actions (healing, dodging) instead of attacking.
* **Special Properties:** Your class and loadout matter!
    * A **Scout's** high speed makes him great at fleeing.
    * A **Spy's** Invisibility Watch gives him a near-guaranteed escape.
    * **Soldiers** and **Demos** can explosive-jump to new locations.
    * **Spies** can sap Sentries for a unique victory.
* **Branching Story:** Make choices that alter your path through the map.
* **Multiple Endings:** Your decisions and performance will lead you to one of three unique endings.
* **Item Pickups:** Find health and ammo packs scattered throughout the level.

## 🖥️ How to Run

### Dependencies

* **Python 3.x**

That's it! The game uses only Python's built-in libraries (`random`, `time`, `sys`) and requires no external packages.

### Instructions

1.  **Save the Game:** Save the game code as a Python file (e.g., `game.py`).
2.  **Open Your Terminal:** Open a terminal or command prompt.
3.  **Navigate to the File:** Use the `cd` command to move to the directory where you saved `game.py`.
    ```bash
    cd path/to/your/game
    ```
4.  **Run the Game:** Execute the script using Python.
    ```bash
    python game.py
    ```
    (or `python3 game.py` on some systems)

## 🎮 Basic Gameplay Commands

The game is played by typing a number (or letter) corresponding to a menu option and pressing **Enter**.

* **Menu Choices:** `1`, `2`, `s`, `j`, etc. - Selects a story choice or combat action.
* **`stats`**: (Available at most prompts) Type this to check your current health, ammo, and class.
* **`inventory`**: (Available at most prompts) Type this to see your equipped weapons and their stats.
* **`quit`**: (Available at most prompts) Type this to exit the game.