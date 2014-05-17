AGGRESSIVE = 0
NEUTRAL = 1
DEFENSIVE = 2

STRIKE = 0
GRAPPLE = 1
BLOCK = 2

test_HP = 20
moves = [(STRIKE, "Strike"), (GRAPPLE, "Grapple"), (BLOCK, "Block")]
test_move_list = {key: moves for key in range(3)}


class BattleModel(object):
    """
    A state model of a game battle.
    """

    def __init__(self):
        self.player = Monster(test_HP, test_move_list)
        self.opponent = Monster(test_HP, test_move_list)
        self.selection = 0

    def up(self):
        if self.selection:
            self.selection += -1
        else:
            self.selection = len(self.player.moves[self.player.stance]) - 1

    def down(self):
        if self.selection == len(self.player.moves[self.player.stance]) - 1:
            self.selection = 0
        else:
            self.selection += 1

class Monster(object):
    """
    A representation of a monster for battles.

    hp (int): Total HP
    move_list (dict): A dictionary of moves.
    """

    def __init__(self, hp, move_list):
        self.max_hp = hp
        self._damage = 0
        self.stance = NEUTRAL
        self.moves = move_list

    @property
    def hp(self):
        return self.max_hp - self._damage

    def damage(self, amount):
        self._damage += amount * -1

    def heal(self, amount):
        self._damage += amount

    def change_stance(self, stance):
        self.stance = stance