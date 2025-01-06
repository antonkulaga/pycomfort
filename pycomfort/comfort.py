import json
from pathlib import Path
from typing import Optional

import typer
from pycomfort.files import replace_in_file, replace_from_dict_in_file

app = typer.Typer()

@app.command("replace")
def replace(
    file: Path = typer.Option(..., exists=True, help="rename file with substitution"),
    what: str = typer.Option(..., help="substitute --from"),
    to: str = typer.Option(..., help="substitute --to"),
    output: Optional[Path] = typer.Option(None, help="optional output, will rewrite --file is not output provided")
) -> Path:
    """Replace text in a file with new text.
    
    Args:
        file: Input file path to perform replacements on
        what: Text to search for and replace
        to: Text to replace matches with
        output: Optional output file path. If not provided, will modify input file in-place
        
    Returns:
        Path to the modified file (either input file or output file)
        
    Example:
        replace --file=config.txt --what="DEBUG" --to="INFO"
    """
    print(f"replacing {what} to {to} in {file}")
    where = output
    return replace_in_file(file, what, to, where)

@app.command("replace_with_dictionary")
def replace_dict(
    file: Path = typer.Option(..., exists=True, help="rename file with substitution"),
    dictionary: Path = typer.Option(..., exists=True, help="dictionary to load from"),
    output: Optional[Path] = typer.Option(None, help="optional output, will rewrite --file is not output provided"),
    verbose: bool = typer.Option(False, help="if we should output more to console")
) -> Path:
    """Replace multiple text patterns in a file using a JSON dictionary.
    
    Args:
        file: Input file path to perform replacements on
        dictionary: Path to JSON file containing old->new text mappings
        output: Optional output file path. If not provided, will modify input file in-place
        verbose: If True, prints detailed replacement information
        
    Returns:
        Path to the modified file (either input file or output file)
        
    Example:
        replace_with_dictionary --file=config.txt --dictionary=replacements.json --verbose
    """
    print(f"replacing from {dictionary} in {file}")
    # reading the data from the file
    with dictionary.open("r+") as f:
        data = f.read()
    js: dict = json.loads(data)
    print(f"substitutions dictionary is:")
    for k, v in js.items():
        print(f"REPLACE {k} WITH {v}\n")
    where = output
    return replace_from_dict_in_file(file, js, where, verbose)

if __name__ == '__main__':
    app()