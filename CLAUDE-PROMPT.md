

# Simplified Game Idea

I am trying to build a simple turn based RPG game. I would like it to be built using pygame. For this first part of the project , lets create a character stats screen. 

Power: Is a "contact" or "hit" modifier. For example you can hit a monster for a certain amount of points. These "power points" can be augmented by inventory items such as weapons and armor. 

Magic: Is how "effective" items can be. For example,  If my magic is lower, then only a certain ratio / percentage of a ring or boot can be utilized. My magic can increase and decrease based on augmenting factors of inventory items such as rings, armor and helmets. All Inventory items can affect power. 

Clarity: Is the ability for the character to create stability in randomness. For example If clarity is below "entity level", it increases a penalty of percentage between the two to create "making a mistake" such as missing a monster during combat or not understanding how to wear a ring because its clarity is higher than the ratio.

Below is the structure concept of leveling with experience and modifiers

**STRUCTURE Attributes of all entities monsters and even items:**

Attributes equal 20, but can have magic augmentation modifiers from weapons, and items to bring this up higher.

Everything has power, magic, clarity, hit points, etc.  The general structure of which is going to be the same for every object and entity in the game regardless of what it is. 

**There are 5  attribute modifier prefixes for all items and monsters:**



1. _PLM _- PowerLevel modifier (int) does not modify hard item level.
2. _ILM  _- ItemLevel modifier (int) based on item modifier logic
3. MLM - MagicLevel modifier (int) 
4. CLM - ClarityLevel modifier (int)
5. ELM - Experience level modifier (int)

All modifiers are controlled by an external script that can be an evalled python script of the modifier for example: _PLM–itemname.py _could contain a small amount code that is evalled when calculating power level modifiers for an item or monster.

**Experience - How many points a player has**

Levelling up LevelMaxExperience  has a max tier of 100 based on a fibonacci sequence for experience points.  



1. 100 = level 1
2. 200 = level 2
3. 300 = level 3
4. 600 = level 4
5. 1200 = level 5
6. 2400 = level 6
7. 4800 = level 7 .. etc

Levelling up grants power level modifiers (PLM) based on calculated percentage:

PLM heuristic =_ NextLevel / NextlevelMaxExp * CurrentExpPoints_

**Power - "hit" contact Heuristic: Total Power = power + (ILM + PLM)**

Power represents the maximum amount when you "hit, kick, smash, or do damage"

**magic - AKA non-"hit" contact and skills  heuristic: Magic = Magic + (ILM + MLM)**

_MLM = _MagicLevel modifier, which is based off of magic modifier logic script

Magic has 3 trigger capabilities: Immediate, Latent, Area [traps?]

My capability of successfully casting a spell which can add power modifiers

Spells can also "event trigger" power hits to immediate,  damage, or AOE, or damage over time

Triggering is based off of **events**

Damaging effects induce a CLARITY power bonus similar to power bonus

**clarity - Concept of mana or magic**

Here is an example of how clarity works:

If the "clarity" ratio between an item level is too high indicate its penalty with red, yellow or green 

Green = receive the full benefit, yellow = some benefit, red little benefit. 

It should still be POSSIBLE to achieve positive with a RED item however its efficacy may not be 100%.

clarity is also able to be augmented with items.

This should allows for controlled "randomness".  

E.g.: If clarity is below "entity level", it increases a penalty of percentage between the two to create "making a mistake" such as missing a monster, or being unable to see through the forest.

If the ratio between the level of an item is too high, indicate its penalty with red, yellow or green

Green = receive the full benefit, 

Yellow = some benefit, 

Red = No benefit, however It should still be POSSIBLE to use a red item its efficacy may not be 100% because of the penalty incurred based on the ratio of the item level.

Clarity can be "item **augmented**" with inventory items such as rings, armor, helmets and rings. 

You can achieve "**overcharge**" which could make your player explode down to 1 hit point, but not die.


# User interface:

**Screen1** - **The map and minimap, this is the default view**

This should be the active screen when the game initializes.  The map should be an auto-generated terrain using 24x24 pixel tiles.  We will apply bitmaps later.  The view should utilize "fog of war" which also can increase with clarity.  The actual size of the map can be anywhere from a single 24x24 square to as large as 24,000,000x24,000,000 squares, but should in reality be able to be infinitely large.  The player icon is also a 24x24 to fit the sizing.  The players movement should always be center, and the map should move around the character center-point. Show x and y coordinates at the bottom of the minimap, and the actual dimensions of the entire map in the bottom right of the screen.  The minimap should show what has been explored. To start the game our player will find himself on an island.  This island is pretty large, but they cannot leave outside the island.  The land should be generated with land types which may or may not incur movement penalties.  Player uses arrow keys to move.

Land types are as follows with their land name, color they should be represented to the user, and a description of moment modifiers:

**Rocky Terrain**, dark-gray, the user cannot move onto the square

**Cobblestone**, light-yellow, the user moves freely

**Swamp**, purple, it takes two movements to walk through one swamp square

**Grass**, pale-green, the user moves freely

**Forest**, dark-green, the user moves freely, but their fog of war field of view is temporarily reduced by 2

**Water**, light-blue, the user cannot pass unless they have a raft in inventory.

**Ocean**, dark-blue, the user cannot pass, and it should surround the island.

**Screen 2 - Combat, this is automatically pulled up and replaces the minimap view while combat is in session.**

Monsters only move when we move.  When we encounter a monster for combat we switch from the map screen to a combat screen automatically.  This combat screen will show our character and stats on the left, and the monster and its stats on the right.  For now the monster can be represented by its name.  Underneath are its stats which are its attributes that we outlined earlier.  To defeat a monster press the space-bar and "hit" it.  This will create a difference between the monsters power and the power of the hit to determine how many hit points are randomly to be removed from the monster.  When its the monsters turn, the same goes for the attacking monster and our character.  When the monster dies, we can LOOT the monster by determining if we want his items, or put them into a bag of holding.

Lets add monsters.   keep in mind monsters have inventory, power,  magic and clarity as well.   Monsters  can move around freely on the  map.  If a player is within the monsters fog of war view, then it will go after the player.  When a monster is encountered, bring up a fight screen.

Randomly place monsters on the map and indicate their presence with red on both the minimap and the main map.

**Screen 3 - Inventory, player can toggle this screen by pressing the "TAB" key**

Everything in the game that moves should also have an INVENTORY with specific item slots even if it is empty:

Weapon, 2 slots, modifies hit damage by using weapon PLM

Armor, 1 slot, Acts as a buffer against enemy hit damage from monsters etc

Rings, 2 slots, a magic jewelry item that can have limitless effects on a character

Boots, 1 slot, can be used for perks such as movement and magic

Helmet, 1 slot, can be used for perks such as magic and clarity

The wearer of the inventory receives the perks from the inventory items.  Each item needs its own evalled python script that is generated when an item drops.  The items should always be unique and identified transparently via a uuid so that we can track changes on the filesystem.  

Inventory also has a "Bag of holding" - this is essentially infinite inventory.  Its just a list of items the user has collected from slain monsters, the item type, and their stats in a columnar table.  

