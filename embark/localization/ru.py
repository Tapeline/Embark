"""RU locale."""

from embark.localization.i18n import I18N


class RuI18N(I18N):
    """RU locale class."""

    name = "ru"

    class UI:  # noqa: WPS431
        playbooks_found_title = (
            "Следующие плейбуки были найдены в данном расположении:"
        )
        playbooks_found_subtitle = (
            "Нажмите на нужную кнопку, чтобы выполнить плейбук"
        )
        playbooks_not_found = "Плейбуки не найдены"

        waiting_for_playbook = "Ожидание плейбука"
        running_playbook = "Выполнение плейбука"
        playbook_started = "Начато выполнение"
        playbook_ended = "Выполнение завершено"
        task_started = "Начато выполнение задачи"
        task_skipped = "Задача пропущена"
        task_ended = "Задача выполнена"
        ask_title = "Вопрос"
        you_sure_want_exit = "Вы уверены, что хотите прервать выполнение и немедленно выйти?"
        stop_playbook = "Остановить выполнение"
