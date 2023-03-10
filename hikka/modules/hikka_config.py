import ast
import functools
from math import ceil
import typing

from telethon.tl.types import Message

from .. import loader, utils, translations
from ..inline.types import InlineCall

# Everywhere in this module, we use the following naming convention:
# `obj_type` of non-core module = False
# `obj_type` of core module = True
# `obj_type` of library = "library"


@loader.tds
class BampiConfigMod(loader.Module):
    """Interactive configurator for Bampi Userbot"""

    strings = {
        "name": "BampiConfig",
        "choose_core": "đ <b>Choose a category</b>",
        "configure": "đ <b>Choose a module to configure</b>",
        "configure_lib": "đĒ´ <b>Choose a library to configure</b>",
        "configuring_mod": (
            "đ <b>Choose config option for mod</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĒ´ <b>Choose config option for library</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_option": (
            "đ <b>Configuring option </b><code>{}</code><b> of mod"
            " </b><code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>Configuring option </b><code>{}</code><b> of library"
            " </b><code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>Option </b><code>{}</code><b> of module </b><code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>Option </b><code>{}</code><b> of library </b><code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Option </b><code>{}</code><b> of module </b><code>{}</code><b> has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Option </b><code>{}</code><b> of library </b><code>{}</code><b> has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "args": "đĢ <b>You specified incorrect args</b>",
        "no_mod": "đĢ <b>Module doesn't exist</b>",
        "no_option": "đĢ <b>Configuration option doesn't exist</b>",
        "validation_error": "đĢ <b>You entered incorrect config value. \nError: {}</b>",
        "try_again": "đ Try again",
        "typehint": "đĩī¸ <b>Must be a{eng_art} {}</b>",
        "set": "set",
        "set_default_btn": "âģī¸ Reset default",
        "enter_value_btn": "âī¸ Enter value",
        "enter_value_desc": "âī¸ Enter new configuration value for this option",
        "add_item_desc": "âī¸ Enter item to add",
        "remove_item_desc": "âī¸ Enter item to remove",
        "back_btn": "đ Back",
        "close_btn": "đģ Close",
        "add_item_btn": "â Add item",
        "remove_item_btn": "â Remove item",
        "show_hidden": "đ¸ Show value",
        "hide_value": "đ Hide value",
        "builtin": "đ° Built-in",
        "external": "đ¸ External",
        "libraries": "đĒ´ Libraries",
    }

    strings_ru = {
        "choose_core": "đ <b>ĐŅĐąĐĩŅĐ¸ ĐēĐ°ŅĐĩĐŗĐžŅĐ¸Ņ</b>",
        "configure": "đ <b>ĐŅĐąĐĩŅĐ¸ ĐŧĐžĐ´ŅĐģŅ Đ´ĐģŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸</b>",
        "configure_lib": "đĒ´ <b>ĐŅĐąĐĩŅĐ¸ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēŅ Đ´ĐģŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸</b>",
        "configuring_mod": (
            "đ <b>ĐŅĐąĐĩŅĐ¸ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code>\n\n<b>ĐĸĐĩĐēŅŅĐ¸Đĩ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĒ´ <b>ĐŅĐąĐĩŅĐ¸ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code>\n\n<b>ĐĸĐĩĐēŅŅĐ¸Đĩ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸:</b>\n\n{}"
        ),
        "configuring_option": (
            "đ <b>ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ </b><code>{}</code><b> ĐŧĐžĐ´ŅĐģŅ"
            " </b><code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ </b><code>{}</code><b> ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸"
            " </b><code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐŧĐžĐ´ŅĐģŅ </b><code>{}</code><b>"
            " ŅĐžŅŅĐ°ĐŊĐĩĐŊ!</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸ </b><code>{}</code><b>"
            " ŅĐžŅŅĐ°ĐŊĐĩĐŊ!</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐŧĐžĐ´ŅĐģŅ </b><code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸ </b><code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "_cls_doc": "ĐĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ĐŊŅĐš ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐžŅ Bampi",
        "args": "đĢ <b>ĐĸŅ ŅĐēĐ°ĐˇĐ°Đģ ĐŊĐĩĐ˛ĐĩŅĐŊŅĐĩ Đ°ŅĐŗŅĐŧĐĩĐŊŅŅ</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>",
        "no_option": "đĢ <b>ĐŖ ĐŧĐžĐ´ŅĐģŅ ĐŊĐĩŅ ŅĐ°ĐēĐžĐŗĐž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐēĐžĐŊŅĐ¸ĐŗĐ°</b>",
        "validation_error": (
            "đĢ <b>ĐĐ˛ĐĩĐ´ĐĩĐŊĐž ĐŊĐĩĐēĐžŅŅĐĩĐēŅĐŊĐžĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐēĐžĐŊŅĐ¸ĐŗĐ°. \nĐŅĐ¸ĐąĐēĐ°: {}</b>"
        ),
        "try_again": "đ ĐĐžĐŋŅĐžĐąĐžĐ˛Đ°ŅŅ ĐĩŅĐĩ ŅĐ°Đˇ",
        "typehint": "đĩī¸ <b>ĐĐžĐģĐļĐŊĐž ĐąŅŅŅ {}</b>",
        "set": "ĐŋĐžŅŅĐ°Đ˛Đ¸ŅŅ",
        "set_default_btn": "âģī¸ ĐĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ",
        "enter_value_btn": "âī¸ ĐĐ˛ĐĩŅŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "enter_value_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐŊĐžĐ˛ĐžĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ŅŅĐžĐŗĐž ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°",
        "add_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ŅĐģĐĩĐŧĐĩĐŊŅ, ĐēĐžŅĐžŅŅĐš ĐŊŅĐļĐŊĐž Đ´ĐžĐąĐ°Đ˛Đ¸ŅŅ",
        "remove_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ŅĐģĐĩĐŧĐĩĐŊŅ, ĐēĐžŅĐžŅŅĐš ĐŊŅĐļĐŊĐž ŅĐ´Đ°ĐģĐ¸ŅŅ",
        "back_btn": "đ ĐĐ°ĐˇĐ°Đ´",
        "close_btn": "đģ ĐĐ°ĐēŅŅŅŅ",
        "add_item_btn": "â ĐĐžĐąĐ°Đ˛Đ¸ŅŅ ŅĐģĐĩĐŧĐĩĐŊŅ",
        "remove_item_btn": "â ĐŖĐ´Đ°ĐģĐ¸ŅŅ ŅĐģĐĩĐŧĐĩĐŊŅ",
        "show_hidden": "đ¸ ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "hide_value": "đ ĐĄĐēŅŅŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "builtin": "đ° ĐŅŅŅĐžĐĩĐŊĐŊŅĐĩ",
        "external": "đ¸ ĐĐŊĐĩŅĐŊĐ¸Đĩ",
        "libraries": "đĒ´ ĐĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸",
    }

    strings_ua = {
        "choose_core": "đ <b>ĐĐ¸ĐąĐĩŅĐ¸ ĐēĐ°ŅĐĩĐŗĐžŅŅŅ</b>",
        "configure": "đ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐŧĐžĐ´ŅĐģŅ Đ´ĐģŅ ĐŊĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊĐŊŅ</b>",
        "configure_lib": "đĒ´ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐąŅĐąĐģŅĐžŅĐĩĐēŅ Đ´ĐģŅ ĐŊĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊĐŊŅ</b>",
        "configuring_mod": (
            "đ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code>\n\n<b>ĐĐžŅĐžŅĐŊŅ"
            " ĐŊĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊĐŊŅ:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĒ´ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐąŅĐąĐģŅĐžŅĐĩĐēĐ¸</b> <code>{}</code>\n\n<b>ĐĐžŅĐžŅĐŊŅ"
            " ĐŊĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊĐŊŅ:</b>\n\n{}"
        ),
        "configuring_option": (
            "đ <b>ĐĐĩŅŅĐ˛Đ°ĐŊĐŊŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ </b><code>{}</code><b> ĐŧĐžĐ´ŅĐģŅ"
            " </b><code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐĩ:"
            " {}</b>\n\n<b>ĐĐžŅĐžŅĐŊĐĩ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ĐĐĩŅŅĐ˛Đ°ĐŊĐŊŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ </b><code>{}</code><b> ĐąŅĐąĐģŅĐžŅĐĩĐēĐ¸"
            " </b><code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĐžŅĐžŅĐŊĐĩ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐŧĐžĐ´ŅĐģŅ </b><code>{}</code><b>"
            " ĐˇĐąĐĩŅĐĩĐļĐĩĐŊĐ¸Đš!</b>\n<b>ĐĐžŅĐžŅĐŊĐĩ: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐąŅĐąĐģŅĐžŅĐĩĐēĐ¸ </b><code>{}</code><b>"
            " ĐˇĐąĐĩŅĐĩĐļĐĩĐŊĐ¸Đš!</b>\n<b>ĐĐžŅĐžŅĐŊĐĩ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐŧĐžĐ´ŅĐģŅ </b><code>{}</code><b>"
            " ŅĐēĐ¸ĐŊŅŅĐž Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐˇĐ° ŅĐŧĐžĐ˛ŅĐ°ĐŊĐŊŅĐŧ</b>\n<b>ĐĐžŅĐžŅĐŊĐĩ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ </b><code>{}</code><b> ĐąŅĐąĐģŅĐžŅĐĩĐēĐ¸ </b><code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĐžŅĐžŅĐŊĐĩ: {}</b>"
        ),
        "_cls_doc": "ĐĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ĐŊĐ¸Đš ĐēĐžĐŊŅŅĐŗŅŅĐ°ŅĐžŅ Bampi",
        "args": "đĢ <b>ĐĸĐ¸ Đ˛ĐēĐ°ĐˇĐ°Đ˛ ĐŊĐĩĐ˛ŅŅĐŊŅ Đ°ŅĐŗŅĐŧĐĩĐŊŅĐ¸</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ŅŅĐŊŅŅ</b>",
        "no_option": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ĐŧĐ°Ņ ŅĐ°ĐēĐžĐŗĐž ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐēĐžĐŊŅŅĐŗŅ</b>",
        "validation_error": (
            "đĢ <b>ĐĐ˛ĐĩĐ´ĐĩĐŊĐž ĐŊĐĩĐēĐžŅĐĩĐēŅĐŊĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐēĐžĐŊŅŅĐŗŅ. \nĐŅĐ¸ĐąĐēĐ°: {}</b>"
        ),
        "try_again": "đ ĐĄĐŋŅĐžĐąŅĐ˛Đ°ŅĐ¸ ŅĐĩ ŅĐ°Đˇ",
        "typehint": "đĩī¸ <b>ĐĐžĐ˛Đ¸ĐŊĐŊĐž ĐąŅŅĐ¸ {}</b>",
        "set": "ĐŋĐžŅŅĐ°Đ˛Đ¸ŅĐ¸",
        "set_default_btn": "âģī¸ ĐĐŊĐ°ŅĐĩĐŊĐŊŅ ĐˇĐ° ĐˇĐ°ĐŧĐžĐ˛ŅŅĐ˛Đ°ĐŊĐŊŅĐŧ",
        "enter_value_btn": "âī¸ ĐĐ˛ĐĩŅŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ",
        "enter_value_desc": "âī¸ ĐĐ˛ĐĩĐ´ŅŅŅ ĐŊĐžĐ˛Đĩ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ŅŅĐžĐŗĐž ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°",
        "add_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐĩĐģĐĩĐŧĐĩĐŊŅ, ŅĐēĐ¸Đš ĐŋĐžŅŅŅĐąĐŊĐž Đ´ĐžĐ´Đ°ŅĐ¸",
        "remove_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐĩĐģĐĩĐŧĐĩĐŊŅ, ŅĐēĐ¸Đš ĐŋĐžŅŅŅĐąĐŊĐž Đ˛Đ¸Đ´Đ°ĐģĐ¸ŅĐ¸",
        "back_btn": "đ ĐĐ°ĐˇĐ°Đ´",
        "close_btn": "đģ ĐĐ°ĐēŅĐ¸ŅĐ¸",
        "add_item_btn": "â ĐĐžĐ´Đ°ŅĐ¸ ĐĩĐģĐĩĐŧĐĩĐŊŅ",
        "remove_item_btn": "â ĐĐ¸Đ´Đ°ĐģĐ¸ŅĐ¸ ĐĩĐģĐĩĐŧĐĩĐŊŅ",
        "show_hidden": "đ¸ ĐĐžĐēĐ°ĐˇĐ°ŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ",
        "hide_value": "đ ĐŅĐ¸ŅĐžĐ˛Đ°ŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ",
        "builtin": "đ° ĐĐąŅĐ´ĐžĐ˛Đ°ĐŊŅ",
        "external": "đ¸ ĐĐžĐ˛ĐŊŅŅĐŊŅ",
        "libraries": "đĒ´ ĐŅĐąĐģŅĐžŅĐĩĐēĐ¸",
    }

    strings_de = {
        "choose_core": "đ <b>WÃ¤hle eine Kategorie</b>",
        "configure": "đ <b>Modul zum Konfigurieren auswÃ¤hlen</b>",
        "configure_lib": "đĒ´ <b>WÃ¤hlen Sie eine zu konfigurierende Bibliothek aus</b>",
        "configuring_mod": (
            "đ <b>WÃ¤hlen Sie einen Parameter fÃŧr das Modul aus</b>"
            " <code>{}</code>\n\n<b>Aktuell Einstellungen:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĒ´ <b>WÃ¤hlen Sie eine Option fÃŧr die Bibliothek aus</b>"
            " <code>{}</code>\n\n<b>Aktuell Einstellungen:</b>\n\n{}"
        ),
        "configuring_option": (
            "đ <b>Option </b><code>{}</code><b> des Moduls </b><code>{}</code>"
            "<b> konfigurieren</b>\n<i>âšī¸ {}</i>\n\n<b>Standard: {}</b>\n\n<b>"
            "Aktuell: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>Option </b><code>{}</code><b> der Bibliothek </b><code>{}</code>"
            "<b> konfigurieren</b>\n<i>âšī¸ {}</i>\n\n<b>Standard: {}</b>\n\n<b>"
            "Aktuell: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>Option </b><code>{}</code><b> des Moduls </b><code>{}</code>"
            "<b> gespeichert!</b>\n<b>Aktuell: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>Option </b><code>{}</code><b> der Bibliothek </b><code>{}</code>"
            "<b> gespeichert!</b>\n<b>Aktuell: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Option </b><code>{}</code><b> des Moduls </b><code>{}</code>"
            "<b> auf den Standardwert zurÃŧckgesetzt</b>\n<b>Aktuell: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Option </b><code>{}</code><b> der Bibliothek </b><code>{}</code>"
            "<b> auf den Standardwert zurÃŧckgesetzt</b>\n<b>Aktuell: {}</b>"
        ),
        "_cls_doc": "Interaktiver Konfigurator von Bampi",
        "args": "đĢ <b>Du hast falsche Argumente angegeben</b>",
        "no_mod": "đĢ <b>Modul existiert nicht</b>",
        "no_option": "đĢ <b>Modul hat keine solche Konfigurationsoption</b>",
        "validation_error": (
            "đĢ <b>UngÃŧltiger Konfigurationswert eingegeben. \nFehler: {}</b>"
        ),
        "try_again": "đ Versuche es noch einmal",
        "typehint": "đĩī¸ <b>Sollte {} sein</b>",
        "set": "setzen",
        "set_default_btn": "âģī¸ Standardwert",
        "enter_value_btn": "âī¸ Wert eingeben",
        "enter_value_desc": "âī¸ Gib einen neuen Wert fÃŧr diese Option ein",
        "add_item_desc": "âī¸ Gib den hinzuzufÃŧgenden Eintrag ein",
        "remove_item_desc": "âī¸ Gib den zu entfernenden Eintrag ein",
        "back_btn": "đ ZurÃŧck",
        "close_btn": "đģ SchlieÃen",
        "add_item_btn": "â Element hinzufÃŧgen",
        "remove_item_btn": "â Element entfernen",
        "show_hidden": "đ¸ Wert anzeigen",
        "hide_value": "đ Wert verbergen",
        "builtin": "đ° Ingebaut",
        "external": "đ¸ Extern",
        "libraries": "đĒ´ Bibliotheken",
    }

    strings_hi = {
        "choose_core": "đ <b>ā¤ā¤ ā¤ļāĨā¤°āĨā¤ŖāĨ ā¤āĨā¤¨āĨā¤</b>",
        "configure": "đ <b>ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤° ā¤ā¤°ā¤¨āĨ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤ā¤ ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤āĨā¤¨āĨā¤</b>",
        "configure_lib": "đĒ´ <b>ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤° ā¤ā¤°ā¤¨āĨ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤˛ā¤žā¤ā¤ŦāĨā¤°āĨā¤°āĨ ā¤ā¤ž ā¤ā¤¯ā¤¨ ā¤ā¤°āĨā¤</b>",
        "configuring_mod": (
            "đ <b>ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤ā¤ ā¤ĒāĨā¤°ā¤žā¤ŽāĨā¤ā¤° ā¤āĨā¤¨āĨā¤</b> <code>{}</code>\n\n<b>ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨"
            " ā¤¸āĨā¤ā¤ŋā¤ā¤:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĒ´ <b>ā¤˛ā¤žā¤ā¤ŦāĨā¤°āĨā¤°āĨ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤ā¤ ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē ā¤āĨā¤¨āĨā¤</b> <code>{}</code>\n\n<b>ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨"
            " ā¤¸āĨā¤ā¤ŋā¤ā¤:</b>\n\n{}"
        ),
        "configuring_option": (
            "đ <b>ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē </b><code>{}</code><b> ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ </b><code>{}</code>"
            "<b> ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤° ā¤ā¤° ā¤°ā¤šā¤ž ā¤šāĨ</b>\n<i>âšī¸ {}</i>\n\n<b>ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤: {}</b>\n\n<b>"
            "ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē </b><code>{}</code><b> ā¤˛ā¤žā¤ā¤ŦāĨā¤°āĨā¤°āĨ </b><code>{}</code>"
            "<b> ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤° ā¤ā¤° ā¤°ā¤šā¤ž ā¤šāĨ</b>\n<i>âšī¸ {}</i>\n\n<b>ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤: {}</b>\n\n<b>"
            "ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē </b><code>{}</code><b> ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ </b><code>{}</code>"
            "<b> ā¤¸ā¤šāĨā¤ā¤ž ā¤ā¤¯ā¤ž!</b>\n<b>ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē </b><code>{}</code><b> ā¤˛ā¤žā¤ā¤ŦāĨā¤°āĨā¤°āĨ </b><code>{}</code>"
            "<b> ā¤¸ā¤šāĨā¤ā¤ž ā¤ā¤¯ā¤ž!</b>\n<b>ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē </b><code>{}</code><b> ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ </b><code>{}</code>"
            "<b> ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤ ā¤Žā¤žā¤¨ ā¤Ēā¤° ā¤°āĨā¤¸āĨā¤ ā¤ā¤° ā¤Ļā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤ž</b>\n<b>ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē </b><code>{}</code><b> ā¤˛ā¤žā¤ā¤ŦāĨā¤°āĨā¤°āĨ </b><code>{}</code>"
            "<b> ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤ ā¤Žā¤žā¤¨ ā¤Ēā¤° ā¤°āĨā¤¸āĨā¤ ā¤ā¤° ā¤Ļā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤ž</b>\n<b>ā¤ĩā¤°āĨā¤¤ā¤Žā¤žā¤¨: {}</b>"
        ),
        "_cls_doc": "Bampi ā¤āĨ ā¤ā¤ā¤ā¤°āĨā¤āĨā¤ā¤ŋā¤ĩ ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤°āĨā¤ļā¤¨",
        "args": "đĢ <b>ā¤ā¤Ēā¤¨āĨ ā¤ā¤˛ā¤¤ ā¤¤ā¤°āĨā¤ ā¤ĒāĨā¤°ā¤Ļā¤žā¤¨ ā¤ā¤ŋā¤ ā¤šāĨā¤</b>",
        "no_mod": "đĢ <b>ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤ŽāĨā¤āĨā¤Ļ ā¤¨ā¤šāĨā¤ ā¤šāĨ</b>",
        "no_option": "đĢ <b>ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤ŽāĨā¤ ā¤ā¤¸ā¤ž ā¤āĨā¤ ā¤ĩā¤ŋā¤ā¤˛āĨā¤Ē ā¤¨ā¤šāĨā¤ ā¤šāĨ</b>",
        "validation_error": (
            "đĢ <b>ā¤ā¤Žā¤žā¤¨āĨā¤¯ ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤°āĨā¤ļā¤¨ ā¤Žā¤žā¤¨ ā¤Ļā¤°āĨā¤ ā¤ā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤žāĨ¤ \nā¤¤āĨā¤°āĨā¤ā¤ŋ: {}</b>"
        ),
        "try_again": "đ ā¤ĒāĨā¤¨: ā¤ĒāĨā¤°ā¤¯ā¤žā¤¸ ā¤ā¤°āĨā¤",
        "typehint": "đĩī¸ <b>ā¤¯ā¤š {} ā¤šāĨā¤¨ā¤ž ā¤ā¤žā¤šā¤ŋā¤</b>",
        "set": "ā¤¸āĨā¤ ā¤ā¤°āĨā¤",
        "set_default_btn": "âģī¸ ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤",
        "enter_value_btn": "âī¸ ā¤ŽāĨā¤˛āĨā¤¯ ā¤Ļā¤°āĨā¤ ā¤ā¤°āĨā¤",
        "remove_item_btn": "â ā¤ā¤ā¤ā¤Ž ā¤šā¤ā¤žā¤ā¤",
        "show_hidden": "đ¸ ā¤ŽāĨā¤˛āĨā¤¯ ā¤Ļā¤ŋā¤ā¤žā¤ā¤",
        "hide_value": "đ ā¤ŽāĨā¤˛āĨā¤¯ ā¤ā¤ŋā¤Ēā¤žā¤ā¤",
        "builtin": "đ° ā¤Ŧā¤ŋā¤˛āĨā¤-ā¤ā¤¨",
        "external": "đ¸ ā¤Ŧā¤žā¤šā¤°āĨ",
        "libraries": "đĒ´ ā¤˛ā¤žā¤ā¤ŦāĨā¤°āĨā¤°āĨ",
        "close_btn": "đģ ā¤Ŧā¤ā¤Ļ ā¤ā¤°āĨā¤",
        "back_btn": "đ ā¤ĒāĨā¤āĨ",
    }

    strings_uz = {
        "choose_core": "đ <b>Kurum tanlang</b>",
        "configure": "đ <b>Sozlash uchun modulni tanlang</b>",
        "configure_lib": "đĒ´ <b>Sozlash uchun kutubxonani tanlang</b>",
        "configuring_mod": (
            "đ <b>Modul uchun parametrni tanlang</b> <code>{}</code>\n\n<b>Joriy"
            " sozlamalar:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĒ´ <b>Kutubxona uchun variantni tanlang</b> <code>{}</code>\n\n<b>Hozirgi"
            " sozlamalar:</b>\n\n{}"
        ),
        "configuring_option": (
            "đ <b>Modul </b><code>{}</code><b> sozlamasi </b><code>{}</code><b>"
            " konfiguratsiya qilinmoqda</b>\n<i>âšī¸ {}</i>\n\n<b>Default:"
            " {}</b>\n\n<b>Hozirgi: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>Modul </b><code>{}</code><b> kutubxonasi sozlamasi"
            " </b><code>{}</code><b> konfiguratsiya qilinmoqda</b>\n<i>âšī¸"
            " {}</i>\n\n<b>Default: {}</b>\n\n<b>Hozirgi: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>Modul </b><code>{}</code><b> sozlamasi saqlandi!</b>\n<b>Hozirgi:"
            " {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>Modul </b><code>{}</code><b> kutubxonasi sozlamasi"
            " saqlandi!</b>\n<b>Hozirgi: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Modul </b><code>{}</code><b> sozlamasi standart qiymatga"
            " tiklandi</b>\n<b>Hozirgi: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Modul </b><code>{}</code><b> kutubxonasi sozlamasi standart qiymatga"
            " tiklandi</b>\n<b>Hozirgi: {}</b>"
        ),
        "_cls_doc": "Bampi interaktiv konfiguratsiyasi",
        "args": "đĢ <b>Siz noto'g'ri ma'lumot kiritdingiz</b>",
        "no_mod": "đĢ <b>Modul mavjud emas</b>",
        "no_option": "đĢ <b>Modulda bunday sozlamalar mavjud emas</b>",
        "validation_error": (
            "đĢ <b>Noto'g'ri konfiguratsiya ma'lumotlari kiritildi. \nXatolik: {}</b>"
        ),
        "try_again": "đ Qayta urinib ko'ring",
        "typehint": "đĩī¸ <b>Buni {} bo'lishi kerak</b>",
        "set": "Sozlash",
        "set_default_btn": "âģī¸ Standart",
        "enter_value_btn": "âī¸ Qiymat kiriting",
        "remove_item_btn": "â Elementni o'chirish",
        "show_hidden": "đ¸ Qiymatni ko'rsatish",
        "hide_value": "đ Qiymatni yashirish",
        "builtin": "đ° Ichki",
        "external": "đ¸ Tashqi",
        "libraries": "đĒ´ Kutubxona",
        "close_btn": "đģ Yopish",
        "back_btn": "đ Orqaga",
    }

    strings_tr = {
        "configuring_option": (
            "đ <b>ModÃŧl </b><code>{}</code><b> seÃ§eneÄi </b><code>{}</code>"
            "<b> yapÄąlandÄąrÄąlÄąyor</b>\n<i>âšī¸ {}</i>\n\n<b>VarsayÄąlan: {}</b>\n\n<b>"
            "Mevcut: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ModÃŧl </b><code>{}</code><b> kÃŧtÃŧphanesi seÃ§eneÄi </b><code>{}</code>"
            "<b> yapÄąlandÄąrÄąlÄąyor</b>\n<i>âšī¸ {}</i>\n\n<b>VarsayÄąlan: {}</b>\n\n<b>"
            "Mevcut: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ModÃŧl </b><code>{}</code><b> seÃ§eneÄi kaydedildi!</b>\n<b>Mevcut:"
            " {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ModÃŧl </b><code>{}</code><b> kÃŧtÃŧphanesi seÃ§eneÄi"
            " kaydedildi!</b>\n<b>Mevcut: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ModÃŧl </b><code>{}</code><b> seÃ§eneÄi varsayÄąlan deÄere"
            " sÄąfÄąrlandÄą</b>\n<b>Mevcut: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ModÃŧl </b><code>{}</code><b> kÃŧtÃŧphanesi seÃ§eneÄi varsayÄąlan deÄere"
            " sÄąfÄąrlandÄą</b>\n<b>Mevcut: {}</b>"
        ),
        "_cls_doc": "Bampi etkileÅimli yapÄąlandÄąrmasÄą",
        "args": "đĢ <b>YanlÄąÅ argÃŧman girdiniz</b>",
        "no_mod": "đĢ <b>ModÃŧl bulunamadÄą</b>",
        "no_option": "đĢ <b>ModÃŧlde bÃļyle bir seÃ§enek bulunamadÄą</b>",
        "validation_error": "đĢ <b>YanlÄąÅ ayarlama bilgileri girildi. \nHata: {}</b>",
        "try_again": "đ Tekrar deneyin",
        "typehint": "đĩī¸ <b>DeÄer {} tÃŧrÃŧnde olmalÄądÄąr</b>",
        "set": "Ayarla",
        "set_default_btn": "âģī¸ VarsayÄąlan",
        "enter_value_btn": "âī¸ DeÄer girin",
        "remove_item_btn": "â ÃÄeyi kaldÄąr",
        "show_hidden": "đ¸ DeÄeri gÃļster",
        "hide_value": "đ DeÄeri gizle",
        "builtin": "đ° Dahili",
        "external": "đ¸ Harici",
        "libraries": "đĒ´ KÃŧtÃŧphane",
        "back_btn": "đ Geri",
    }

    strings_ja = {
        "configuring_option": (
            "đ <b>ãĸã¸ãĨãŧãĢ </b><code>{}</code><b> ãĒããˇã§ãŗ </b><code>{}</code>"
            "<b> ãč¨­åŽããĻããžã</b>\n<i>âšī¸ {}</i>\n\n<b>ãããŠãĢã: {}</b>\n\n<b>"
            "įžå¨: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ãĸã¸ãĨãŧãĢ </b><code>{}</code><b> ãŠã¤ããŠãĒãĒããˇã§ãŗ </b><code>{}</code>"
            "<b> ãč¨­åŽããĻããžã</b>\n<i>âšī¸ {}</i>\n\n<b>ãããŠãĢã: {}</b>\n\n<b>"
            "įžå¨: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ãĸã¸ãĨãŧãĢ </b><code>{}</code><b> ãĒããˇã§ãŗãäŋå­ãããžããīŧ</b>\n<b>įžå¨: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ãĸã¸ãĨãŧãĢ </b><code>{}</code><b> ãŠã¤ããŠãĒãĒããˇã§ãŗ ãäŋå­ãããžããīŧ</b>\n<b>įžå¨: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ãĸã¸ãĨãŧãĢ </b><code>{}</code><b> ãĒããˇã§ãŗããããŠãĢãå¤ãĢ"
            " ãĒãģãããããžãã</b>\n<b>įžå¨: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ãĸã¸ãĨãŧãĢ </b><code>{}</code><b> ãŠã¤ããŠãĒãĒããˇã§ãŗããããŠãĢãå¤ãĢ"
            " ãĒãģãããããžãã</b>\n<b>įžå¨: {}</b>"
        ),
        "_cls_doc": "Bampiå¯žčŠąįãĒč¨­åŽ",
        "args": "đĢ <b>åŧæ°ãééãŖãĻããžã</b>",
        "no_mod": "đĢ <b>ãĸã¸ãĨãŧãĢãčĻã¤ãããžãã</b>",
        "no_option": "đĢ <b>ãĸã¸ãĨãŧãĢãĢããŽãĒããˇã§ãŗã¯ãããžãã</b>",
        "validation_error": "đĢ <b>č¨­åŽæå ąãééãŖãĻããžãã \nã¨ãŠãŧ: {}</b>",
        "try_again": "đ ããä¸åēĻčŠĻããĻãã ãã",
        "typehint": "đĩī¸ <b>å¤ {} ã¯åã§ãĒããã°ãĒããžãã</b>",
        "set": "č¨­åŽ",
        "set_default_btn": "âģī¸ ãããŠãĢã",
        "enter_value_btn": "âī¸ å¤ãåĨå",
        "remove_item_btn": "â é įŽãåé¤",
        "show_hidden": "đ¸ å¤ãčĄ¨į¤ē",
        "hide_value": "đ å¤ãé ã",
        "builtin": "đ° ããĢãã¤ãŗ",
        "external": "đ¸ ã¨ã¯ãšããŗãˇã§ãŗ",
        "libraries": "đĒ´ ãŠã¤ããŠãĒ",
        "back_btn": "đ æģã",
    }

    strings_kr = {
        "configuring_option": (
            "đ <b>ëĒ¨ë </b><code>{}</code><b> ėĩė </b><code>{}</code>"
            "<b> ëĨŧ ė¤ė íŠëë¤</b>\n<i>âšī¸ {}</i>\n\n<b>ę¸°ëŗ¸ę°: {}</b>\n\n<b>"
            "íėŦ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ëĒ¨ë </b><code>{}</code><b> ëŧė´ë¸ëŦëĻŦ ėĩė </b><code>{}</code>"
            "<b> ëĨŧ ė¤ė íŠëë¤</b>\n<i>âšī¸ {}</i>\n\n<b>ę¸°ëŗ¸ę°: {}</b>\n\n<b>"
            "íėŦ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ëĒ¨ë </b><code>{}</code><b> ėĩėė´ ė ėĨëėėĩëë¤!</b>\n<b>íėŦ: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ëĒ¨ë </b><code>{}</code><b> ëŧė´ë¸ëŦëĻŦ ėĩėė´ ė ėĨëėėĩëë¤!</b>\n<b>íėŦ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ëĒ¨ë </b><code>{}</code><b> ėĩėė´ ę¸°ëŗ¸ę°ėŧëĄ ėŦė¤ė ëėėĩëë¤</b>\n<b>íėŦ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ëĒ¨ë </b><code>{}</code><b> ëŧė´ë¸ëŦëĻŦ ėĩėė´ ę¸°ëŗ¸ę°ėŧëĄ"
            " ėŦė¤ė ëėėĩëë¤</b>\n<b>íėŦ: {}</b>"
        ),
        "_cls_doc": "Bampi ëíí ė¤ė ",
        "args": "đĢ <b>ėëĒģë ė¸ėėëë¤</b>",
        "no_mod": "đĢ <b>ëĒ¨ëė ė°žė ė ėėĩëë¤</b>",
        "no_option": "đĢ <b>ëĒ¨ëė ė´ ėĩėė´ ėėĩëë¤</b>",
        "validation_error": "đĢ <b>ė¤ė  ė ëŗ´ę° ėëĒģëėėĩëë¤. \nė¤ëĨ: {}</b>",
        "try_again": "đ ë¤ė ėëíė­ėė¤",
        "typehint": "đĩī¸ <b>ę° {} ė(ë) íėė´ė´ėŧ íŠëë¤</b>",
        "set": "ė¤ė ",
        "set_default_btn": "âģī¸ ę¸°ëŗ¸ę°",
        "enter_value_btn": "âī¸ ę° ėë Ĩ",
        "remove_item_btn": "â í­ëĒŠ ė ęą°",
        "show_hidden": "đ¸ ę° íė",
        "hide_value": "đ ę° ė¨ę¸°ę¸°",
        "builtin": "đ° ëší¸ė¸",
        "external": "đ¸ íėĨ",
        "libraries": "đĒ´ ëŧė´ë¸ëŦëĻŦ",
        "back_btn": "đ ë¤ëĄ",
    }

    strings_ar = {
        "configuring_option": (
            "đ <b>ØĨØšØ¯Ø§Ø¯ ØŽŲØ§Øą </b><code>{}</code><b> ŲŲŲŲØ¯ŲŲŲ </b><code>{}</code>"
            "<b> </b>\n<i>âšī¸ {}</i>\n\n<b>Ø§ŲØ§ŲØĒØąØ§ØļŲ: {}</b>\n\n<b>"
            "Ø§ŲØ­Ø§ŲŲ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>ØĨØšØ¯Ø§Ø¯ ØŽŲØ§Øą </b><code>{}</code><b> ŲŲŲØĒØ¨ØŠ Ø§ŲŲŲØ¯ŲŲŲ </b><code>{}</code>"
            "<b> </b>\n<i>âšī¸ {}</i>\n\n<b>Ø§ŲØ§ŲØĒØąØ§ØļŲ: {}</b>\n\n<b>"
            "Ø§ŲØ­Ø§ŲŲ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ØĒŲ Ø­ŲØ¸ ØŽŲØ§Øą Ø§ŲŲŲØ¯ŲŲŲ </b><code>{}</code><b> !</b>\n<b>Ø§ŲØ­Ø§ŲŲ: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ØĒŲ Ø­ŲØ¸ ØŽŲØ§Øą ŲŲØĒØ¨ØŠ Ø§ŲŲŲØ¯ŲŲŲ </b><code>{}</code><b> !</b>\n<b>Ø§ŲØ­Ø§ŲŲ:"
            " {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ØĒŲØĒ ØĨØšØ§Ø¯ØŠ ØĒØšŲŲŲ ØŽŲØ§Øą Ø§ŲŲŲØ¯ŲŲŲ </b><code>{}</code><b> ØĨŲŲ"
            " Ø§ŲØ§ŲØĒØąØ§ØļŲ</b>\n<b>Ø§ŲØ­Ø§ŲŲ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ØĒŲØĒ ØĨØšØ§Ø¯ØŠ ØĒØšŲŲŲ ØŽŲØ§Øą ŲŲØĒØ¨ØŠ Ø§ŲŲŲØ¯ŲŲŲ </b><code>{}</code><b> ØĨŲŲ"
            " Ø§ŲØ§ŲØĒØąØ§ØļŲ</b>\n<b>Ø§ŲØ­Ø§ŲŲ: {}</b>"
        ),
        "_cls_doc": "ØĨØšØ¯Ø§Ø¯Ø§ØĒ Bampi Ø§ŲØĒŲØ§ØšŲŲØŠ",
        "args": "đĢ <b>ŲØšŲŲØ§ØĒ ØēŲØą ØĩØ­ŲØ­ØŠ</b>",
        "no_mod": "đĢ <b>ŲŲ ŲØĒŲ Ø§ŲØšØĢŲØą ØšŲŲ Ø§ŲŲŲØ¯ŲŲŲ</b>",
        "no_option": "đĢ <b>ŲØ§ ŲŲØŦØ¯ ØŽŲØ§Øą Ø¨ŲØ°Ø§ Ø§ŲØ§ØŗŲ ŲŲ Ø§ŲŲŲØ¯ŲŲŲ</b>",
        "validation_error": "đĢ <b>ØĒØšØ°Øą ØĒØ­ŲŲŲ Ø§ŲŲØšŲŲŲØ§ØĒ. \nØ§ŲØŽØˇØŖ: {}</b>",
        "try_again": "đ Ø­Ø§ŲŲ ŲØąØŠ ØŖØŽØąŲ",
        "typehint": "đĩī¸ <b>ŲØŦØ¨ ØŖŲ ŲŲŲŲ Ø§ŲŲŲŲØŠ {} ŲŲ ŲŲØš {}</b>",
        "set": "ØĒØšŲŲŲ",
        "set_default_btn": "âģī¸ Ø§ŲØ§ŲØĒØąØ§ØļŲ",
        "enter_value_btn": "âī¸ ØĨØ¯ØŽØ§Ų Ø§ŲŲŲŲØŠ",
        "remove_item_btn": "â Ø­Ø°Ų Ø§ŲØšŲØĩØą",
        "show_hidden": "đ¸ ØĨØ¸ŲØ§Øą Ø§ŲŲŲŲ",
        "hide_value": "đ ØĨØŽŲØ§ØĄ Ø§ŲŲŲŲ",
        "builtin": "đ° ŲØ¯ŲØŦ",
        "external": "đ¸ ØŽØ§ØąØŦŲ",
        "libraries": "đĒ´ ŲŲØĒØ¨Ø§ØĒ",
        "back_btn": "đ ØąØŦŲØš",
    }

    strings_es = {
        "configuring_option": (
            "đ <b>Configurando la opciÃŗn </b><code>{}</code><b> del mÃŗdulo"
            " </b><code>{}</code><b> </b>\n<i>âšī¸ {}</i>\n\n<b>Por defecto:"
            " {}</b>\n\n<b>Actual: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĒ´ <b>Configurando la opciÃŗn </b><code>{}</code><b> de la librerÃ­a del"
            " mÃŗdulo </b><code>{}</code><b> </b>\n<i>âšī¸ {}</i>\n\n<b>Por defecto:"
            " {}</b>\n\n<b>Actual: {}</b>\n\n{}"
        ),
        "option_saved": (
            "đ <b>ÂĄGuardada la opciÃŗn del mÃŗdulo"
            " </b><code>{}</code><b>!</b>\n<b>Actual: {}</b>"
        ),
        "option_saved_lib": (
            "đĒ´ <b>ÂĄGuardada la opciÃŗn de la librerÃ­a del mÃŗdulo"
            " </b><code>{}</code><b>!</b>\n<b>Actual: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>La opciÃŗn del mÃŗdulo </b><code>{}</code><b> se ha reiniciado a su"
            " valor por defecto</b>\n<b>Actual: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>La opciÃŗn de la librerÃ­a del mÃŗdulo </b><code>{}</code><b> se ha"
            " reiniciado a su valor por defecto</b>\n<b>Actual: {}</b>"
        ),
        "_cls_doc": "Configuraciones interactivas de Bampi",
        "args": "đĢ <b>Argumentos no vÃĄlidos</b>",
        "no_mod": "đĢ <b>No se encontrÃŗ el mÃŗdulo</b>",
        "no_option": "đĢ <b>El mÃŗdulo no tiene esta opciÃŗn</b>",
        "validation_error": "đĢ <b>No se pudo analizar la informaciÃŗn. \nError: {}</b>",
        "try_again": "đ Intentar de nuevo",
        "typehint": "đĩī¸ <b>El valor debe ser de tipo {}</b>",
        "set": "Establecer",
        "set_default_btn": "âģī¸ Por defecto",
        "enter_value_btn": "âī¸ Introducir valor",
        "remove_item_btn": "â Eliminar elemento",
        "show_hidden": "đ¸ Mostrar valores",
        "hide_value": "đ Ocultar valores",
        "builtin": "đ° Integrado",
        "external": "đ¸ Externo",
        "libraries": "đĒ´ LibrerÃ­as",
        "back_btn": "đ Volver",
    }

    _row_size = 3
    _num_rows = 5

    @staticmethod
    def prep_value(value: typing.Any) -> typing.Any:
        if isinstance(value, str):
            return f"</b><code>{utils.escape_html(value.strip())}</code><b>"

        if isinstance(value, list) and value:
            return (
                "</b><code>[</code>\n    "
                + "\n    ".join(
                    [f"<code>{utils.escape_html(str(item))}</code>" for item in value]
                )
                + "\n<code>]</code><b>"
            )

        return f"</b><code>{utils.escape_html(value)}</code><b>"

    def hide_value(self, value: typing.Any) -> str:
        if isinstance(value, list) and value:
            return self.prep_value(["*" * len(str(i)) for i in value])

        return self.prep_value("*" * len(str(value)))

    async def inline__set_config(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__reset_default(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        mod_instance = self.lookup(mod)
        mod_instance.config[option] = mod_instance.config.getdef(option)

        await call.edit(
            self.strings(
                "option_reset" if isinstance(obj_type, bool) else "option_reset_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__set_bool(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        validator = self.lookup(mod).config._config[option].validator
        doc = utils.escape_html(
            next(
                (
                    validator.doc[lang]
                    for lang in self._db.get(translations.__name__, "lang", "en").split(
                        " "
                    )
                    if lang in validator.doc
                ),
                validator.doc["en"],
            )
        )

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                utils.escape_html(self.lookup(mod).config.getdoc(option)),
                self.prep_value(self.lookup(mod).config.getdef(option)),
                self.prep_value(self.lookup(mod).config[option])
                if not validator or validator.internal_id != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
                if doc
                else "",
            ),
            reply_markup=self._generate_bool_markup(mod, option, obj_type),
        )

        await call.answer("â")

    def _generate_bool_markup(
        self,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                *(
                    [
                        {
                            "text": f"â {self.strings('set')} `False`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    else [
                        {
                            "text": f"â {self.strings('set')} `True`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                )
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__add_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            try:
                query = ast.literal_eval(query)
            except Exception:
                pass

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            self.lookup(mod).config[option] = self.lookup(mod).config[option] + query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__remove_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            try:
                query = ast.literal_eval(query)
            except Exception:
                pass

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            query = list(map(str, query))

            old_config_len = len(self.lookup(mod).config[option])

            self.lookup(mod).config[option] = [
                i for i in self.lookup(mod).config[option] if str(i) not in query
            ]

            if old_config_len == len(self.lookup(mod).config[option]):
                raise loader.validators.ValidationError(
                    f"Nothing from passed value ({self.prep_value(query)}) is not in"
                    " target list"
                )
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    def _generate_series_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("remove_item_btn"),
                            "input": self.strings("remove_item_desc"),
                            "handler": self.inline__remove_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                        {
                            "text": self.strings("add_item_btn"),
                            "input": self.strings("add_item_desc"),
                            "handler": self.inline__add_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                    ]
                    if self.lookup(mod).config[option]
                    else []
                ),
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def _choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        validator = self.lookup(mod).config._config[option].validator

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not validator.internal_id == "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

        await call.answer("â")

    async def _multi_choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            if value in self.lookup(mod).config._config[option].value:
                self.lookup(mod).config._config[option].value.remove(value)
            else:
                self.lookup(mod).config._config[option].value += [value]

            self.lookup(mod).config.reload()
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await self.inline__configure_option(call, mod, option, False, obj_type)
        await call.answer("â")

    def _generate_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'âī¸' if self.lookup(mod).config[option] == value else 'đ'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : 6
                if self.lookup(mod).config[option]
                != self.lookup(mod).config.getdef(option)
                else 7
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    def _generate_multi_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'âī¸' if value in self.lookup(mod).config[option] else 'âģī¸'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._multi_choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : 6
                if self.lookup(mod).config[option]
                != self.lookup(mod).config.getdef(option)
                else 7
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__configure_option(
        self,
        call: InlineCall,
        mod: str,
        config_opt: str,
        force_hidden: bool = False,
        obj_type: typing.Union[bool, str] = False,
    ):
        module = self.lookup(mod)
        args = [
            utils.escape_html(config_opt),
            utils.escape_html(mod),
            utils.escape_html(module.config.getdoc(config_opt)),
            self.prep_value(module.config.getdef(config_opt)),
            self.prep_value(module.config[config_opt])
            if not module.config._config[config_opt].validator
            or module.config._config[config_opt].validator.internal_id != "Hidden"
            or force_hidden
            else self.hide_value(module.config[config_opt]),
        ]

        if (
            module.config._config[config_opt].validator
            and module.config._config[config_opt].validator.internal_id == "Hidden"
        ):
            additonal_button_row = (
                [
                    [
                        {
                            "text": self.strings("hide_value"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
                if force_hidden
                else [
                    [
                        {
                            "text": self.strings("show_hidden"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
            )
        else:
            additonal_button_row = []

        try:
            validator = module.config._config[config_opt].validator
            doc = utils.escape_html(
                next(
                    (
                        validator.doc[lang]
                        for lang in self._db.get(
                            translations.__name__, "lang", "en"
                        ).split(" ")
                        if lang in validator.doc
                    ),
                    validator.doc["en"],
                )
            )
        except Exception:
            doc = None
            validator = None
            args += [""]
        else:
            args += [
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
            ]
            if validator.internal_id == "Boolean":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_bool_markup(mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Series":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_series_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Choice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_choice_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "MultiChoice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_multi_choice_markup(
                        call, mod, config_opt, obj_type
                    ),
                )
                return

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(*args),
            reply_markup=additonal_button_row
            + [
                [
                    {
                        "text": self.strings("enter_value_btn"),
                        "input": self.strings("enter_value_desc"),
                        "handler": self.inline__set_config,
                        "args": (mod, config_opt, call.inline_message_id),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("set_default_btn"),
                        "callback": self.inline__reset_default,
                        "args": (mod, config_opt),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ],
            ],
        )

    async def inline__configure(
        self,
        call: InlineCall,
        mod: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        btns = [
            {
                "text": param,
                "callback": self.inline__configure_option,
                "args": (mod, param),
                "kwargs": {"obj_type": obj_type},
            }
            for param in self.lookup(mod).config
        ]

        await call.edit(
            self.strings(
                "configuring_mod" if isinstance(obj_type, bool) else "configuring_lib"
            ).format(
                utils.escape_html(mod),
                "\n".join(
                    [
                        f"âĢī¸ <code>{utils.escape_html(key)}</code>: <b>{{}}</b>".format(
                            self.prep_value(value)
                            if (
                                not self.lookup(mod).config._config[key].validator
                                or self.lookup(mod)
                                .config._config[key]
                                .validator.internal_id
                                != "Hidden"
                            )
                            else self.hide_value(value)
                        )
                        for key, value in self.lookup(mod).config.items()
                    ]
                ),
            ),
            reply_markup=list(utils.chunks(btns, 2))
            + [
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__choose_category(self, call: typing.Union[Message, InlineCall]):
        await utils.answer(
            call,
            self.strings("choose_core"),
            reply_markup=[
                [
                    {
                        "text": self.strings("builtin"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": True},
                    },
                    {
                        "text": self.strings("external"),
                        "callback": self.inline__global_config,
                    },
                ],
                *(
                    [
                        [
                            {
                                "text": self.strings("libraries"),
                                "callback": self.inline__global_config,
                                "kwargs": {"obj_type": "library"},
                            }
                        ]
                    ]
                    if self.allmodules.libraries
                    and any(hasattr(lib, "config") for lib in self.allmodules.libraries)
                    else []
                ),
                [{"text": self.strings("close_btn"), "action": "close"}],
            ],
        )

    async def inline__global_config(
        self,
        call: InlineCall,
        page: int = 0,
        obj_type: typing.Union[bool, str] = False,
    ):
        if isinstance(obj_type, bool):
            to_config = [
                mod.strings("name")
                for mod in self.allmodules.modules
                if hasattr(mod, "config")
                and callable(mod.strings)
                and (mod.__origin__.startswith("<core") or not obj_type)
                and (not mod.__origin__.startswith("<core") or obj_type)
            ]
        else:
            to_config = [
                lib.name for lib in self.allmodules.libraries if hasattr(lib, "config")
            ]

        to_config.sort()

        kb = []
        for mod_row in utils.chunks(
            to_config[
                page
                * self._num_rows
                * self._row_size : (page + 1)
                * self._num_rows
                * self._row_size
            ],
            3,
        ):
            row = [
                {
                    "text": btn,
                    "callback": self.inline__configure,
                    "args": (btn,),
                    "kwargs": {"obj_type": obj_type},
                }
                for btn in mod_row
            ]
            kb += [row]

        if len(to_config) > self._num_rows * self._row_size:
            kb += self.inline.build_pagination(
                callback=functools.partial(
                    self.inline__global_config, obj_type=obj_type
                ),
                total_pages=ceil(len(to_config) / (self._num_rows * self._row_size)),
                current_page=page + 1,
            )

        kb += [
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__choose_category,
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ]
        ]

        await call.edit(
            self.strings(
                "configure" if isinstance(obj_type, bool) else "configure_lib"
            ),
            reply_markup=kb,
        )

    @loader.command(
        ru_doc="ĐĐ°ŅŅŅĐžĐ¸ŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        de_doc="Konfiguriere Module",
        tr_doc="ModÃŧlleri yapÄąlandÄąr",
        hi_doc="ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤° ā¤ā¤°āĨā¤",
        uz_doc="Modullarni sozlash",
        ja_doc="ãĸã¸ãĨãŧãĢãč¨­åŽããžã",
        kr_doc="ëĒ¨ë ė¤ė ",
        ar_doc="ØĒŲŲŲŲ Ø§ŲŲØ­Ø¯Ø§ØĒ",
        es_doc="Configurar mÃŗdulos",
    )
    async def configcmd(self, message: Message):
        """Configure modules"""
        args = utils.get_args_raw(message)
        if self.lookup(args) and hasattr(self.lookup(args), "config"):
            form = await self.inline.form("đ", message)
            mod = self.lookup(args)
            if isinstance(mod, loader.Library):
                type_ = "library"
            else:
                type_ = mod.__origin__.startswith("<core")

            await self.inline__configure(form, args, obj_type=type_)
            return

        await self.inline__choose_category(message)

    @loader.command(
        ru_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> <ĐŊĐ°ŅŅŅĐžĐšĐēĐ°> <ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ> - ŅŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐēĐžĐŊŅĐ¸ĐŗĐ° Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ"
        ),
        de_doc=(
            "<Modul> <Einstellung> <Wert> - Setze den Wert der Konfiguration fÃŧr das"
            " Modul"
        ),
        tr_doc="<modÃŧl> <ayar> <deÄer> - ModÃŧl iÃ§in yapÄąlandÄąrma deÄerini ayarla",
        hi_doc="<ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛> <ā¤¸āĨā¤ā¤ŋā¤ā¤> <ā¤Žā¤žā¤¨> - ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤āĨ ā¤˛ā¤ŋā¤ ā¤āĨā¤¨āĨā¤Ģā¤ŧā¤ŋā¤ā¤°āĨā¤ļā¤¨ ā¤Žā¤žā¤¨ ā¤¸āĨā¤ ā¤ā¤°āĨā¤",
        uz_doc="<modul> <sozlash> <qiymat> - modul uchun sozlash qiymatini o'rnatish",
        ja_doc="<ãĸã¸ãĨãŧãĢ> <č¨­åŽ> <å¤> - ãĸã¸ãĨãŧãĢãŽč¨­åŽå¤ãč¨­åŽããžã",
        kr_doc="<ëĒ¨ë> <ė¤ė > <ę°> - ëĒ¨ëė ęĩŦėą ę°ė ė¤ė íŠëë¤",
        ar_doc="<ŲØ­Ø¯ØŠ> <ØĨØšØ¯Ø§Ø¯> <ŲŲŲØŠ> - ØĒØšŲŲŲ ŲŲŲØŠ Ø§ŲØĒŲŲŲŲ ŲŲŲØ­Ø¯ØŠ",
        es_doc=(
            "<mÃŗdulo> <configuraciÃŗn> <valor> - Establecer el valor de configuraciÃŗn"
        ),
    )
    async def fconfig(self, message: Message):
        """<module_name> <property_name> <config_value> - set the config value for the module
        """
        args = utils.get_args_raw(message).split(maxsplit=2)

        if len(args) < 3:
            await utils.answer(message, self.strings("args"))
            return

        mod, option, value = args

        instance = self.lookup(mod)
        if not instance:
            await utils.answer(message, self.strings("no_mod"))
            return

        if option not in instance.config:
            await utils.answer(message, self.strings("no_option"))
            return

        instance.config[option] = value
        await utils.answer(
            message,
            self.strings(
                "option_saved"
                if isinstance(instance, loader.Module)
                else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(instance.config[option])
                if not instance.config._config[option].validator
                or instance.config._config[option].validator.internal_id != "Hidden"
                else self.hide_value(instance.config[option]),
            ),
        )
