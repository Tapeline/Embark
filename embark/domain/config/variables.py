"""
Provides tools for managing variables inside configurations
"""


class VariablesEnv:
    """
    Represents variable environment which is regular envs
    + user-defined variables in `variables` section of playbook
    """
    def __init__(self, variables: dict, envs):
        self.vars = variables
        self.envs = envs

    def format(self, string: str) -> str:
        """Format a single string"""
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

    def get_value_or_leave_as_is(self, var: str) -> str:
        """Get variable value or return string as is"""
        if not (var.startswith("{{") and var.endswith("}}")):
            return var
        var_name = var[2:len(var) - 2]
        if var_name in self.vars:
            return self.vars[var_name]
        if var_name in self.envs:
            return self.envs[var_name]
        return var

    def format_object(self, obj):
        """Recursively format object"""
        if isinstance(obj, dict):
            return {
                key: self.format_object(value)
                for key, value in obj.items()
            }
        if isinstance(obj, list):
            return [
                self.format_object(element)
                for element in obj
            ]
        if isinstance(obj, str):
            return self.format(obj)
        return obj
