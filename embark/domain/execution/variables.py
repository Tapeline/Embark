"""Provides tools for managing variables inside configurations."""

from typing import Any


class VariablesEnv:
    """Variables: envs + user-defined vars in ``variables`` section."""

    def __init__(self, variables: dict, envs) -> None:
        """Create variable environment."""
        self.vars = variables  # noqa: WPS110 (bad name)
        self.envs = envs

    def format(self, string: str) -> str:
        """Format a single string."""
        formatted = ""
        i = 0
        start = 0
        in_var = False
        while i < len(string):
            if (i < len(string) - 1 and not in_var and
                    string[i] == "{" and string[i + 1] == "{"):
                start = i
                i += 2
                in_var = True
                continue
            if (i < len(string) - 1 and in_var and
                    string[i] == "}" and string[i + 1] == "}"):
                formatted += self.get_value_or_leave_as_is(string[start:i+2])
                i += 2
                in_var = False
                continue
            if not in_var:
                formatted += string[i]
            i += 1
        return formatted

    def get_value_or_leave_as_is(self, var_str: str) -> str:
        """Get variable value or return string as is."""
        if not (var_str.startswith("{{") and var_str.endswith("}}")):
            return var_str
        var_name = var_str[2:len(var_str) - 2]
        return self.vars.get(var_name) or self.envs.get(var_name) or var_str

    def format_object[T: Any](self, obj: T) -> T:  # noqa: WPS110
        """Recursively format object."""
        if isinstance(obj, dict):
            return {  # type: ignore
                key: self.format_object(value)
                for key, value in obj.items()  # noqa: WPS110
            }
        if isinstance(obj, list):
            return [  # type: ignore
                self.format_object(element)
                for element in obj
            ]
        if isinstance(obj, str):
            return self.format(obj)  # type: ignore
        return obj
