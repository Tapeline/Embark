"""Provides i18n base."""

import ctypes
import locale

_CURRENT_LOCALE: str | None = None
_DEFAULT_LOCALE = "en"
_FALLBACK_LOCALE = _DEFAULT_LOCALE


def get_windows_locale() -> str:
    """Get current Windows locale."""
    global _CURRENT_LOCALE  # noqa: WPS420
    if _CURRENT_LOCALE is None:
        windll = ctypes.windll.kernel32
        win_locale = windll.GetUserDefaultUILanguage()
        _CURRENT_LOCALE = locale.windows_locale[win_locale]  # noqa: WPS122
    return _CURRENT_LOCALE  # noqa: WPS121


class I18N:
    """Base i18n class."""

    locales: dict[str, "I18N"] = {}

    name = ""

    def __init_subclass__(cls):
        super().__init_subclass__()
        I18N.locales[cls.name] = cls()


def get_locale(name: str) -> I18N | None:
    """Get locale by name."""
    for l_name, lang in I18N.locales.items():
        if l_name in name:
            return lang
    return None


def localize(message_code: str) -> str:
    """Get message by code."""
    lang_node = get_locale(get_windows_locale()) or get_locale(_DEFAULT_LOCALE)
    if lang_node is None:
        return "Translation not found"
    try:
        return _get_message(lang_node, message_code)
    except AttributeError:
        fallback_node = get_locale(_FALLBACK_LOCALE)
        try:  # noqa: WPS505
            return _get_message(fallback_node, message_code)
        except AttributeError:
            return "Translation not found"


def _get_message(lang_node, message_code: str) -> str:
    if lang_node is None:
        return "Translation not found"
    for attr in message_code.split("."):
        lang_node = getattr(lang_node, attr)
    return str(lang_node)


L = localize
