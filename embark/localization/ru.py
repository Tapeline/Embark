"""RU locale."""

from embark.localization.i18n import I18N


class RuI18N(I18N):
    """RU locale class."""

    name = "ru"

    class UI:
        playbooks_found_title = "Следующие плейбуки были найдены в данном расположении:"
        playbooks_found_subtitle = "Нажмите на нужную кнопку, чтобы выполнить плейбук"
        playbooks_not_found = "Плейбуки не найдены"
