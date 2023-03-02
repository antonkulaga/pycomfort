from pathlib import Path
from typing import Union, Optional, Callable
from functional import seq
from functional.pipeline import Sequence


def children(p: Path) -> Sequence:
    """
    files and subfolders in the folder as sequence
    :param p:
    :return:
    """
    return seq(list(p.iterdir()))


def dirs(p: Path) -> Sequence:
    """
    subfolders in the folder as sequence
    :param p:
    :return:
    """
    return children(p).filter(lambda f: f.is_dir())


def files(p: Path) -> Sequence:
    """
    only files in the folder
    :param p:
    :return:
    """
    return children(p).filter(lambda f: f.is_file())


def with_ext(p: Path, ext: str) -> Sequence:
    """
    files in the folder that have appropriate extension
    :param p:
    :param ext:
    :return:
    """
    return files(p).filter(lambda f: ext in f.suffix)


def by_ext(p: Path, ext: str) -> Sequence:
    return files(p).filter(lambda f: ext in f.suffix).group_by(lambda f: f.suffix)


def rename_files_with_dictionary(files_or_path: Union[seq, Path], dictionary: dict, test: bool = False):
    """
    File renaming based on a dictionary oldsubstring -> newsubstring pairs
    :param files_or_path:
    :param dictionary:
    :param test:
    :return:
    """

    if isinstance(files_or_path, Path):
        if files_or_path.is_dir():
            return rename_files_with_dictionary(files(files_or_path), dictionary=dictionary)
        else:
            return rename_files_with_dictionary(seq(files_or_path),  dictionary=dictionary)
    else:
        results = []
        for p in files_or_path:
            for k, v in dictionary.items():
                if k in p.name:
                    new_name = p.name.replace(k, v)
                    if not test:
                        p.rename(Path(p.parent, p.name.replace(k, v)))
                    results.append((p.name, new_name))
        return results


def rename_files(files_or_path: Union[seq, Path], has: str, what: str, to: str):
    """
    rename files that contain a substring
    :param files_or_path: sequence of files or folder #TODO: update to Union[seq, Path] when switched to python 3.10
    :param has: substring to search for
    :param what: substring to substitute (not always the same as "has")
    :param to: substitute to string
    :return: renamed files
    """
    if isinstance(files_or_path, Path):
        if files_or_path.is_dir():
            return rename_files(files(files_or_path), has, what, to)
        else:
            return rename_files(seq(files_or_path), has, what, to)
    else:
        return files_or_path.map(lambda p: p if has not in p.name else p.rename(Path(p.parent, p.name.replace(what, to))))


def rename_not_files(files: seq, not_has: str, what: str, to: str) -> seq:
    """
    rename files that do NOT contain a substring
    :param files: sequence of files
    :param not_has: substring to avoid
    :param what: substring to substitute (not always the same as "has")
    :param to: substitute to string
    :return: renamed files
    """
    return files.map(lambda p: p if not_has in p.name else p.rename(Path(p.parent, p.name.replace(what, to))))


def replace_in_file(file: Path, what: str, to: str, output: Optional[Path] = None) -> Path:
    """
    Replaces text in the file
    :param file: file to make replacement
    :param what: which text to replace
    :param to: to what string
    :param output: path to the output file (or same file if no output provided)
    :return:
    """
    in_place = output is None
    with file.open("r+") as text_file:
        s: str = text_file.read().replace(what, to)
        if in_place:
            text_file.write(s)
            return file
        else:
            output.write_text(s)
            return output


def replace_from_dict_in_file(file: Path, replacement: dict, output: Optional[Path] = None, verbose: bool = False) -> Path:
    """
    :param file: Path to the file
    :param replacement: dictionary for replacing test in files
    :param output:
    :param verbose:
    :return:
    """
    in_place = output is None
    with file.open("r+") as text_file:
        s: str = text_file.read()
    for old, new in replacement.items():
        if old in s:
            if verbose:
                print(f"REPLACING {old}\n WITH {new}")
            s = s.replace(old, new) # warning: mutation!
    if in_place:
        if verbose:
            print(f"editing {str(file)} in place")
        with file.open("w") as rewrite:
            rewrite.write(s)
        return file
    else:
        if verbose:
            print(f"writing {str(file)} with replacements to {str(output)}")
        output.write_text(s)
        return output


def traverse(p: Path, fun: Callable[[Path], bool] = None, max_depth: int = -1, flatten: bool = True, depth: int = 0) -> list:
    """
    traverses the files according to the condition and returns sequence with results
    :param p: path to start from
    :param fun: function to filter
    :param max_depth: how deep to traverse
    :param flatten: if we should flatten results
    :param depth:
    :return:
    """
    fl = files(p).to_list() if fun is None else files(p).filter(fun).to_list()
    folds = dirs(p).to_list() if fun is None else dirs(p).filter(fun).to_list()
    if depth == max_depth:
        return fl + folds
    else:
        if flatten:
            return fl + folds + dirs(p).flat_map(lambda d: traverse(d, fun, max_depth, flatten, depth + 1)).to_list()
        else:
            return fl + folds + dirs(p).map(lambda d: traverse(d, fun, max_depth, flatten, depth + 1)).to_list()


def tprint(p: Path, max_depth: int = -1,  prefix: str = "", debug: bool = False, depth: int = 0):
    """
    Pretty-print the content of the folder recursively
    :param p: path to print content for
    :param max_depth: how deep to traverse, by default -1 which is unlimited
    :param prefix: prefix to add in the beginning
    :param debug: adding debug statements to separate files from folders
    :param depth: current depth
    :return:
    """
    fl = files(p)
    print(prefix+p.name)
    if fl.len() > 0:
        if debug:
            print(prefix + "FILES:")
        files(p).for_each(lambda f: print(f"\t"+prefix+f.name))
    folders = dirs(p)
    if folders.len() > 0 and depth != max_depth:
        if debug:
            print(prefix+"FOLDERS")
        folders.for_each(lambda d: tprint(d, max_depth=max_depth, prefix = f"\t"+prefix, debug=debug, depth=depth+1))