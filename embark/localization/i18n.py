"""Provides i18n base."""

import ctypes
import locale

_CURRENT_LOCALE: str | None = None
_DEFAULT_LOCALE = "en"
_FALLBACK_LOCALE = _DEFAULT_LOCALE


def get_windows_locale() -> str:
    """Get current Windows locale."""
    global _CURRENT_LOCALE
    if _CURRENT_LOCALE is None:
        windll = ctypes.windll.kernel32
        _CURRENT_LOCALE = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return _CURRENT_LOCALE


class I18N:
    """Base i18n class."""

    LOCALES = {}

    name = ""

    def __init_subclass__(cls):
        super().__init_subclass__()
        I18N.LOCALES[cls.name] = cls


def get_locale(name: str) -> I18N | None:
    """Get locale by name."""
    for l_name, lang in I18N.LOCALES.items():
        if l_name in name:
            return lang
    return None


def localize(message_code: str) -> str:
    """Get message by code."""
    lang_node = get_locale(get_windows_locale()) or get_locale(_DEFAULT_LOCALE)
    if lang_node is None:
        return "Translation not found"
    try:
        for attr in message_code.split("."):
            lang_node = getattr(lang_node, attr)
        return lang_node
    except AttributeError:
        lang_node = get_locale(_FALLBACK_LOCALE)
        if lang_node is None:
            return "Translation not found"
        try:
            for attr in message_code.split("."):
                lang_node = getattr(lang_node, attr)
            return lang_node
        except AttributeError:
            return "Translation not found"


L = localize
