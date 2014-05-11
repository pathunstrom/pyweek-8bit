import genetics
from locals import *


D_GENES = 1, 1, 1, 1, 1
D_EXPERIENCE = 0, 0, 0, 0
MOVE_SET = {'aggressive': [1, 0, 0],
            'defensive': [1, 0, 0],
            'neutral': [1, 0, 0],
            'passive': [1, 0, 0]}


class Monster(object):
    """Object to represent a monster in memory."""

    def __init__(self, genes=D_GENES, experience=D_EXPERIENCE, move_set=False):
        """Initialize using passed in values.
        Stats = Iterable of integers.
        Experience = Iterable of integers.
        move_set = dictionary with keys 'aggressive', 'defensive', 'neutral',
            and 'passive.'"""

#       Unpack Body
        self.head = genes[0]
        self.body = genes[1]
        self.legs = genes[2]
        self.tail = genes[3]
        self.wings = genes[4]

#       Unpack Experience.
        self.skill = experience[0]
        self._power = experience[1]
        self._defense = experience[2]
        self._health = experience[3]

#       Unpack Status.
        self.damage = 0

        self.move_set = move_set if move_set else dict(MOVE_SET)
        self.stance = NEUTRAL

    @property
    def power(self):
        """Return calculated power."""
        return self._power + self.gene_modifier('power')

    @property
    def defense(self):
        """Return calculated defense."""
        return self._defense + self.gene_modifier('defense')

    @property
    def health(self):
        """Return calculated health."""
        return self._health + self.gene_modifier('health')

    @property
    def current_health(self):
        return self.health - self.damage

    def gene_modifier(self, stat):
        return genetics.stat(self, stat)

    def __repr__(self):
        representation = """Monster {name}
                            Stats:
                              POW: {power}
                              DEF: {defense}
                              HP: {current_hp}/{total_hp}"""

        return representation.format(name="Monster",
                                     power=self.power,
                                     defense=self.defense,
                                     current_hp=self.current_health,
                                     total_hp=self.health)