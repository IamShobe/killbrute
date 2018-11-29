import os

import yaml
import click
import pkg_resources
from attrdict import AttrDict
from functools import partial

from .core.pattern.parser import PatternParser
from .core.crack import crack_password, try_pattern_password, \
    try_wild_password


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
BASE_DIR = os.path.dirname(__file__)
CHARSET_FILE_PATH = os.path.join(BASE_DIR, "charset.yml")
CYPHERS = {}


for entry_point in pkg_resources.iter_entry_points('killbrute.cyphers'):
    CYPHERS[entry_point.name] = entry_point.load()


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass



@main.command(help="crack passwords")
@click.option("--pattern", "-p", required=False,
              help="pattern of the password")
@click.option("--min", default=6, help="minimum length the password")
@click.option("--max", default=12, help="maximum length of the password")
@click.option("--charset", "-C", default=CHARSET_FILE_PATH,
              show_default=True, help="path to charset yaml file")
@click.option("--input", "-i",
              help="input path of needed to crack passwords")
@click.option("--cypher", "-c", type=click.Choice(CYPHERS.keys()),
              default="none", help="cypher of the keys")
@click.option("--output", "-o", help="output path of cracked passwords")
@click.argument("pass_hash")
def crack(pattern, min, max, charset, input, cypher, output, pass_hash):
    if pass_hash is None and input is None:
        raise RuntimeError("either --input must be given or <pass_hash>")

    required_passwords = []
    if pass_hash is not None:
        required_passwords.append(pass_hash)

    if input is not None:
        with open(input) as f:
            needed_passwords = [line.strip() for line in f]
            required_passwords += needed_passwords

    _cypher = CYPHERS[cypher](required_passwords)

    with open(charset) as f:
        charset_config = AttrDict(yaml.load(f))

    parser = PatternParser(charset_config)
    if pattern:
        _pattern = parser.parse(pattern)
        pass_gen = partial(try_pattern_password, _pattern)
        print("Password pattern parsed successfully, of length: {}".format(
            len(_pattern)))

    else:
        print("No pattern provided trying with any password [{}, {}]".format(
            min, max))
        pass_gen = partial(try_wild_password, min, max,
                           parser.all_possibilities)

    crack_password(pass_gen, cypher=_cypher, output=output)
    _cypher.cleanup()

if __name__ == '__main__':
    cli()
