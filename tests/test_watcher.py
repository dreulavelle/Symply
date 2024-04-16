import pytest
from unittest.mock import patch, MagicMock
from symply.watcher import SymlinkMonitor, SymlinkHandler

@pytest.fixture
def mock_observer():
    with patch('symply.watcher.Observer') as MockObserver:
        yield MockObserver.return_value

@pytest.fixture
def handler():
    callback = MagicMock()
    # Wrap the callback in SymlinkHandler to properly simulate its usage
    return SymlinkHandler(callback)

def test_monitor_start_stop(mock_observer, handler):
    monitor = SymlinkMonitor('/fake/directory', handler)
    monitor.start()
    monitor.stop()
    
    mock_observer.start.assert_called_once()
    mock_observer.stop.assert_called_once()
