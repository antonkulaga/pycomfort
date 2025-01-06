# pycomfort 
[![PyPI version](https://badge.fury.io/py/pycomfort.svg)](https://badge.fury.io/py/pycomfort)
[![Tests](https://github.com/antonkulaga/pycomfort/actions/workflows/tests.yml/badge.svg)](https://github.com/antonkulaga/pycomfort/actions/workflows/tests.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/pycomfort.svg)](https://pypi.org/project/pycomfort/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python utility library that provides convenient methods for file operations and text manipulation using a functional programming approach. Built with developer comfort in mind, pycomfort offers:

- 🗂️ **Functional File Operations** - Chain operations on files and directories using pyfunctional
- 🔄 **Smart Text Replacement** - Easily replace text patterns in single or multiple files
- 📝 **Enhanced Logging** - Beautiful hierarchical logging based on Eliot library with timing and argument tracking
- 🛠️ **CLI Tools** - Command-line utilities for common file and text operations

## Installation

Install using pip:

```bash
pip install pycomfort
```

Or preferably using Poetry:

```bash
poetry add pycomfort
```

## Features

### File Operations
The library provides functional-style methods for file system operations using the pyfunctional library:

### Key Functions

#### File System Operations
- `children(p: Path) -> seq` - Lists files and subfolders as pyfunctional sequence
- `dirs(p: Path) -> seq` - Lists subfolders as pyfunctional sequence
- `files(p: Path) -> seq` - Lists files as pyfunctional sequence
- `with_ext(p: Path, ext: str) -> seq` - Filters files by extension

#### File Manipulation
- `rename_files_with_dictionary(files_or_path, dictionary, test=False)` - Batch rename files using a dictionary
- `replace_in_file(file, what, to, output=None)` - Replace text in files
- `replace_from_dict_in_file(file, replacement, output=None)` - Replace multiple patterns using a dictionary

#### Extended Logging Features (based on Eliot logging library)
- `to_nice_stdout(output_file: Optional[Path])` - Configure Eliot logging with improved rendering to stdout
- `to_nice_file(output_file: Path, rendered_file: Path)` - Configure Eliot logging with improved rendering to separate files
- `log_function` decorator - Enhanced function logging with timing and argument tracking

### Examples

Some examples of how to use the library.

#### Get all Python files and print their names

```python
print(files("test"))
python_files = with_ext("test", ".py") #get all python files in current directory
python_files.map(lambda p: p.name).for_each(print) #print all python files names
```

Replace multiple patterns in all markdown files:
```python
replacements = {
"# TODO": "# DONE",
"- [ ]": "- [x]"
}
with_ext("docs", ".md").for_each(lambda f: replace_from_dict_in_file(f, replacements))
```

#### Pretty print directory structure:

```python
tprint("project", max_depth=2, debug=True)
```

#### Chain operations to process specific files:

```python
(dirs("src")
.flat_map(lambda d: with_ext(d, ".py"))
.filter(lambda p: p.stat().st_size > 1000)
.for_each(lambda f: replace_in_file(f, "old", "new")))
```


#### Function Logging with Decorator

```python
from pycomfort.logging import log_function, LogLevel
@log_function(
include_args=True,
include_result=True,
log_level=LogLevel.INFO,
include_timing=True
)
def process_data(data):
    # Some processing logic
    return data

process_data(123)
```

The decorator will log:
- Function entry with arguments
- Execution time
- Return value
- Any errors that occur

You can output logs in hirarcial way bu registering the logger file destinations using the `to_nice_stdout` or `to_nice_file` functions.
```python
to_nice_file(
output_file=Path("logs/output.json"),
rendered_file=Path("logs/readable.log")
)
```

#### Basic Logging Setup

### CLI Tools

The package provides command-line tools for text replacement:

#### Simple Text Replacement

Replace text in a file using the `replace` command:

```bash
replace --file=config.txt --what="DEBUG" --to="INFO"
```


Options:
- `--file`: Input file path (required)
- `--what`: Text to search for and replace (required)
- `--to`: Text to replace matches with (required)
- `--output`: Optional output file path. If not provided, modifies the input file in-place

#### Dictionary-based Replacement

Replace multiple patterns at once using a JSON dictionary with the `replace_dict` command:

```bash
replace_dict --file=config.txt --dictionary=replacements.json --verbose
```

Options:
- `--file`: Input file path (required)
- `--dictionary`: Path to a JSON file containing replacement patterns (required)
- `--verbose`: Enable verbose logging

#### Replace Text in Multiple Files Using a Dictionary

Replace multiple patterns in all markdown files:

```bash
replace_dict --file=docs --dictionary=replacements.json --output=docs_new --verbose
```
where `replacements.json` is:
```json
{
"DEBUG": "INFO",
"WARNING": "WARN",
"ERROR": "ERR"
}

Options:
- `--file`: Input file path (required)
- `--dictionary`: Path to JSON file containing old->new text mappings (required)
- `--output`: Optional output file path. If not provided, modifies the input file in-place
- `--verbose`: Print detailed replacement information

## Development Setup

1. Clone the repository:

2. Install poetry if you haven't:

3. Install dependencies:

4. Run tests:

## Publishing

To publish a new version to PyPI:

1. Update version in pyproject.toml
2. Run the publish script:

## License

Apache License 2.0 - See LICENSE file for details.

Example `replacements.json`:
```json
{
    "DEBUG": "INFO",
    "WARNING": "WARN",
    "ERROR": "ERR"
}
```
