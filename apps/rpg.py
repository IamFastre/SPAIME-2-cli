import os, sys
from os.path import dirname, join, abspath
from time import sleep

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import random, math, re, copy

# Importing my modules
from res.colors import *
from res.libs import *

# So we can happily fry your device
sys.setrecursionlimit(100000)



def identify(Obj):

    if   type(Obj) == Creature:
        Type = 'creatures'
    elif type(Obj) == Block:
        Type = 'block'
    elif isinstance(Obj, Item) == Item:
        Type = 'items'
    else:
        Type = 'others'

    return Type


def addHP(this, num):
    print(f"{this.name} healed {num} ♥.")
    this.health += num


def remHP(this, num):
    print(f"{this.name} damaged {num} ♥.")
    this.health -= num


# Things Definition:
class Thing:

    def move(this, X, Y):

        x, y = this.position[0], this.position[1]

        this.position = (X, Y)
        this.world.map[x][y][identify(this)].remove(this)
        this.world.map[X][Y][identify(this)].append(this)

    def distance(this, Obj):
        X, Y = this.position[0], this.position[1]
        x, y = Obj.position [0], Obj.position [1]

        distance = ((X - x) ** 2 + ( Y - y) ** 2 ) ** 0.5

        return distance




# Items Definition:
ITEMS:dict = {}

class Item(Thing):
    def __init__(this, name:str, id:int, func:dict, attributes:dict = {}) -> None:
        this.name  = name
        this.id    = id
        this.func = func
        this.attrs = attributes
        ITEMS[id]  = this

class Weapon(Item):
    def __init__(this, name: str, id: int, func:dict, damage:int, attributes:dict = {}) -> None:
        super().__init__(name, id, func, attributes)
        this.damage = damage

class Apple(Item):
    def __init__(this, attributes: dict = {}) -> None:
        super().__init__('Apple', 0, {addHP: [10]}, attributes)

class Poison(Item):
    def __init__(this, attributes: dict = {}) -> None:
        super().__init__('Poison', 1, {remHP: [10]}, attributes)




# Blocks Definition:
class Block(Item, Thing):
    def __init__(this, name: str, id: int, func:dict, attributes:dict = {}) -> None:
        super().__init__(name, id, func, attributes)



# Races Definition:
class Mage():
    name      = 'Mage'
    health    = 100
    attack    = 20
    inventory = [Poison()]




# World/Map Definition:
class World():

    def __init__(this, name:str, X:int, Y:int) -> None:
        this.name = name

        this.X    = X
        this.Y    = Y

        this.map  = this.makeMap()
        this.size = X * Y


    def __getitem__(this, X) -> list:
        return this.map[X]


    def makeMap(this):

        TILE  = {
            'block'    : [],
            'creatures': [],
            'items'    : [],
            'others'   : []
        }

        MAP   = [[copy.deepcopy(TILE) for _ in range(this.Y)] for _ in range(this.X)]
        return MAP


    def addTo(this, obj:Thing, x:int, y:int):
        objType = identify(obj)

        this.map[x][y][objType].append(obj) 

        



# Characters Definition:
class Creature(Thing):

    def __init__(this, name:str, race:dict, world:World, position:tuple = (0,0)) -> None:
        this.name      = name
        this.race      = race

        this.world     = world
        this.position  = position
        world.addTo(this, *position)

        this.attack    = race.attack
        this.health    = race.health
        this.maxHealth = race.health

        this.inventory:list = race.inventory


    def __str__(this) -> str:
        inventory = [_.name for _ in (this.inventory)]

        return f"""
        {X0.END}=====[{X0.GOLD}Character List{X0.END}]=====
        {X0.VIOLET}Name: {this.name}
        {X0.VIOLET}World: {this.world.name}
        {X0.VIOLET}Position: {this.position[0]}, {this.position[1]}
        {X0.VIOLET}Race: {this.race.name}
        {X0.VIOLET}Health: {this.health}/{this.maxHealth} {X0.RED}♥
        {X0.VIOLET}Inventory: {', '.join(inventory)}
        {X0.END}==========================
        """.replace(' '*8, '').replace(':', X0.GRAY + ':')


    def hit(this, who) -> int:
        print(f"{this.name} hit {who.name} with {this.attack} ♥.")
        who.health -= this.attack


    def use(this, item:Item, who:Thing = None) -> None:

        who = this if who == None else who

        if item in this.inventory:
            print(f"{this.name} used {item.name}.")
            for Use in item.func:
                args = item.func[Use]
                Use(who, *args)
            this.inventory.remove(item)
        else:
            print(f"Item {item.name} not available.")

if __name__ == '__main__':

    clear()

    hell    = World('Hell', 10, 10)
    fastre  = Creature('Fastre', Mage, hell, (0,0))
    slowre  = Creature('Slowre', Mage, hell, (5,5))

    print(fastre, slowre)
    fastre.use(fastre.inventory[0], slowre)
    print(fastre, slowre)


"""
attrs = {
    func: stuff
}
"""