from pprint import pprint
import pytest
from pathlib import Path
from typing import List, Tuple
from pycomfort.files import (
    children, 
    dirs, 
    files, 
    with_ext,
    rename_files_with_dictionary
)

@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """Create a temporary directory with some test files and subdirectories"""
    # Create test files
    (tmp_path / "test1.txt").write_text("test1")
    (tmp_path / "test2.txt").write_text("test2")
    (tmp_path / "test.py").write_text("print('hello')")
    
    # Create subdirectories
    subdir1 = tmp_path / "subdir1"
    subdir2 = tmp_path / "subdir2"
    subdir1.mkdir()
    subdir2.mkdir()
    
    # Create files in subdirectories
    (subdir1 / "subfile1.txt").write_text("subfile1")
    (subdir2 / "subfile2.py").write_text("print('subfile2')")
    
    return tmp_path

def test_children(temp_directory: Path) -> None:
    """Test the children() function"""
    child_items = children(temp_directory).to_list()
    assert len(child_items) == 5  # 3 files + 2 directories
    assert all(isinstance(item, Path) for item in child_items)

def test_dirs(temp_directory: Path) -> None:
    """Test the dirs() function"""
    directories = dirs(temp_directory).to_list()
    assert len(directories) == 2
    assert all(d.is_dir() for d in directories)
    assert "subdir1" in [d.name for d in directories]
    assert "subdir2" in [d.name for d in directories]

def test_files(temp_directory: Path) -> None:
    """Test the files() function"""
    file_list = files(temp_directory).to_list()
    assert len(file_list) == 3
    assert all(f.is_file() for f in file_list)
    assert set(f.suffix for f in file_list) == {".txt", ".py"}

def test_with_ext(temp_directory: Path) -> None:
    """Test the with_ext() function"""
    # Test .txt files
    txt_files = with_ext(temp_directory, ".txt").to_list()
    assert len(txt_files) == 2
    assert all(f.suffix == ".txt" for f in txt_files)
    
    # Test .py files
    py_files = with_ext(temp_directory, ".py").to_list()
    assert len(py_files) == 1
    assert all(f.suffix == ".py" for f in py_files)

def test_rename_files_with_dictionary(temp_directory: Path) -> None:
    """Test the rename_files_with_dictionary() function"""
    # Create rename dictionary
    rename_dict = {
        "test1": "new1",
        "test2": "new2"
    }
    
    # Perform rename operation
    results = rename_files_with_dictionary(temp_directory, rename_dict)
    
    # Check results
    assert len(results) == 2
    
    # Verify files were renamed
    new_files = files(temp_directory).map(lambda f: f.name).to_list()
    assert "new1.txt" in new_files
    assert "new2.txt" in new_files
    assert "test1.txt" not in new_files
    assert "test2.txt" not in new_files