import os
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from symply import symlink, delete_symlink


def test_symlink_creation():
    with Patcher() as patcher:
        # Setup a fake file system
        patcher.fs.create_file("/fake/source.txt")
        source = "/fake/source.txt"
        target = "/fake/target_link.txt"

        # Test symlink creation
        symlink(source, target)

        # Assert symlink was created correctly
        assert patcher.fs.islink(target)
        assert patcher.fs.readlink(target) == source

def test_symlink_with_nonexistent_source():
    with Patcher():
        source = "/fake/nonexistent.txt"
        target = "/fake/target_link.txt"

        # Expect FileNotFoundError
        with pytest.raises(FileNotFoundError):
            symlink(source, target)

def test_overwrite_existing_symlink():
    with Patcher() as patcher:
        # Setup a fake file system and create initial files and symlinks
        patcher.fs.create_file("/fake/source.txt")
        patcher.fs.create_file("/fake/new_source.txt")
        patcher.fs.create_symlink("/fake/target_link.txt", "/fake/source.txt")

        source_new = "/fake/new_source.txt"
        target = "/fake/target_link.txt"

        # Try to create a new symlink where one already exists without force
        with pytest.raises(FileExistsError):
            symlink(source_new, target, force=False)

        # Now try with force=True, which should overwrite the existing symlink
        symlink(source_new, target, force=True)

        # Assert the symlink was overwritten
        assert patcher.fs.islink(target), "The target should still be a symlink."
        assert patcher.fs.readlink(target) == source_new, "The symlink should point to the new source."

def test_no_force_on_existing_symlink():
    with Patcher() as patcher:
        # Setup a fake file system and create initial files and symlinks
        patcher.fs.create_file("/fake/original_source.txt")
        patcher.fs.create_file("/fake/intended_source.txt")
        patcher.fs.create_symlink("/fake/target_link.txt", "/fake/original_source.txt")

        source_intended = "/fake/intended_source.txt"
        target = "/fake/target_link.txt"

        # Attempt to create a symlink where one already exists without using force
        with pytest.raises(FileExistsError):
            symlink(source_intended, target, force=False)
        
        # Assert the original symlink was not changed
        assert patcher.fs.islink(target), "The target should remain a symlink."
        assert patcher.fs.readlink(target) == "/fake/original_source.txt", "The symlink should still point to the original source."

def test_fail_to_overwrite_existing_symlink():
    with Patcher() as patcher:
        patcher.fs.create_file("/fake/source.txt")
        patcher.fs.create_symlink("/fake/target_link.txt", "/fake/old_source.txt")
        
        source = "/fake/source.txt"
        target = "/fake/target_link.txt"
        
        # Expect FileExistsError since force=False and symlink already exists
        with pytest.raises(FileExistsError):
            symlink(source, target)

def test_invalid_input_types():
    with Patcher():
        # Expect TypeError if inputs are not strings
        with pytest.raises(TypeError):
            symlink(123, "/fake/target_link.txt")
        with pytest.raises(TypeError):
            symlink("/fake/source.txt", 456)

def test_empty_input_strings():
    with Patcher():
        # Expect ValueError if source or target is empty
        with pytest.raises(ValueError):
            symlink("", "/fake/target_link.txt")
        with pytest.raises(ValueError):
            symlink("/fake/source.txt", "")

def test_delete_existing_symlink():
    with Patcher() as patcher:
        patcher.fs.create_symlink("/fake/target_link.txt", "/fake/source.txt")
        target = "/fake/target_link.txt"
        
        # Test symlink deletion
        assert delete_symlink(target) is True
        assert not patcher.fs.exists(target)

def test_delete_nonexistent_symlink():
    with Patcher() as patcher:
        target = "/fake/nonexistent_link.txt"
        
        # Test deletion of a non-existing symlink
        assert delete_symlink(target) is False
        assert not patcher.fs.exists(target)

def test_delete_when_target_is_regular_file():
    with Patcher() as patcher:
        patcher.fs.create_file("/fake/regular_file.txt")
        target = "/fake/regular_file.txt"
        
        # Test attempting to delete a regular file as a symlink
        assert delete_symlink(target) is False
        assert patcher.fs.exists(target)  # File should still exist

def test_symlink_with_invalid_paths():
    with Patcher():
        source = "/invalid/??source.txt"
        target = "/invalid/??target_link.txt"
        
        # Expect an exception due to invalid characters in the path
        with pytest.raises(Exception):
            symlink(source, target)

def test_symlink_with_unicode_characters():
    with Patcher() as patcher:
        source = "/valid/unicodé_source.txt"
        target = "/valid/unicodé_target_link.txt"
        patcher.fs.create_file(source)

        # Test creation with unicode characters
        symlink(source, target)
        assert patcher.fs.islink(target), "The symlink should be created with unicode characters."

def test_symlink_loops():
    with Patcher() as patcher:
        source = "/loop/source.txt"
        target = "/loop/target_link.txt"
        patcher.fs.create_file(source)

        # Creating a symlink that points to itself
        with pytest.raises(Exception):
            symlink(target, target)

def test_symlink_with_insufficient_permissions():
    with Patcher() as patcher:
        source = "/secure/source.txt"
        target = "/secure/target_link.txt"
        patcher.fs.create_file(source)
        # Set directory to read-only
        os.chmod('/secure', 0o400)

        # Expect a permission error
        with pytest.raises(PermissionError):
            symlink(source, target)
