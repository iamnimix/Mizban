import string, random


def generate_short_code(length=5):
    chars = string.ascii_letters + string.digits
    code = "".join(random.choices(chars, k=length))

    return code
