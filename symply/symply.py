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


def symlink(source: str, target: str, force: bool = False) -> None:
    """
    Create a symlink from source to target. Optionally, overwrite any existing symlink if `force` is True.

    Args:
        source (str): The path to the source file.
        target (str): The path where the symlink will be created.
        force (bool): If True, overwrite an existing symlink if it exists.

    Raises:
        TypeError: If any of the parameters are not of the expected type.
        ValueError: If source or target is an empty string.
        FileNotFoundError: If the source file or target directory does not exist.
        FileExistsError: If the symlink already exists and points to a different source, and force is False.
        Exception: If the symlink creation fails for other reasons.

    Returns:
        None: A successful operation is indicated by the function completing without raising an exception.
    """
    if not isinstance(source, str) or not isinstance(target, str):
        raise TypeError("Source and target must be strings")
    if not isinstance(force, bool):
        raise TypeError("Force must be a boolean")

    if not source or not target:
        raise ValueError("Source and target must be non-empty strings")

    source: str = os.path.abspath(source)
    target: str = os.path.abspath(target)

    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file does not exist: {source}")

    target_dir: str = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logger.info(f"Created missing directory: {target_dir}")

    if os.path.lexists(target):
        current_target: str | None = os.readlink(target) if os.path.islink(target) else None
        if current_target != source:
            if force:
                os.unlink(target)
                logger.info(f"Removed existing link: {target}")
            else:
                raise FileExistsError(
                    f"Symlink already exists and points to a different source: {current_target}"
                )

    if not os.path.exists(target):
        os.symlink(source, target)
        logger.info(f"Symlink created: {target} -> {source}")
    else:
        logger.info(f"Symlink points correctly: {target} -> {source}")

    if not os.path.islink(target) or os.readlink(target) != source:
        raise Exception("Failed to create or validate the symlink")


def delete_symlink(target):
    """Deletes a symlink if it exists.

    Args:
        target (str): The path to the symlink to delete.

    Returns:
        bool: True if the symlink was successfully deleted, False otherwise.
    """
    try:
        if os.path.islink(target):
            os.unlink(target)
            logger.info(f"Symlink deleted: {target}")
            return True
        else:
            logger.error(f"No symlink found at {target}")
            return False
    except OSError as e:
        logger.error(f"Failed to delete symlink: {e}")
        return False
