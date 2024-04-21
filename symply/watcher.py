"""
Enhanced monitoring module for directory changes and symlink management.

This module provides advanced monitoring capabilities for directories, handling events like creations, deletions, and modifications. It supports filtering events and customizable callbacks for various events.

Example:
    >>> handler = SymlinkHandler(handle_event)
    >>> monitor = SymlinkMonitor('/path/to/directory', handler, include_patterns=['*.txt', '*.docx'])
    >>> monitor.start()

The `SymlinkMonitor` class allows you to monitor a directory for changes and handle events using a custom event handler. The `SymlinkHandler` class provides a custom event handler for managing symlink-related events and more.

Attributes:
- `watch_directory` (str): The path to the directory being monitored.
- `event_handler` (FileSystemEventHandler): The event handler used for managing events.
- `observer` (Observer): The observer instance used for monitoring.
- `thread` (Thread): The thread used to run the observer.
"""
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, RegexMatchingEventHandler

logger = logging.getLogger(__name__)


class SymlinkMonitor:
    """
    Monitor a directory for changes and handle events using a custom event handler.
    
    Args:
        `watch_directory` (str): The path to the directory to monitor.
        `event_handler` (FileSystemEventHandler): The event handler to use for managing events.
        `include_patterns` (list): A list of regex patterns to include in monitoring.
        `exclude_patterns` (list): A list of regex patterns to exclude from monitoring.

    Attributes:
        watch_directory (str): The path to the directory being monitored.
        event_handler (FileSystemEventHandler): The event handler used for managing events.
        observer (Observer): The observer instance used for monitoring.
        thread (Thread): The thread used to run the observer.

    Example:
        >>> handler = SymlinkHandler(handle_event)
        >>> monitor = SymlinkMonitor('/path/to/directory', handler, include_patterns=['*.txt', '*.docx'])
        >>> monitor.start()
    """
    def __init__(self, watch_directory, event_handler, include_patterns=None, exclude_patterns=None):
        self.watch_directory = watch_directory
        self.event_handler = event_handler if event_handler else FileSystemEventHandler()
        self.observer = Observer()
        self.thread = threading.Thread(target=self._run, daemon=True)
        if include_patterns or exclude_patterns:
            self.event_handler = RegexMatchingEventHandler(ignore_directories=False, ignore_regexes=exclude_patterns, regexes=include_patterns)

    def _run(self):
        """Internal method to run the observer in a separate thread."""
        self.observer.schedule(self.event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        self.observer.join()

    def start(self):
        """Starts monitoring the specified directory in a background thread."""
        self.thread.start()
        logger.info(f"Advanced monitoring started on {self.watch_directory}")

    def stop(self):
        """Stops monitoring the directory and ensures clean thread termination."""
        self.observer.stop()
        self.thread.join()
        logger.info("Advanced monitoring stopped.")


class SymlinkHandler(RegexMatchingEventHandler):
    """Custom handler for managing symlink-related events and more."""
    def __init__(self, on_event_callback, include_patterns=None, exclude_patterns=None):
        super().__init__(ignore_directories=False, ignore_regexes=exclude_patterns, regexes=include_patterns)
        self.on_event_callback = on_event_callback

    def on_deleted(self, event):
        """Handle deleted files or directories."""
        logger.info(f"Deleted: {event.src_path}")
        self.on_event_callback(event.src_path, event_type='deleted')

    def on_modified(self, event):
        """Handle modifications to files or directories."""
        logger.info(f"Modified: {event.src_path}")
        self.on_event_callback(event.src_path, event_type='modified')

    def on_created(self, event):
        """Handle new files or directories."""
        logger.info(f"Created: {event.src_path}")
        self.on_event_callback(event.src_path, event_type='created')

    def on_moved(self, event):
        """Handle moving files or directories."""
        logger.info(f"Moved from {event.src_path} to {event.dest_path}")
        self.on_event_callback(event.src_path, event_type='moved', destination=event.dest_path)


def handle_event(path, event_type, destination=None):
    """Generic event handling function to log and manage changes detected by the monitor."""
    logger.info(f"Event Type: {event_type}, Path: {path}, Destination: {destination if destination else 'N/A'}")
