AGGRESSIVE = 0
NEUTRAL = 1
DEFENSIVE = 2

STRIKE = 0
GRAPPLE = 1
BLOCK = 2

test_HP = 5
moves = [(STRIKE, "Strike"), (GRAPPLE, "Grapple"), (BLOCK, "Block")]
test_move_list = {key: moves for key in range(3)}


class BattleModel(object):
    """
    A state model of a game battle.
    """

    def __init__(self):
        self.winner = None
        self.multiplayer = False
        self.player = Monster(test_HP, test_move_list)
        self.opponent = Monster(test_HP, test_move_list)
        self.selection = 0
        self.local_set = False
        self.selection_o = 0
        self.remote_set = False
        self.animation_step = 0
        self.step_complete = False

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

    def step_animation(self):
        self.resolve()
        self.animation_step += 1

    def end_animation(self):
        self.animation_step = 0

    def set_opponent(self, selection):
        self.selection_o = selection
        self.remote_set = not self.remote_set

    def resolve(self):
        if self.animation_step == 5:
            self.selection = 0
            self.local_set = False
            self.remote_set = False
        elif self.animation_step == 4:
            self.opponent.stance = self.selection_o
        elif self.animation_step == 3:
            self.player.stance = self.selection
        elif self.animation_step == 2:
            if self.selection == self.selection_o:
                self._draw(self.selection)
            elif self.selection == STRIKE:
                if self.selection_o == BLOCK:
                    self.player.damage(1)
                else:
                    self.opponent.damage(1)
            elif self.selection == BLOCK:
                if self.selection_o == GRAPPLE:
                    self.player.damage(1)
                else:
                    self.opponent.damage(1)
            else:
                if self.selection_o == STRIKE:
                    self.player.damage(1)
                else:
                    self.opponent.damage(1)

    def _draw(self, advantage):
        if self.player.stance == self.opponent.stance:
            return
        elif self.player.stance == advantage:
            self.opponent.damage(1)
        elif self.opponent.stance == advantage:
            self.player.damage(1)
        else:
            return



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
        self._damage += amount

    def heal(self, amount):
        self._damage += amount * -1

    def change_stance(self, stance):
        self.stance = stance