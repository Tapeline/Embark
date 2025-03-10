from types import MappingProxyType
from typing import Final

import pytest

from embark.domain.execution.variables import VariablesEnv


@pytest.mark.parametrize(
    ("defined_vars", "defined_envs", "format_str", "expected"),
    [
        ({"a": "abc"}, {}, "{{a}}", "abc"),
        ({}, {"a": "abc"}, "{{a}}", "abc"),
        ({"a": "abcd"}, {"a": "abc"}, "{{a}}", "abcd"),
        ({"a": "abcd"}, {"a": "abc", "b": "def"}, "{{a}}{{b}}", "abcddef"),
    ]
)
def test_variable_format(
        defined_vars, defined_envs, format_str, expected
):
    """Test that variables are substituted."""
    variables = VariablesEnv(defined_vars, defined_envs)
    assert variables.format(format_str) == expected


@pytest.mark.parametrize(
    "format_str",
    [
        "{{non existent variable}}",
        "{{invalid var syntax",
        "{{normal var syntax}}{{invalid var syntax",
        "{{}}"
    ]
)
def test_wrong_format_strings(format_str):
    """Test that wrong var strings are left as is."""
    variables = VariablesEnv({}, {})
    assert variables.format(format_str) == format_str


_VARS: Final = MappingProxyType({
    "a": "123",
    "b": "456"
})
_ENVS: Final = MappingProxyType({
    "a": "abc",
    "c": "def"
})


@pytest.mark.parametrize(
    ("object_fmt", "expected"),
    [
        (
            "{{a}}{{b}}{{c}}",
            "123456def"
        ),
        (
            ["{{a}}", "{{b}}", "{{c}}"],
            ["123", "456", "def"]
        ),
        (
            {
                "k1": "{{a}}",
                "k2": "{{b}}",
                "k3": "{{c}}",
            },
            {
                "k1": "123",
                "k2": "456",
                "k3": "def",
            }
        ),
        (
            {
                "k1": "{{a}}",
                "k2": ["{{b}}", {"k4": "{{c}}"}],
                "k3": {"k5": "{{c}}"},
            },
            {
                "k1": "123",
                "k2": ["456", {"k4": "def"}],
                "k3": {"k5": "def"},
            }
        )
    ]
)
def test_complex_format(
        object_fmt, expected
):
    """Test that variables are substituted in objects."""
    variables = VariablesEnv(_VARS, _ENVS)
    assert variables.format_object(object_fmt) == expected
