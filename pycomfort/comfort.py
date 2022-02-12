import json

import click
from pycomfort.files import replace_in_file, replace_from_dict_in_file
from pathlib import Path
from typing import Union, Optional


@click.command("replace")
@click.option('--file', type=click.Path(exists=True), help="rename file with substitution")
@click.option('--what', help="substitute --from")
@click.option('--to', help="substitute --to")
@click.option('--output', help="optional output, will rewirte --file is not output provided")
def replace(file: str, what: str, to: str, output: Optional[str]):
    print(f"replacing {what} to {to} in {file}")
    where = None if output is None else Path(output)
    return replace_in_file(Path(file), what, to, where)


@click.command("replace_with_dictionary")
@click.option('--file', type=click.Path(exists=True), help="rename file with substitution")
@click.option('--dictionary', type=click.Path(exists=True), help="dictionary to load from")
@click.option('--output', help="optional output, will rewrite --file is not output provided")
@click.option('--verbose', type=click.BOOL, help="if we should output more to console")
def replace_dict(file: str, dictionary: str, output: Optional[str], verbose: bool = False):
    print(f"replacing from {dict} in {file}")
    # reading the data from the file
    with Path(dictionary).open("r+") as f:
        data = f.read()
    js: dict = json.loads(data)
    print(f"substitutions dictionary is:")
    for k, v in js.items():
        print(f"REPLACE {k} WITH {v}\n")
    where = None if output is None else Path(output)
    return replace_from_dict_in_file(Path(file), js, where, verbose)


if __name__ == '__main__':
    replace()