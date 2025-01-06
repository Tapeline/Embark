"""EN locale."""

from embark.localization.i18n import I18N


class EnI18N(I18N):
    """EN locale class."""

    name = "en"

    class UI:
        playbooks_found_title = "Following playbooks found in this location"
        playbooks_found_subtitle = "Click on a button to load"
        playbooks_not_found = "No playbooks found"
