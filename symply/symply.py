"""
Symply is a simple Python module for creating and managing symlinks.

The `symlink` function creates a symlink from a source file to a target path. It can optionally overwrite an existing symlink if the `force` parameter is set to True.

Example:
    >>> symlink("/path/to/source.txt", "/path/to/target_link.txt", force=True)

The `delete_symlink` function deletes a symlink if it exists.

Example:
    >>> delete_symlink("/path/to/target_link.txt")

The module also provides a `SymlinkMonitor` class for advanced monitoring of directories and handling events using a custom event handler.

Example:
    >>> handler = SymlinkHandler(handle_event)
    >>> monitor = SymlinkMonitor('/path/to/directory', handler, include_patterns=['*.txt', '*.docx'])
    >>> monitor.start()

For more information, see the documentation for each function and class.
"""
import logging
import os

logger = logging.getLogger(__name__)


def symlink(source: str, target: str, force: bool = False) -> bool:
    """
    Create a symlink from source to target. Optionally, overwrite any existing symlink if `force` is True.

    Args:
        source (str): The path to the source file.
        target (str): The path where the symlink will be created.
        force (bool): If True, overwrite an existing symlink if it exists.

    Raises:
        TypeError: If any of the parameters are not of the expected type.
        ValueError: If source or target is an empty string.
        FileNotFoundError: If the source file does not exist.
        FileExistsError: If the target already exists and force is not True.
        Exception: If the symlink creation fails for other reasons.

    Returns:
        bool: True if the symlink was created successfully, otherwise False.
    """
    if not (isinstance(source, str) and isinstance(target, str)):
        raise TypeError("Source and target must be strings")
    if not isinstance(force, bool):
        raise TypeError("Force must be a boolean")
    if not source or not target:
        raise ValueError("Source and target must be non-empty strings")

    source = os.path.abspath(source)
    target = os.path.abspath(target)

    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file or directory does not exist: {source}")

    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logger.info(f"Created missing directory: {target_dir}")

    if os.path.lexists(target):
        if os.path.islink(target):
            current_target = os.path.realpath(target)
            if current_target != source:
                if force:
                    os.unlink(target)
                    logger.info(f"Removed existing link: {target}")
                else:
                    raise FileExistsError(f"Symlink exists and points to a different source: {current_target}")
        elif force:
            if os.path.isfile(target) or os.path.isdir(target):
                os.remove(target)
                logger.info(f"Removed existing file or directory: {target}")
            else:
                raise FileExistsError(f"File or directory exists and is not a symlink: {target}")
        else:
            raise FileExistsError(f"File or directory exists and is not a symlink: {target}")

    os.symlink(source, target)
    if not os.path.islink(target) or os.path.realpath(target) != source:
        raise Exception("Failed to create or validate the symlink")

    logger.info(f"Symlink created: {target} -> {source}")
    return True


def delete_symlink(target, remove_source=False) -> bool:
    """Remove a symlink at the specified target path and optionally remove the source file or directory."""
    if not os.path.islink(target):
        return False

    source = os.path.realpath(target)
    os.unlink(target)
    logger.info(f"Deleted symlink: {target}")

    if remove_source:
        if os.path.isfile(source):
            os.remove(source)
            logger.info(f"Deleted source file: {source}")
        elif os.path.isdir(source):
            os.rmdir(source)
            logger.info(f"Deleted source directory: {source}")
    return True