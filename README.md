# Symply - Advanced Symlink Management and Monitoring

Symply is a Python library designed to provide robust symlink creation, deletion, and monitoring functionality. It helps developers handle file system events efficiently and perform specific actions based on those events, such as creating or managing symlinks dynamically.

## Features

- **Symlink Management**: Easily create and delete symlinks using straightforward Python functions.
- **File System Monitoring**: Monitor directories for changes like creation, deletion, modification, and moving of files or directories.
- **Event-Driven Actions**: Execute custom actions based on file system events using user-defined callback functions.
- **Customizable Filters**: Specify which files to monitor based on patterns, enhancing the flexibility and efficiency of the monitoring process.

## Installation

To install Symply, clone this repository and include it in your project, or use pip to install directly from the source:

```bash
pip install symply
```

## Usage

### Symlink Management

#### Creating a Symlink

```python
from symply import symlink

symlink('/path/to/source', '/path/to/target', force=True)
```

#### Deleting a Symlink

```python
from symply import delete_symlink

delete_symlink('/path/to/target')
```

### File System Monitoring

Set up monitoring to react to file system events:

```python
from symply.watcher import SymlinkMonitor, SymlinkHandler

def handle_event(path, event_type, destination=None):
    print(f"Event: {event_type}, Path: {path}")
    if destination:
        print(f"Destination: {destination}")

handler = SymlinkHandler(handle_event)
monitor = SymlinkMonitor('/path/to/watch', handler)
monitor.start()
```

### Stop Monitoring

```python
input("Monitoring... Press Enter to stop.\n")
monitor.stop()
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
