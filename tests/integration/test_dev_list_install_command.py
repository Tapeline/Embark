from argparse import Namespace

from embark.commands.cmd_dev_list_installs import DevListInstallsCommand
from tests.integration.mock import MockOSInterface, mock_streams


def test_dli_command(snapshot):
    """Test that embark dli command works."""
    with mock_streams() as streams:
        command = DevListInstallsCommand(MockOSInterface())
        ret_code = command(Namespace())
    assert ret_code == 0
    assert streams.stdout.value == snapshot
    assert not streams.stderr.value
