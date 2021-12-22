from pathlib import Path
from typing import Union
from functional import seq


def children(p: Path) -> seq:
    """
    files and subfolders in the folder as sequence
    :param p:
    :return:
    """
    return seq(list(p.iterdir()))


def dirs(p: Path) -> seq:
    """
    subfolders in the folder as sequence
    :param p:
    :return:
    """
    return children(p).filter(lambda f: f.is_dir())


def files(p: Path) -> seq:
    """
    only files in the folder
    :param p:
    :return:
    """
    return children(p).filter(lambda f: f.is_file())

def with_ext(p: Path, ext: str) -> seq:
    """
    files in the folder that have appropriate extension
    :param p:
    :param ext:
    :return:
    """
    return files(p).filter(lambda f: ext in f.suffix)


def by_ext(p: Path, ext: str) -> seq:
    return files(p).filter(lambda f: ext in f.suffix).group_by(lambda f: f.suffix)


def rename_files(dir: Union[seq, Path], has: str, what: str, to: str):
    """
    rename files that contain a substring
    :param files: sequence of files or folder #TODO: update to Union[seq, Path] when switched to python 3.10
    :param has: substring to search for
    :param what: substring to substitute (not always the same as "has")
    :param to: substitute to string
    :return: renamed files
    """
    if isinstance(dir, Path):
        return rename_files(files(dir), has, what, to)
    else:
        return dir.map(lambda p: p if not has in p.name else p.rename(Path(p.parent, p.name.replace(what, to))))


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


def tprint(p: Path, prefix: str = "", debug: bool = False):
    """
    Pretty-print the content of the folder recursively
    :param p: path to print content for
    :param prefix: prefix to add in the beginning
    :param debug: adding debug statements to separate files from folders
    :return:
    """
    fl = files(p)
    print(prefix+p.name)
    if fl.len() > 0:
        if debug:
            print(prefix + "FILES:")
        files(p).for_each(lambda f: print(f"\t"+prefix+f.name))
    folders = dirs(p)
    if folders.len() > 0:
        if debug:
            print(prefix+"FOLDERS")
        folders.for_each(lambda d: tprint(d, f"\t"+prefix))