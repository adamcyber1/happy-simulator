import random

HEX = '0123456789ABCDEF'
def get_id() -> str:
    # TODO: can increase the length of the ID if needed, but it's mainly used for debugging and logging
    return ''.join(random.choice(HEX) for _ in range(6))