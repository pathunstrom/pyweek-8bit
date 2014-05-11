def resolve_turn(attack1, attack2):
    """Determine winning attack, call attack win and lose methods."""
#   compare attack types and set "winner".
    case = {'strike': strike, 'grapple': grapple, 'block': block}
    attacks = case[attack1.type](attack1, attack2)
#   Resolve winning attack.
    attacks[0].win()
#   Resolve losing attack.
    attacks[1].lose()


def strike(attack1, attack2):
    return attack1, attack2


def grapple(attack1, attack2):
    return attack1, attack2


def block(attack1, attack2):
    return attack1, attack2