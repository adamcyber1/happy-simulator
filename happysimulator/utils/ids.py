import random

HEX = '0123456789ABCDEF'
def get_id() -> str:
    return ''.join(random.choice(HEX) for _ in range(6))