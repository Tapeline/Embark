# UI mode usage

Since v0.3-alpha Embark provides UI mode.
If Embark executable is launched
without arguments (a simple double-click on an exe) then it searches for all
playbooks in current directory ands provides a dialog where you can choose your
desired playbook. The encoding of the playbook is defaulted to UTF-8.

First a playbook select window will appear:

![](embark_ui_selector_en.png)

It will scan current directory and find all playbook-looking
files and suggest them for running. When you click on
an option, the playbook will start and the Runner window
will appear:

![](embark_ui_main_en.png)

Here you can track all activity that is happening
through the process of playbook execution.

Icons have following meaning:
- ✅ - task is done
- ⌛ - task is running
- ❔ - task is pending
- ❌ - task has failed
- ⏩ - task was skipped
