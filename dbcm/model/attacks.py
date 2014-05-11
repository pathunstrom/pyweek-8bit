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

    def __repr__(self):
        return "Attack {}".format(self.name)


def no_attack(attack):
    return None


def full(attack):
    attack.target.damage += damage(attack)


def partial(attack):
    attack.target.damage += int(damage(attack) * .75)


def shave(attack):
    attack.target.damage += int(damage(attack) * .25)


aggressive = [
    {'name': '', 'potency': 0, 'type': BLOCK,
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
    {'name': 'Blitz', 'potency': 50, 'type': STRIKE,
     'speed': 1.0, 'stance': NEUTRAL,
     'win': full, 'lose': partial},
    {'name': 'Punch', 'potency': 30, 'type': STRIKE,
     'speed': 1.5, 'stance': AGGRESSIVE,
     'win': full, 'lose': shave},
    {'name': 'Throw', 'potency': 40, 'type': GRAPPLE,
     'speed': 0.5, 'stance': DEFENSIVE,
     'win': full, 'lose': no_attack},
]

neutral = [
    {'name': '', 'potency': 0, 'type': BLOCK,
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
    {'name': 'Tackle', 'potency': 50, 'type': STRIKE,
     'speed': 1.0, 'stance': AGGRESSIVE,
     'win': full, 'lose': no_attack},
    {'name': 'Reverse', 'potency': 50, 'type': GRAPPLE,
     'speed': 0.5, 'stance': NEUTRAL,
     'win': full, 'lose': no_attack},
    {'name': 'Stop', 'potency': 10, 'type': BLOCK,
     'speed': 1.5, 'stance': DEFENSIVE,
     'win': full, 'lose': shave},
]

defensive = [
    {'name': '', 'potency': 0, 'type': '',
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
    {'name': 'Reverse', 'potency': 50, 'type': GRAPPLE,
     'speed': 1.0, 'stance': NEUTRAL,
     'win': full, 'lose': no_attack},
    {'name': 'Reverse', 'potency': 0, 'type': GRAPPLE,
     'speed': 0.5, 'stance': NEUTRAL,
     'win': full, 'lose': no_attack},
    {'name': 'Perfect Defense', 'potency': 0, 'type': BLOCK,
     'speed': 1.5, 'stance': DEFENSIVE,
     'win': full, 'lose': no_attack},
]

passive = [
    {'name': '', 'potency': 0, 'type': '',
     'speed': 0.0, 'stance': PASSIVE,
     'win': no_attack, 'lose': no_attack},
]