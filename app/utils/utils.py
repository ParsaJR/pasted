import string
import random

charPool = string.ascii_letters + string.digits


def generateShortCode() -> str:
    code = ""
    for _ in range(6):
        code += random.choice(charPool)
    return code
