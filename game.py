import random
import math


class Hit:
    def __init__(self, hit, element):
        self.hit = hit
        self.element = element

class Player:
    def __init__(self, level, name):
        self.level = level
        self.hp = math.log(self.level)*50
        self.lifepoints = self.hp
        rolls = [random.randint(1, 20) for i in range(0, 4)]
        self.strength = math.log(rolls[0])*5
        self.intelligence = math.log(rolls[1])*5
        self.agility = math.log(rolls[2])*5
        self.luck = math.log(rolls[3])*5
        self.name = name

        self.res = {
                'str': 1/100 * random.randint(0, 40),
                'int': 1/100 * random.randint(0, 40),
                'agi': 1/100 * random.randint(0, 40),
                'luck': 1/100 * random.randint(0, 40)
            }

    def takeHit(self, hit):
        print('You take {} damage.\n'.format(hit.hit*self.res[hit.element]))
        self.lifepoints -= hit.hit * self.res[hit.element]
        print('You have {} lifepoints left.\n'.format(self.lifepoints))
        

class Monster():
    def __init__(self, level):
        self.level = level
        self.hp = math.log(self.level)*50
        self.lifepoints = self.hp
        rolls = [random.randint(1, 20) for i in range(0, 4)]
        self.strength = math.log(rolls[0])*5
        self.intelligence = math.log(rolls[1])*5
        self.agility = math.log(rolls[2])*5
        self.luck = math.log(rolls[3])*5

        self.spells = [self.rogue_wave, self.burning_arrows, self.doom_scythe]
        self.spellnames = ['Rogue Wave', 'Burning Arrows', 'Doom Scythe']

        self.res = {
            'str': 1/100 * random.randint(0, 40),
            'int': 1/100 * random.randint(0, 40),
            'agi': 1/100 * random.randint(0, 40),
            'luck': 1/100 * random.randint(0, 40)
            }
        
    def takeHit(self, hit):
        print('Monster takes {} damage!\n'.format(hit.hit*self.res[hit.element]))
        self.lifepoints -= hit.hit * self.res[hit.element]
        print('Monster has {} lifepoints remaining.\n'.format(self.lifepoints))


    def rogue_wave(self, player):
        h = Hit(random.randint(0, 10)*self.strength/10, 'int')
        print('Monster casts Rogue Wave!\n')
        player.takeHit(h)


    def burning_arrows(self, player):
        print('Monster casts Burning Arrows!\n')
        player.takeHit(Hit(random.randint(0, 15)*self.strength/10, 'str'))

    def doom_scythe(self, player):
        print('Monster casts Doom Scythe!\n')
        player.takeHit(Hit(random.randint(0, 15)*self.luck/10, 'luck'))

class Wizard(Player):
    def __init__(self, level, name):
        Player.__init__(self, level, name)

        self.spells = {
            '1': self.manta_ray,
            '2': self.explosive_fist,
            '3': self.healing_heart
            }
        
        self.spellnames = ['Manta Ray',
                            'Explosive Fist',
                           'Healing Heart']
        
    def manta_ray(self, monster):
        print('You cast Manta Ray!\n')
        monster.takeHit(Hit(random.randint(0, 10)*self.luck/10, 'int'))
    

    def explosive_fist(self, monster):
        print('You cast Explosive Fist!\n')
        monster.takeHit(Hit(random.randint(3, 12)*self.strength/10, 'str'))

    def healing_heart(self, monster):
        print('You cast Healing Heart!\n')
        self.lifepoints += random.randint(1, 11)*self.intelligence/10

class Rogue(Player):
    def __init__(self, level, name):
        Player.__init__(self, level, name)

        self.spells = {
            '1': self.roguery,
            '2': self.toxic_gift,
            '3': self.swift_kick
            }

        self.spellnames = ['Roguery',
                           'Toxic Gift',
                           'Swift Kick']

    def roguery(self, monster):
        print('You cast Roguery!\n')
        h = Hit(random.randint(0, 10)* self.luck/10, 'luck')
        monster.takeHit(h)
        self.lifepoints += h.hit

    def toxic_gift(self, monster):
        print('You cast Toxic Gift!\n')
        poison = Hit(random.randint(10, 15) * self.agility/10, 'agi')
        poison_count = 5
        return [poison_count, poison]

    def swift_kick(self, monster):
        pass

class Archer(Player):
    pass

class Swordsman(Player):
    pass

class Pirate(Player):
    pass
    

def Fight(player, monster, initialisation, poison_counter):
    ops = [monster_casts_spell, player_casts_spell]

    if initialisation == 0:
        ops[0](monster, player)
    else:
        poison_counter = ops[1](monster, player)

    return poison_counter






def monster_casts_spell(monster, player):
    ran = random.randint(0, 2)
    monster.spells[ran](player)

def player_casts_spell(monster, player):
    cast = input("Choose your spell. To cast {0}, type '1'. To cast {1}, type '2'. To cast {2}, type '3'.\n".format(player.spellnames[0], player.spellnames[1], player.spellnames[2]))

    return player.spells[cast](monster)

    
    
    
classes = {'1': Wizard, '2': Rogue, '3': Archer, '4': Swordsman, '5': Pirate}
    


def gameloop():
    level = 3
    poison_counter = 0
    PC = 0
    playername = input("What is your name?\n")
    chosen_class=''
    while chosen_class not in ['1', '2', '3', '4', '5']:
        chosen_class = input("Choose your class. 1: Wizard, 2: Rogue, 3: Archer, 4: Swordsman, 5: Pirate\n")
    print("Your statistics are as following, %s:" % playername)
    
    monster = Monster(level)
    player = classes[chosen_class](level, playername)

    print("Strength: {0}\n".format(player.strength) + "Intelligence: {0}\n".format(player.intelligence) + "Agility: {0}\n".format(player.agility) + "Luck: {0}\n".format(player.luck))

    initialisation = random.randint(0, 1)
    game_counter = 0
    while player.lifepoints > 0 and monster.lifepoints > 0:
        poison_counter = Fight(player, monster, initialisation, poison_counter)
        
        if poison_counter and poison_counter[0] > 0:
            p = poison_counter[1].hit * monster.res[poison_counter[1].element]
            print('Monster is poisoned! It takes {} damage.\n'.format(p))
            monster.lifepoints -= p
            print('Monster has {} lifepoints left.\n'.format(monster.lifepoints))
            poison_counter[0] -= 1
    

if __name__ == "__main__":
    gameloop()
