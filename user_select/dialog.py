import os
from tkinter import StringVar

from customtkinter import CTk, CTkButton, CTkComboBox, CTkLabel

from embark.domain.config.loader import AbstractTaskLoader
from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    Task,
    TaskExecutionContext,
)


class SelectUserTaskLoader(AbstractTaskLoader):
    name = "user_select.dialog"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        criteria = None
        requirements = []
        target = SelectUserTarget()
        return Task(context_factory, task_name, criteria, requirements, target)


class Flag:
    def __init__(self, value):
        self.value = value

    def set(self, value):
        self.value = value


class SelectUserTarget(AbstractExecutionTarget):
    def __init__(self): ...

    def execute(self, context: TaskExecutionContext) -> bool:
        root = CTk()
        root.title("Select target user")
        root.geometry("300x100")
        root.resizable(False, False)
        ok_pressed = Flag(False)

        users_dir = os.path.expandvars("%SYSTEMDRIVE%\\Users")
        choices = [
            d for d in os.listdir(users_dir)
            if os.path.exists(os.path.join(users_dir, d, "Desktop"))
        ]
        if len(choices) < 2:
            return True
        variable = StringVar(root)
        variable.set(choices[0])
        lbl = CTkLabel(root, text="Select target user")
        lbl.pack(fill="x", padx=4, pady=4)
        w = CTkComboBox(root, state="readonly", values=choices, variable=variable)
        w.set(choices[0])
        w.pack(fill="x", padx=4, pady=4)
        btn = CTkButton(root, text="OK", command=lambda: (ok_pressed.set(True), root.destroy()))
        btn.pack(fill="x", padx=4, pady=4)
        root.mainloop()

        selected_path = os.path.join(users_dir, variable.get())
        context.playbook_context.set_variable(
            "SELECTED_USER_DIR", selected_path
        )
        return ok_pressed.value

    def get_display_name(self) -> str:
        """Get display name of task."""
        return "Select target user task"


__embark_loader__ = SelectUserTaskLoader()
