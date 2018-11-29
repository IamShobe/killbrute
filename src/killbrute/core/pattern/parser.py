ESCAPE_CHAR = "?"
ALL = "a"
LETTERS = "L"
LEFT_BRACKET = "["
RIGHT_BRACKET = "]"
LEFT_CHARSET_BRACKET = "{"
RIGHT_CHARSET_BRACKET = "}"


TYPES = {
    "u": "upper",
    "l": "lower",
    "s": "symbol",
    "d": "digit",
    "S": "special",
}

class WildCardChar(object):
    def __init__(self, possibilities):
        self.possibilities = possibilities

    def __iter__(self):
        return iter(self.possibilities)

    def __repr__(self):
        return "WildCard({!r})".format(self.possibilities)


class PatternParser(object):
    def __init__(self, charset):
        self.charset = charset

    @property
    def all_possibilities(self):
        possibilities = \
            [self.charset[item] for item in TYPES.values()]
        return "".join(possibilities)

    @property
    def letters(self):
        return "".join([self.charset.lower, self.charset.upper])

    def _parse_bracket(self, char_index, pattern):
        possibilities = []
        while char_index < len(pattern):
            ch = pattern[char_index]
            if ch == LEFT_BRACKET:
                raise RuntimeError("There cant be brackets inside of brackets")

            if ch == RIGHT_BRACKET:
                return char_index, "".join(possibilities)

            possibilities.append(self._get_possibilities(ch))
            char_index += 1

        raise RuntimeError("No closing bracket found!")

    def _parse_charset_bracket(self, char_index, pattern):
        possibilities = []
        while char_index < len(pattern):
            ch = pattern[char_index]
            if ch == LEFT_CHARSET_BRACKET:
                raise RuntimeError("There cant be brackets inside of brackets")

            if ch == RIGHT_CHARSET_BRACKET:
                return char_index, "".join(possibilities)

            possibilities.append(ch)
            char_index += 1

        raise RuntimeError("No closing bracket found!")

    def _get_possibilities(self, ch):
        if ch == ALL:
            return self.all_possibilities

        elif ch == LETTERS:
            return self.letters

        else:
            try:
                return self.charset[TYPES[ch]]

            except:
                raise RuntimeError("Unknown charset letter given {}".format(
                    ch))

    def parse(self, pattern):
        password_pattern = []
        char_index = 0
        while char_index < len(pattern):
            ch = pattern[char_index]
            if ch == ESCAPE_CHAR:
                char_index += 1  # advance pointer by 1
                ch = pattern[char_index]
                if ch == ESCAPE_CHAR:
                    password_pattern.append(ch)

                else:
                    if ch == LEFT_BRACKET:
                        char_index += 1
                        char_index, possibilities = \
                            self._parse_bracket(char_index, pattern)

                    elif ch == LEFT_CHARSET_BRACKET:
                        char_index += 1
                        char_index, possibilities = \
                            self._parse_charset_bracket(char_index, pattern)

                    else:
                        possibilities = self._get_possibilities(ch)

                    password_pattern.append(
                        WildCardChar(possibilities))

            else:
                password_pattern.append(pattern[char_index])

            char_index += 1

        return password_pattern