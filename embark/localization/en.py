from embark.localization.i18n import I18N


class EnI18N(I18N):
    name = "en"

    class UI:
        playbooks_found_title = "Following playbooks found in this location"
        playbooks_found_subtitle = "Click on a button to load"
        playbooks_not_found = "No playbooks found"

        waiting_for_playbook = "Waiting for playbook"
        running_playbook = "Running a playbook"
        playbook_started = "Playbook started"
        playbook_ended = "Playbook finished"
        task_started = "Task started"
        task_skipped = "Task skipped"
        task_ended = "Task completed"
        ask_title = "Question"
        you_sure_want_exit = "Are you sure you want to interrupt the playbook and exit immediately?"
        stop_playbook = "Stop execution"

        debug = "Debug tools:"
        debug_vars = "Debug variables"
        debug_exec = "Execute in scope"
        debug_vars_section = "Playbook variables"
        debug_envs_section = "Environment variables"
        execute_expression = "Execute code"
