import random
from locals import *


def get_attack(stance, index):
    case = {AGGRESSIVE: aggressive,
            NEUTRAL: neutral,
            DEFENSIVE: defensive,
            PASSIVE: passive}

    return Attack(case[stance][index])


def damage(attack):
    limiter = 50
    modifier = float(random.randint(85, 115) / 100)
    skill = attack.user.skill
    power = attack.user.power
    potency = attack.potency

    offense = skill * power * potency
    defense = offense / attack.target.defense

    return int(defense / limiter * modifier)


class Attack(object):

    def __init__(self, definition):
        self.name = definition['name']
        self.potency = definition['potency']
        self.type = definition['type']
        self.speed = definition['speed']
        self.stance = definition['stance']
        self._win = definition['win']
        self._lose= definition['lose']
        self.user = None
        self.target = None

    def win(self):
        return self._win(self)

    def lose(self):
        return self._lose(self)


def no_attack(attack):
    return None


def full(attack):
    attack.target.damage += damage(attack)


def partial(attack):
    attack.target.damage += int(damage(attack) * .75)


def shave(attack):
    attack.target.damage += int(damage(attack) * .25)


aggressive = [
    {'name': '', 'potency': 0, 'type': '',
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
]

neutral = [
    {'name': '', 'potency': 0, 'type': '',
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
]

defensive = [
    {'name': '', 'potency': 0, 'type': '',
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
]

passive = [
    {'name': '', 'potency': 0, 'type': '',
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
]