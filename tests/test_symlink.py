import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from symply import symlink


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
