from argparse import Namespace

import pytest

from embark.commands.cmd_dev_query_install import DevQueryInstallCommand
from tests.integration.mock import MockOSInterface, mock_streams


@pytest.mark.parametrize(
    ("name", "publisher", "version"),
    [
        ("NameA", "PubA", "1.0"),
        ("NameB", "PubA", ...),
        (".*", "PubB", "1.2"),
        (".*", ".*", ...)
    ]
)
def test_dqi_command(name, publisher, version, snapshot):
    """Test that embark dqi works."""
    with mock_streams() as streams:
        command = DevQueryInstallCommand(MockOSInterface())
        ret_code = command(Namespace(
            name=name,
            publisher=publisher,
            version=None if version is ... else version,
            ignore_version=version is ...
        ))
    assert ret_code == 0
    assert streams.stdout.value == snapshot
    assert not streams.stderr.value
