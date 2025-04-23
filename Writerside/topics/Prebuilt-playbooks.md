# Prebuilt playbooks

If you have an archive and/or a folder with `embark.exe`, `playbook.yml` and
lots of other files, then it's probably a playbook that has been assembled
for you to quickly deploy it.


## Launching the playbook

In order to launch the playbook, just double-click the `embark.exe` file.
It will ask for administrative permissions, you should grant them, because
playbooks are intended to modify your apps and system, thus these permissions
are needed.

> **Attention!**
>
> On some versions of Windows, such as Windows 10 1703,
> running `embark.exe` packaged as a single
> file is not supported. In this case, you need to download 
> `embark-unpacked.zip`, unpack it (without deleting 
> the `_internal` folder) and run  `embark.exe` included in the archive.
{style="warning"}

When you double-click the file, a screen will appear:

![embark_ui_selector_en.png](embark_ui_selector_en.png)

Click on the desired playbook button. The main screen will appear.

![embark_ui_main_en.png](embark_ui_main_en.png)

Here you can see how the playbook execution is going:
- ✅ - task is done
- ⌛ - task is running
- ❔ - task is pending
- ❌ - task has failed
- ⏩ - task was skipped

More info in [](UI-mode-usage.md)
