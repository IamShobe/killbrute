import sys
import time
from zipfile import ZipFile
from itertools import product, combinations

import colorama

colorama.init()


def _print_match(cyphered_password, current_password, matches):
    sys.stdout.write("\x1b[{a}B\n"
                     "Found new match!: {original}:{match} "
                     "\r\x1b[{b}A".format(
        original=cyphered_password,
        match=current_password, a=matches, b=matches + 1))


def try_wild_password(min_len, max_len, charset_string):
    for password_length in range(min_len, max_len):
        for password_try in product(charset_string, repeat=password_length):
            yield password_try


def try_pattern_password(password_pattern):
    for password_try in product(*password_pattern):
        yield password_try


def crack_password(password_gen, cypher, output):
    matches = 0

    file = None
    if output:
        file = open(output, "w")

    for password_try in password_gen():
        current_password = "".join(password_try)
        sys.stdout.write("Now trying: " + current_password + "\r")

        cyphered_password = cypher.is_good(current_password)
        if cyphered_password is not None:
            if file:
                file.write("{original}:{match}\n".format(
                    original=cyphered_password, match=current_password))

            else:
                _print_match(cyphered_password, current_password, matches)
            matches += 1
            if len(cypher.required_array) == 0:
                break

    sys.stdout.write(
        "\x1b[2KDone password cracking!\r"
        "\x1b[{moves}B\n".format(
            moves=matches))

    if file:
        file.close()