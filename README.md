# pycomfort
Utility methods for python code

So far contains only file/folder related methods but will be extended in the future

## files.py

The most important methods are:
* def children(p: Path) -> seq #lists files and subfolders as pyfunctional sequence
* def dirs(p: Path) -> seq #lists subfolders as pyfunctional sequence
* def files(p: Path) -> seq: #lists files as pyfunctional sequence
* def with_ext(p: Path, ext: str) -> seq: # filters files by extension
* def rename_files_with_dictionary(files_or_path: Union[seq, Path], dictionary: dict, test: bool = False): #renames files according to key value pairs mentioned in the dictionary
* def rename_files(files_or_path: Union[seq, Path], has: str, what: str, to: str): rename files that contain a substring
* def rename_not_files(files: seq, not_has: str, what: str, to: str) -> seq: #rename files that do NOT contain a substring
* def replace_in_file(file: Path, what: str, to: str, output: Optional[Path] = None): #replaces string in a file
* def replace_from_dict_in_file(file: Path, replacement: dict, output: Optional[Path] = None, verbose: bool = False) -> Path: # replaces the text in the file based on key-value pairs in the dictionary
* def tprint(p: Path, prefix: str = "", debug: bool = False): #prints the file tree

## executables

Executables are in comfort.py. At the moment it is the text replacement functions wrapped to CLI by click library:
* def replace(file: str, what: str, to: str, output: Optional[str]):
* def replace_dict(file: str, dictionary: str, output: Optional[str], verbose: bool = False):


# publishing to pip

You can use publish.sh script
