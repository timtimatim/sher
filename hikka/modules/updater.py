import asyncio
import atexit
import contextlib
import logging
import os
import subprocess
import sys
import time
import typing

import git
from git import GitCommandError, Repo

from telethon.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from telethon.tl.types import DialogFilter, Message
from telethon.extensions.html import CUSTOM_EMOJIS

from .. import loader, utils, main, version

from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class UpdaterMod(loader.Module):
    """Updates itself"""

    strings = {
        "name": "Updater",
        "source": (
            "<emoji document_id=5456255401194429832>๐</emoji> <b>Read the source code"
            " from</b> <a href='{}'>here</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Your {} is"
            " restarting...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Downloading"
            " updates...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Installing"
            " updates...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>โฑ</emoji> <b>Restart successful!"
            " {}</b>\n<i>But still loading modules...</i>\n<i>Restart took {}s</i>"
        ),
        "origin_cfg_doc": "Git origin URL, for where to update from",
        "btn_restart": "๐ Restart",
        "btn_update": "๐งญ Update",
        "restart_confirm": "โ <b>Are you sure you want to restart?</b>",
        "secure_boot_confirm": (
            "โ <b>Are you sure you want to restart in secure boot mode?</b>"
        ),
        "update_confirm": (
            "โ <b>Are you sure you"
            " want to update?\n\n<a"
           ' href="https://github.com/timtimatim/Bampi/commit{}">{}</a> โค <a'
            ' href="https://github.com/timtimatim/Bampi/commit{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>You are on the latest version, pull updates anyway?</b>",
        "cancel": "๐ซ Cancel",
        "lavhost_restart": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>Your {} is"
            " restarting...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>Your {} is"
            " updating...</b>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>๐</emoji> <b>Userbot is fully"
            " loaded! {}</b>\n<i>Full restart took {}s</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>Secure boot completed! {}</b>\n<i>Restart took {}s</i>"
        ),
    }

    strings_ru = {
        "source": (
            "<emoji document_id=5456255401194429832>๐</emoji> <b>ะััะพะดะฝัะน ะบะพะด ะผะพะถะฝะพ"
            " ะฟัะพัะธัะฐัั</b> <a href='{}'>ะทะดะตัั</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ะขะฒะพะน Bampi"
            " ะฟะตัะตะทะฐะณััะถะฐะตััั...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ะกะบะฐัะธะฒะฐะฝะธะต"
            " ะพะฑะฝะพะฒะปะตะฝะธะน...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ะฃััะฐะฝะพะฒะบะฐ"
            " ะพะฑะฝะพะฒะปะตะฝะธะน...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>โฑ</emoji> <b>ะะตัะตะทะฐะณััะทะบะฐ"
            " ััะฟะตัะฝะฐ! {}</b>\n<i>ะะพ ะผะพะดัะปะธ ะตัะต ะทะฐะณััะถะฐัััั...</i>\n<i>ะะตัะตะทะฐะณััะทะบะฐ"
            " ะทะฐะฝัะปะฐ {} ัะตะบ</i>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>๐</emoji> <b>Bampi ะฟะพะปะฝะพัััั"
            " ะทะฐะณััะถะตะฝ! {}</b>\n<i>ะะพะปะฝะฐั ะฟะตัะตะทะฐะณััะทะบะฐ ะทะฐะฝัะปะฐ {} ัะตะบ</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>ะะตะทะพะฟะฐัะฝะฐั ะทะฐะณััะทะบะฐ ะทะฐะฒะตััะตะฝะฐ! {}</b>\n<i>ะะตัะตะทะฐะณััะทะบะฐ ะทะฐะฝัะปะฐ {}"
            " ัะตะบ</i>"
        ),
        "origin_cfg_doc": "ะกััะปะบะฐ, ะธะท ะบะพัะพัะพะน ะฑัะดัั ะทะฐะณััะถะฐัััั ะพะฑะฝะพะฒะปะตะฝะธั",
        "btn_restart": "๐ ะะตัะตะทะฐะณััะทะธัััั",
        "btn_update": "๐งญ ะะฑะฝะพะฒะธัััั",
        "restart_confirm": "โ <b>ะขั ัะฒะตัะตะฝ, ััะพ ัะพัะตัั ะฟะตัะตะทะฐะณััะทะธัั Bampi?</b>",
        "secure_boot_confirm": (
            "โ <b>ะขั ัะฒะตัะตะฝ, ััะพ"
            " ัะพัะตัั ะฟะตัะตะทะฐะณััะทะธัััั ะฒ ัะตะถะธะผะต ะฑะตะทะพะฟะฐัะฝะพะน ะทะฐะณััะทะบะธ?</b>"
        ),
        "update_confirm": (
            "โ <b>ะขั ัะฒะตัะตะฝ, ััะพ"
            " ัะพัะตัั ะพะฑะฝะพะฒะธัััั??\n\n<a"
            ' href="https://github.com/timtimatim/Bampi/commit{}">{}</a> โค <a'
            ' href="https://github.com/timtimatim/Bampi/commit{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>ะฃ ัะตะฑั ะฟะพัะปะตะดะฝัั ะฒะตััะธั. ะะฑะฝะพะฒะธัััั ะฟัะธะฝัะดะธัะตะปัะฝะพ?</b>",
        "cancel": "๐ซ ะัะผะตะฝะฐ",
        "_cls_doc": "ะะฑะฝะพะฒะปัะตั ัะทะตัะฑะพั",
        "lavhost_restart": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>ะขะฒะพะน {}"
            " ะฟะตัะตะทะฐะณััะถะฐะตััั...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>ะขะฒะพะน {}"
            " ะพะฑะฝะพะฒะปัะตััั...</b>"
        ),
    }

    strings_ua = {
        "source": (
            "<emoji document_id=5456255401194429832>๐</emoji> <b>ะะธััะดะฝะธะน ะบะพะด ะผะพะถะฝะฐ"
            " ะฟัะพัะธัะฐัะธ</b> <a href='{}'>ััั</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ะขะฒัะน Bampi"
            " ะฟะตัะตะทะฐะฒะฐะฝัะฐะถัััััั...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ะะฐะฒะฐะฝัะฐะถะตะฝะฝั"
            " ะพะฝะพะฒะปะตะฝั...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ะััะฐะฝะพะฒะปะตะฝะฝั"
            " ะพะฝะพะฒะปะตะฝั...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>โฑ</emoji> <b>ะะตัะตะทะฐะฒะฐะฝัะฐะถะตะฝะฝั"
            " ััะฟััะฝo! {}</b>\n<i>ะะปะต ะผะพะดัะปั ัะต ะทะฐะฒะฐะฝัะฐะถัััััั...</i>\n<i>ะะตัะตะทะฐะฒะฐะฝัะฐะถะตะฝะฝั"
            " ะทะฐะนะฝัะปo {} ัะตะบ</i>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>๐</emoji> <b>Bampi ะฟะพะฒะฝัััั"
            " ะทะฐะฒะฐะฝัะฐะถะตะฝะธะน! {}</b>\n<i>ะะพะฒะฝะต ะฟะตัะตะทะฐะฒะฐะฝัะฐะถะตะฝะฝั ะทะฐะนะฝัะปะพ {} ัะตะบ</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>ะะตะทะฟะตัะฝะต ะทะฐะฒะฐะฝัะฐะถะตะฝะฝั ะทะฐะฒะตััะตะฝะพ! {}</b>\n<i>ะะตัะตะทะฐะฒะฐะฝัะฐะถะตะฝะฝั ะทะฐะนะฝัะปะพ {}"
            " ัะตะบ</i>"
        ),
        "origin_cfg_doc": "ะะพัะธะปะฐะฝะฝั, ะท ัะบะพะณะพ ะทะฐะฒะฐะฝัะฐะถัะฒะฐัะธะผะตัััั ะพะฝะพะฒะปะตะฝะฝั",
        "btn_restart": "๐ ะะตัะตะทะฐะฒะฐะฝัะฐะถะธัะธ",
        "btn_update": "๐งญ ะะฝะพะฒะธัะธัั",
        "restart_confirm": "โ <b>ะขะธ ะฒะฟะตะฒะฝะตะฝะธะน, ัะพ ัะพัะตั ะฟะตัะตะทะฐะฒะฐะฝัะฐะถะธัะธ Bampi?</b>",
        "secure_boot_confirm": (
            "โ <b>ะขะธ ะฒะฟะตะฒะฝะตะฝะธะน, ัะพ"
            " ัะพัะตั ะฟะตัะตะทะฐะฒะฐะฝัะฐะถะธัะธัั ั ัะตะถะธะผั ะฑะตะทะฟะตัะฝะพะณะพ ะทะฐะฒะฐะฝัะฐะถะตะฝะฝั?</b>"
        ),
        "update_confirm": (
            "โ <b>ะขะธ ะฒะฟะตะฒะฝะตะฝะธะน, ัะพ"
            " ัะพัะตั ะพะฝะพะฒะธัะธัั??\n\n<a"
            ' href="https://github.com/timtimatim/Bampi/commit{}">{}</a> โค <a'
            ' href="https://github.com/timtimatim/Bampi/commit{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>ะฃ ัะตะฑะต ะพััะฐะฝะฝั ะฒะตัััั. ะะฑะฝะพะฒะธัะธัั ะฟัะธะผััะพะฒะพ?</b>",
        "cancel": "๐ซ ัะบะฐััะฒะฐัะธ",
        "_cls_doc": "ะะฝะพะฒะปัั ัะทะตัะฑะพั",
        "lavhost_restart": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>ะขะฒัะน {}"
            " ะฟะตัะตะทะฐะฒะฐะฝัะฐะถัััััั...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>ะขะฒัะน {}"
            " ะพะฝะพะฒะปัััััั...</b>"
        ),
    }

    strings_de = {
        "source": (
            "<emoji document_id=5456255401194429832>๐</emoji> <b>Der Quellcode kann"
            " hier</b> <a href='{}'>gelesen</a> <b>werden</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Dein {}"
            " wird neugestartet...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Updates"
            " werden heruntergeladen...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Updates"
            " werden installiert...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>โฑ</emoji> <b>Neustart erfolgreich!"
            " {}</b>\n<i>Aber Module werden noch geladen...</i>\n<i>Neustart dauerte {}"
            " Sekunden</i>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>๐</emoji> <b>Dein Userbot ist"
            " vollstรคndig geladen! {}</b>\n<i>Vollstรคndiger Neustart dauerte {}"
            " Sekunden</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>Sicherer Bootvorgang abgeschlossen! {}</b>\n<i>Neustart dauerte"
            " {} Sekunden</i>"
        ),
        "origin_cfg_doc": "Link, von dem Updates heruntergeladen werden",
        "btn_restart": "๐ Neustart",
        "btn_update": "๐งญ Update",
        "restart_confirm": "โ <b>Bist du sicher, dass du neustarten willst?</b>",
        "secure_boot_confirm": (
            "โ <b>Bist du sicher, dass du in den sicheren Modus neustarten willst?</b>"
        ),
        "update_confirm": (
            "โ <b>Bist du sicher, dass"
            " du updaten willst??\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "๐ธ <b>Du hast die neueste Version. Willst du trotzdem updaten?</b>"
        ),
        "cancel": "๐ซ Abbrechen",
        "_cls_doc": "Aktualisiert den Userbot",
        "lavhost_restart": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>Dein {}"
            " wird neugestartet...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>Dein {}"
            " wird aktualisiert...</b>"
        ),
    }

    strings_hi = {
        "source": (
            "<emoji document_id=5456255401194429832>๐</emoji> <b>เคธเฅเคฐเฅเคธ เคเฅเคก เคฏเคนเคพเค เคชเคขเคผเคพ"
            " เคเคพ เคธเคเคคเคพ เคนเฅ</b> <a href='{}'>เคชเคขเคผเฅเค</a> <b>เคนเฅ</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>เคเคชเคเคพ {}"
            " เคซเคฟเคฐ เคธเฅ เคถเฅเคฐเฅ เคเคฟเคฏเคพ เคเคพ เคฐเคนเคพ เคนเฅ...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>เคเคชเคกเฅเค"
            " เคกเคพเคเคจเคฒเฅเคก เคนเฅ เคฐเคนเฅ เคนเฅเค...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>เคเคชเคกเฅเค"
            " เคเคเคธเฅเคเฅเคฒ เคนเฅ เคฐเคนเฅ เคนเฅเค...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>โฑ</emoji> <b>เคชเฅเคจเค เคเคฐเคเคญ"
            " เคธเคซเคฒ! {}</b>\n<i>เคฒเฅเคเคฟเคจ เคฎเฅเคกเฅเคฏเฅเคฒ เคญเฅ เคฒเฅเคก เคนเฅ เคฐเคนเฅ เคนเฅเค...</i>\n<i>เคชเฅเคจเค เคเคฐเคเคญ"
            " {} เคธเฅเคเคเคก เคฒเฅ เคเคฏเคพ</i>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>๐</emoji> <b>เคเคชเคเคพ เคฏเฅเคเคฐเคฌเฅเค เคชเฅเคฐเฅ เคคเคฐเคน"
            " เคธเฅ เคฒเฅเคก เคนเฅ เคเคฏเคพ เคนเฅ! {}</b>\n<i>เคชเฅเคฐเคพ เคชเฅเคจเค เคเคฐเคเคญ {} เคธเฅเคเคเคก เคฒเฅ เคเคฏเคพ</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>เคธเฅเคฐเคเฅเคทเคฟเคค เคฌเฅเค เคชเฅเคฐเคเฅเคฐเคฟเคฏเคพ เคชเฅเคฐเฅ เคนเฅ เคเค! {}</b>\n<i>เคชเฅเคจเค เคเคฐเคเคญ {}"
            " เคธเฅเคเคเคก เคฒเฅ เคเคฏเคพ</i>"
        ),
        "origin_cfg_doc": "เคธเฅ เคเคชเคกเฅเค เคกเคพเคเคจเคฒเฅเคก เคเคฟเคฏเคพ เคเคพเคเคเคพ",
        "btn_restart": "๐ เคชเฅเคจเค เคเคฐเคเคญ",
        "btn_update": "๐งญ เคเคชเคกเฅเค",
        "restart_confirm": "โ <b>เคเฅเคฏเคพ เคเคช เคตเคพเคเค เคชเฅเคจเค เคเคฐเคเคญ เคเคฐเคจเคพ เคเคพเคนเคคเฅ เคนเฅเค?</b>",
        "secure_boot_confirm": (
            "โ <b>เคเฅเคฏเคพ เคเคช เคตเคพเคเค เคธเฅเคฐเคเฅเคทเคฟเคค เคฎเฅเคก เคฎเฅเค เคชเฅเคจเค เคเคฐเคเคญ เคเคฐเคจเคพ เคเคพเคนเคคเฅ เคนเฅเค?</b>"
        ),
        "update_confirm": (
            "โ <b>เคเฅเคฏเคพ เคเคช เคตเคพเคเค เคเคชเคกเฅเค เคเคฐเคจเคพ เคเคพเคนเคคเฅ เคนเฅเค??\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "๐ธ <b>เคเคชเคเคพ เคจเคตเฅเคจเคคเคฎ เคธเคเคธเฅเคเคฐเคฃ เคนเฅเฅค เคเฅเคฏเคพ เคเคช เคญเฅ เคเคชเคกเฅเค เคเคฐเคจเคพ เคเคพเคนเคคเฅ เคนเฅเค?</b>"
        ),
        "cancel": "๐ซ เคฐเคฆเฅเคฆ เคเคฐเฅเค",
        "_cls_doc": "เคเคชเคฏเฅเคเคเคฐเฅเคคเคพ เคฌเฅเค เคเฅ เคเคชเคกเฅเค เคเคฐเคคเคพ เคนเฅ",
        "lavhost_restart": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>เคเคชเคเคพ {}"
            " เคชเฅเคจเค เคเคฐเคเคญ เคนเฅ เคฐเคนเคพ เคนเฅ...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>เคเคชเคเคพ {}"
            " เคเคชเคกเฅเค เคนเฅ เคฐเคนเคพ เคนเฅ...</b>"
        ),
    }

    strings_tr = {
        "source": (
            "<emoji document_id=5456255401194429832>๐</emoji> <b>Manba kodini shu <a"
            " href='{}'>yerdan</a> oสปqing</b>"
        ),
        "restarting": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{}"
            " yeniden baลlatฤฑlฤฑyor...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{}"
            " yeniden baลlatฤฑlฤฑyor...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Gรผncelleme"
            " indiriliyor...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Gรผncelleme"
            " yรผkleniyor...</b>"
        ),
        "success": (
            "<emoji document_id=6321050180095313397>โฑ</emoji> <b>Yeniden baลlatma"
            " baลarฤฑlฤฑ! {}</b>\n<i>Modรผller yรผkleniyor...</i>\n<i>Yeniden baลlatma {}"
            " saniye sรผrdรผ</i>"
        ),
        "full_success": (
            "<emoji document_id=6323332130579416910>๐</emoji> <b>Botunuz tamamen"
            " yรผklendi! {}</b>\n<i>Toplam yeniden baลlatma {} saniye sรผrdรผ</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>Gรผvenli mod baลarฤฑyla tamamlandฤฑ! {}</b>\n<i>Yeniden baลlatma {}"
            " saniye sรผrdรผ</i>"
        ),
        "origin_cfg_doc": "dan gรผncelleme indirilecek",
        "btn_restart": "๐ Yeniden baลlat",
        "btn_update": "๐งญ Gรผncelle",
        "restart_confirm": "โ <b>Gerรงekten yeniden baลlatmak istiyor musunuz?</b>",
        "secure_boot_confirm": (
            "โ <b>Gerรงekten gรผvenli modda yeniden baลlatmak istiyor musunuz?</b>"
        ),
        "update_confirm": (
            "โ <b>Gerรงekten gรผncellemek istiyor musunuz??\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>Zaten son sรผrรผmรผnรผz. Gรผncelleme yapmak ister misiniz?</b>",
        "cancel": "๐ซ ฤฐptal",
        "_cls_doc": "Kullanฤฑcฤฑ botunu gรผnceller",
        "lavhost_restart": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{}"
            " yeniden baลlatฤฑlฤฑyor...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{}"
            " gรผncelleniyor...</b>"
        ),
    }

    strings_uz = {
        "restarting": (
            "<emoji document_id=5469986291380657759>๐</emoji> <b>{}"
            " qayta ishga tushirilmoqda...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=5469986291380657759>๐</emoji> <b>{}"
            " qayta ishga tushirilmoqda...</b>"
        ),
        "downloading": (
            "<emoji document_id=5469986291380657759>๐</emoji> <b>Yangilanish"
            " yuklanmoqda...</b>"
        ),
        "installing": (
            "<emoji document_id=5469986291380657759>๐</emoji> <b>Yangilanish"
            " o'rnatilmoqda...</b>"
        ),
        "success": (
            "<emoji document_id=5469986291380657759>โฑ</emoji> <b>Qayta ishga tushirish"
            " muvaffaqiyatli yakunlandi! {}</b>\n<i>Modullar"
            " yuklanmoqda...</i>\n<i>Qayta ishga tushirish {} soniya davom etdi</i>"
        ),
        "full_success": (
            "<emoji document_id=5469986291380657759>๐</emoji> <b>Sizning botingiz"
            " to'liq yuklandi! {}</b>\n<i>Jami qayta ishga tushirish {} soniya davom"
            " etdi</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>Xavfsiz rejim muvaffaqiyatli yakunlandi! {}</b>\n<i>Qayta ishga"
            " tushirish {} soniya davom etdi</i>"
        ),
        "origin_cfg_doc": "dan yangilanish yuklanadi",
        "btn_restart": "๐ Qayta ishga tushirish",
        "btn_update": "๐งญ Yangilash",
        "restart_confirm": "โ <b>Haqiqatan ham qayta ishga tushirmoqchimisiz?</b>",
        "secure_boot_confirm": (
            "โ <b>Haqiqatan ham xavfsiz rejimda qayta ishga tushirmoqchimisiz?</b>"
        ),
        "update_confirm": (
            "โ <b>Haqiqatan ham yangilamoqchimisiz??\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "๐ธ <b>Siz allaqachon eng so'nggi versiyasiz. Yangilamoqchimisiz?</b>"
        ),
        "cancel": "๐ซ Bekor qilish",
        "_cls_doc": "Foydalanuvchi botini yangilaydi",
        "lavhost_restart": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>{}"
            " qayta ishga tushirilmoqda...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>โ๏ธ</emoji> <b>{}"
            " yangilanmoqda...</b>"
        ),
    }

    strings_ja = {
        "restarting": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{} ๅ่ตทๅไธญ...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{} ๅ่ตทๅไธญ...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ใขใใใใผใใใใฆใณใญใผใไธญ...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ใขใใใใผใใใคใณในใใผใซไธญ...</b>"
        ),
        "success": (
            "<emoji document_id=6318970114548958978>โฑ</emoji> <b>ๅ่ตทๅใๅฎไบใใพใใ!"
            " {}</b>\n<i>ใขใธใฅใผใซใใใฆใณใญใผใไธญ...</i>\n<i>ๅ่ตทๅ {} ็งใใใใพใใ</i>"
        ),
        "full_success": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ใใชใใฎใใใใฏๅฎๅจใซ"
            "ใใฆใณใญใผใใใใพใใ! {}</b>\n<i>ๅ่ตทๅ {} ็งใใใใพใใ</i>"
        ),
        "secure_boot_complete": "๐ <b>ใปใญใฅใขใขใผใใๅฎไบใใพใใ! {}</b>\n<i>ๅ่ตทๅ {} ็งใใใใพใใ</i>",
        "origin_cfg_doc": "ใใใขใใใใผใใใใฆใณใญใผใ",
        "btn_restart": "๐ ๅ่ตทๅ",
        "btn_update": "๐งญ ใขใใใใผใ",
        "restart_confirm": "โ <b>ๆฌๅฝใซๅ่ตทๅใใพใใ๏ผ</b>",
        "secure_boot_confirm": "โ <b>ๆฌๅฝใซใปใญใฅใขใขใผใใงๅ่ตทๅใใพใใ๏ผ</b>",
        "update_confirm": (
            "โ <b>ๆฌๅฝใซใขใใใใผใใใพใใ๏ผ\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>ใใงใซๆๆฐใใผใธใงใณใงใใใขใใใใผใใใพใใ๏ผ</b>",
        "cancel": "๐ซ ใญใฃใณใปใซ",
        "_cls_doc": "ใฆใผใถใผใใใใใใขใใใใผใใใพใ",
        "lavhost_restart": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{} ๅ่ตทๅไธญ...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{} ใขใใใใผใไธญ...</b>"
        ),
    }

    strings_kr = {
        "restarting": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{} ์ฌ์์ ์ค...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{} ์ฌ์์ ์ค...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>์๋ฐ์ดํธ ๋ค์ด๋ก๋ ์ค...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>์๋ฐ์ดํธ ์ค์น ์ค...</b>"
        ),
        "success": (
            "<emoji document_id=6318970114548958978>โฑ</emoji> <b>์ฌ์์์ด ์๋ฃ๋์์ต๋๋ค!"
            " {}</b>\n<i>๋ชจ๋์๋ค์ด๋ก๋ ์ค...</i>\n<i>์ฌ์์ {} ์ด ๊ฑธ๋?ธ์ต๋๋ค</i>"
        ),
        "full_success": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>๋น์?์ ๋ด์ ์์?ํ"
            "๋ค์ด๋ก๋ ๋์์ต๋๋ค! {}</b>\n<i>์ฌ์์ {} ์ด ๊ฑธ๋?ธ์ต๋๋ค</i>"
        ),
        "secure_boot_complete": "๐ <b>๋ณด์ ๋ชจ๋๊ฐ ์๋ฃ๋์์ต๋๋ค! {}</b>\n<i>์ฌ์์ {} ์ด ๊ฑธ๋?ธ์ต๋๋ค</i>",
        "origin_cfg_doc": "์์ ์๋ฐ์ดํธ ๋ค์ด๋ก๋",
        "btn_restart": "๐ ์ฌ์์",
        "btn_update": "๐งญ ์๋ฐ์ดํธ",
        "restart_confirm": "โ <b>์ฌ์์ ํ์๊ฒ?์ต๋๊น?</b>",
        "secure_boot_confirm": "โ <b>๋ณด์ ๋ชจ๋๋ก ์ฌ์์ ํ์๊ฒ?์ต๋๊น?</b>",
        "update_confirm": (
            "โ <b>์๋ฐ์ดํธ ํ์๊ฒ?์ต๋๊น?\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>์ด๋ฏธ ์ต์? ๋ฒ์?์๋๋ค. ์๋ฐ์ดํธ ํ์๊ฒ?์ต๋๊น?</b>",
        "cancel": "๐ซ ์ทจ์",
        "_cls_doc": "์ฌ์ฉ์๊ฐ ๋ด ์๋ฐ์ดํธ",
        "lavhost_restart": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{} ์ฌ์์ ์ค...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{} ์๋ฐ์ดํธ ์ค...</b>"
        ),
    }

    strings_ar = {
        "restarting": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{}"
            " ุฅุนุงุฏุฉ ุงูุชุดุบูู...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{}"
            " ุฅุนุงุฏุฉ ุงูุชุดุบูู...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ุชุญููู ุงูุชุญุฏูุซ...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ุชุซุจูุช ุงูุชุญุฏูุซ...</b>"
        ),
        "success": (
            "<emoji document_id=6318970114548958978>โฑ</emoji> <b>ุชู ุฅุนุงุฏุฉ ุงูุชุดุบูู"
            " ุจูุฌุงุญ! {}</b>\n<i>ุฌุงุฑู ุชูุฒููุงููุญุฏุงุช...</i>\n<i>ุฃุณุชุบุฑู ุฅุนุงุฏุฉ ุงูุชุดุบูู {}"
            " ุซุงููุฉ</i>"
        ),
        "full_success": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ุชู ุชุญููู ุงูุจูุช ุจูุฌุงุญ!"
            " {}</b>\n<i>ุฃุณุชุบุฑู ุฅุนุงุฏุฉ ุงูุชุดุบูู {} ุซุงููุฉ</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>ุชู ุฅููุงู ูุถุน ุงูุฅููุงุน ุงูุขูู! {}</b>\n<i>ุฃุณุชุบุฑู ุฅุนุงุฏุฉ ุงูุชุดุบูู {}"
            " ุซุงููุฉ</i>"
        ),
        "origin_cfg_doc": "ุชุญููู ุงูุชุญุฏูุซ ูู",
        "btn_restart": "๐ ุฅุนุงุฏุฉ ุงูุชุดุบูู",
        "btn_update": "๐งญ ุชุญุฏูุซ",
        "restart_confirm": "โ <b>ูู ุชุฑูุฏ ุฅุนุงุฏุฉ ุงูุชุดุบููุ</b>",
        "secure_boot_confirm": "โ <b>ูู ุชุฑูุฏ ุฅุนุงุฏุฉ ุงูุชุดุบูู ูู ูุถุน ุงูุฅููุงุน ุงูุขููุ</b>",
        "update_confirm": (
            "โ <b>ูู ุชุฑูุฏ ุชุญุฏูุซุ\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>ูุฐุง ูู ุขุฎุฑ ุฅุตุฏุงุฑ. ูู ุชุฑูุฏ ุชุญุฏูุซุ</b>",
        "cancel": "๐ซ ุฅูุบุงุก",
        "_cls_doc": "ุงููุณุชุฎุฏู ูุนูุฏ ุชุดุบูู ุงูุจูุช",
        "lavhost_restart": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{}"
            " ุฅุนุงุฏุฉ ุงูุชุดุบูู...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{} ุชุญุฏูุซ...</b>"
        ),
    }

    strings_es = {
        "restarting": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{} Reiniciando...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>{} Reiniciando...</b>"
        ),
        "downloading": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Descargando la"
            " actualizaciรณn...</b>"
        ),
        "installing": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>Instalando la"
            " actualizaciรณn...</b>"
        ),
        "success": (
            "<emoji document_id=6318970114548958978>โฑ</emoji> <b>Reiniciado con รฉxito!"
            " {}</b>\n<i>Descargandomรณdulos...</i>\n<i>Reiniciado en {} segundos</i>"
        ),
        "full_success": (
            "<emoji document_id=6318970114548958978>๐</emoji> <b>ยกBot actualizado con"
            " รฉxito! {}</b>\n<i>Reiniciado en {} segundos</i>"
        ),
        "secure_boot_complete": (
            "๐ <b>ยกModo de arranque seguro activado! {}</b>\n<i>Reiniciado en {}"
            " segundos</i>"
        ),
        "origin_cfg_doc": "Descargar actualizaciรณn desde",
        "btn_restart": "๐ Reiniciar",
        "btn_update": "๐งญ Actualizar",
        "restart_confirm": "โ <b>ยฟQuieres reiniciar?</b>",
        "secure_boot_confirm": (
            "โ <b>ยฟQuieres reiniciar en modo de arranque seguro?</b>"
        ),
        "update_confirm": (
            "โ <b>ยฟQuieres actualizar?\n\n<a"
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a> โค <a'
            ' href="https://github.com/hikariatama/Bampi/commit/{}">{}</a></b>'
        ),
        "no_update": "๐ธ <b>Esta es la รบltima versiรณn. ยฟQuieres actualizar?</b>",
        "cancel": "๐ซ Cancelar",
        "_cls_doc": "El usuario reinicia el bot",
        "lavhost_restart": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{} Reiniciando...</b>"
        ),
        "lavhost_update": (
            "<emoji document_id=6318970114548958978>โ๏ธ</emoji> <b>{}"
            " Actualizando...</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GIT_ORIGIN_URL",
                "https://github.com/hikariatama/Bampi",
                lambda: self.strings("origin_cfg_doc"),
                validator=loader.validators.Link(),
            )
        )

    @loader.owner
    @loader.command(
        ru_doc="ะะตัะตะทะฐะณััะถะฐะตั ัะทะตัะฑะพั",
        de_doc="Startet den Userbot neu",
        tr_doc="Kullanฤฑcฤฑ botunu yeniden baลlatฤฑr",
        uz_doc="Foydalanuvchi botini qayta ishga tushiradi",
        hi_doc="เคเคชเคฏเฅเคเคเคฐเฅเคคเคพ เคฌเฅเค เคเฅ เคฐเฅเคธเฅเคเคพเคฐเฅเค เคเคฐเคคเคพ เคนเฅ",
        ja_doc="ใฆใผใถใผใใใใๅ่ตทๅใใพใ",
        kr_doc="์ฌ์ฉ์ ๋ด์ ๋ค์ ์์ํฉ๋๋ค",
        ar_doc="ูุนูุฏ ุชุดุบูู ุงูุจูุช",
        es_doc="Reinicia el bot",
    )
    async def restart(self, message: Message):
        """Restarts the userbot"""
        secure_boot = "--secure-boot" in utils.get_args_raw(message)
        try:
            if (
                "--force" in (utils.get_args_raw(message) or "")
                or "-f" in (utils.get_args_raw(message) or "")
                or not self.inline.init_complete
                or not await self.inline.form(
                    message=message,
                    text=self.strings(
                        "secure_boot_confirm" if secure_boot else "restart_confirm"
                    ),
                    reply_markup=[
                        {
                            "text": self.strings("btn_restart"),
                            "callback": self.inline_restart,
                            "args": (secure_boot,),
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                )
            ):
                raise
        except Exception:
            await self.restart_common(message, secure_boot)

    async def inline_restart(self, call: InlineCall, secure_boot: bool = False):
        await self.restart_common(call, secure_boot=secure_boot)

    async def process_restart_message(self, msg_obj: typing.Union[InlineCall, Message]):
        self.set(
            "selfupdatemsg",
            msg_obj.inline_message_id
            if hasattr(msg_obj, "inline_message_id")
            else f"{utils.get_chat_id(msg_obj)}:{msg_obj.id}",
        )

    async def restart_common(
        self,
        msg_obj: typing.Union[InlineCall, Message],
        secure_boot: bool = False,
    ):
        if (
            hasattr(msg_obj, "form")
            and isinstance(msg_obj.form, dict)
            and "uid" in msg_obj.form
            and msg_obj.form["uid"] in self.inline._units
            and "message" in self.inline._units[msg_obj.form["uid"]]
        ):
            message = self.inline._units[msg_obj.form["uid"]]["message"]
        else:
            message = msg_obj

        if secure_boot:
            self._db.set(loader.__name__, "secure_boot", True)

        msg_obj = await utils.answer(
            msg_obj,
            self.strings("restarting_caption").format(
                utils.get_platform_emoji(self._client)
                if self._client.Bampi_me.premium
                and CUSTOM_EMOJIS
                and isinstance(msg_obj, Message)
                else "Bampi"
            )
            if "LAVHOST" not in os.environ
            else self.strings("lavhost_restart").format(
                '</b><emoji document_id="5192756799647785066">โ๏ธ</emoji><emoji'
                ' document_id="5193117564015747203">โ๏ธ</emoji><emoji'
                ' document_id="5195050806105087456">โ๏ธ</emoji><emoji'
                ' document_id="5195457642587233944">โ๏ธ</emoji><b>'
                if self._client.Bampi_me.premium
                and CUSTOM_EMOJIS
                and isinstance(msg_obj, Message)
                else "lavHost"
            ),
        )

        await self.process_restart_message(msg_obj)

        self.set("restart_ts", time.time())

        await self._db.remote_force_save()

        if "LAVHOST" in os.environ:
            os.system("lavhost restart")
            return

        with contextlib.suppress(Exception):
            await main.Bampi.web.stop()

        atexit.register(restart, *sys.argv[1:])
        handler = logging.getLogger().handlers[0]
        handler.setLevel(logging.CRITICAL)

        for client in self.allclients:
            # Terminate main loop of all running clients
            # Won't work if not all clients are ready
            if client is not message.client:
                await client.disconnect()

        await message.client.disconnect()
        sys.exit(0)

    async def download_common(self):
        try:
            repo = Repo(os.path.dirname(utils.get_base_dir()))
            origin = repo.remote("origin")
            r = origin.pull()
            new_commit = repo.head.commit
            for info in r:
                if info.old_commit:
                    for d in new_commit.diff(info.old_commit):
                        if d.b_path == "requirements.txt":
                            return True
            return False
        except git.exc.InvalidGitRepositoryError:
            repo = Repo.init(os.path.dirname(utils.get_base_dir()))
            origin = repo.create_remote("origin", self.config["GIT_ORIGIN_URL"])
            origin.fetch()
            repo.create_head("master", origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            return False

    @staticmethod
    def req_common():
        # Now we have downloaded new code, install requirements
        logger.debug("Installing new requirements...")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.join(
                        os.path.dirname(utils.get_base_dir()),
                        "requirements.txt",
                    ),
                    "--user",
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            logger.exception("Req install failed")

    @loader.owner
    @loader.command(
        ru_doc="ะกะบะฐัะธะฒะฐะตั ะพะฑะฝะพะฒะปะตะฝะธั ัะทะตัะฑะพัะฐ",
        de_doc="Lรคdt Updates fรผr den Userbot herunter",
        tr_doc="Userbot gรผncellemelerini indirir",
        uz_doc="Userbot yangilanishlarini yuklaydi",
        hi_doc="เคฏเฅเคเคฐเคฌเฅเค เคเฅ เคเคชเคกเฅเค เคกเคพเคเคจเคฒเฅเคก เคเคฐเคคเคพ เคนเฅ",
        ja_doc="ใฆใผใถใผใใใใฎใขใใใใผใใใใฆใณใญใผใใใพใ",
        kr_doc="์?์?๋ด ์๋ฐ์ดํธ๋ฅผ ๋ค์ด๋ก๋ํฉ๋๋ค",
        ar_doc="ูููู ุจุชุญููู ุชุญุฏูุซุงุช ุงูุจูุช",
        es_doc="Descarga las actualizaciones del bot",
    )
    async def update(self, message: Message):
        """Downloads userbot updates"""
        try:
            current = utils.get_git_hash()
            upcoming = next(
                git.Repo().iter_commits(f"origin/{version.branch}", max_count=1)
            ).hexsha
            if (
                "--force" in (utils.get_args_raw(message) or "")
                or "-f" in (utils.get_args_raw(message) or "")
                or not self.inline.init_complete
                or not await self.inline.form(
                    message=message,
                    text=self.strings("update_confirm").format(
                        current, current[:8], upcoming, upcoming[:8]
                    )
                    if upcoming != current
                    else self.strings("no_update"),
                    reply_markup=[
                        {
                            "text": self.strings("btn_update"),
                            "callback": self.inline_update,
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                )
            ):
                raise
        except Exception:
            await self.inline_update(message)

    async def inline_update(
        self,
        msg_obj: typing.Union[InlineCall, Message],
        hard: bool = False,
    ):
        # We don't really care about asyncio at this point, as we are shutting down
        if hard:
            os.system(f"cd {utils.get_base_dir()} && cd .. && git reset --hard HEAD")

        try:
            if "LAVHOST" in os.environ:
                msg_obj = await utils.answer(
                    msg_obj,
                    self.strings("lavhost_update").format(
                        "</b><emoji document_id=5192756799647785066>โ๏ธ</emoji><emoji"
                        " document_id=5193117564015747203>โ๏ธ</emoji><emoji"
                        " document_id=5195050806105087456>โ๏ธ</emoji><emoji"
                        " document_id=5195457642587233944>โ๏ธ</emoji><b>"
                        if self._client.Bampi_me.premium
                        and CUSTOM_EMOJIS
                        and isinstance(msg_obj, Message)
                        else "lavHost"
                    ),
                )
                await self.process_restart_message(msg_obj)
                os.system("lavhost update")
                return

            with contextlib.suppress(Exception):
                msg_obj = await utils.answer(msg_obj, self.strings("downloading"))
            req_update = await self.download_common()

            with contextlib.suppress(Exception):
                msg_obj = await utils.answer(msg_obj, self.strings("installing"))
            if req_update:
                self.req_common()

            await self.restart_common(msg_obj)
        except GitCommandError:
            if not hard:
                await self.inline_update(msg_obj, True)
                return

            logger.critical("Got update loop. Update manually via .terminal")
            return

    @loader.unrestricted
    @loader.command(
        ru_doc="ะะพะบะฐะทะฐัั ัััะปะบั ะฝะฐ ะธััะพะดะฝัะน ะบะพะด ะฟัะพะตะบัะฐ",
        de_doc="Zeigt den Link zum Quellcode des Projekts an",
        tr_doc="Proje kaynak kodu baฤlantฤฑsฤฑnฤฑ gรถsterir",
        uz_doc="Loyihaning manba kodiga havola ko'rsatadi",
        hi_doc="เคชเฅเคฐเฅเคเฅเคเฅเค เคเฅเคก เคเคพ เคฒเคฟเคเค เคฆเคฟเคเคพเคเค",
        ja_doc="ใใญใธใงใฏใใฎใฝใผในใณใผใใธใฎใชใณใฏใ่กจ็คบใใพใ",
        kr_doc="ํ๋ก์?ํธ ์์ค ์ฝ๋ ๋งํฌ๋ฅผ ํ์ํฉ๋๋ค",
        ar_doc="ูุนุฑุถ ุฑุงุจุท ูุตุฏุฑ ุงูุจูุช",
        es_doc="Muestra el enlace al cรณdigo fuente del proyecto",
    )
    async def source(self, message: Message):
        """Links the source code of this project"""
        await utils.answer(
            message,
            self.strings("source").format(self.config["GIT_ORIGIN_URL"]),
        )

    async def client_ready(self):
        if self.get("selfupdatemsg") is not None:
            try:
                await self.update_complete()
            except Exception:
                logger.exception("Failed to complete update!")

        if self.get("do_not_create", False):
            return

        try:
            await self._add_folder()
        except Exception:
            logger.exception("Failed to add folder!")
        finally:
            self.set("do_not_create", True)

    async def _add_folder(self):
        folders = await self._client(GetDialogFiltersRequest())

        if any(getattr(folder, "title", None) == "Bampi" for folder in folders):
            return

        try:
            folder_id = (
                max(
                    folders,
                    key=lambda x: x.id,
                ).id
                + 1
            )
        except ValueError:
            folder_id = 2

        try:
            await self._client(
                UpdateDialogFilterRequest(
                    folder_id,
                    DialogFilter(
                        folder_id,
                        title="Bampi",
                        pinned_peers=(
                            [
                                await self._client.get_input_entity(
                                    self._client.loader.inline.bot_id
                                )
                            ]
                            if self._client.loader.inline.init_complete
                            else []
                        ),
                        include_peers=[
                            await self._client.get_input_entity(dialog.entity)
                            async for dialog in self._client.iter_dialogs(
                                None,
                                ignore_migrated=True,
                            )
                            if dialog.name
                            in {
                                "Bampi-logs",
                                "Bampi-onload",
                                "Bampi-assets",
                                "Bampi-backups",
                                "Bampi-acc-switcher",
                                "silent-tags",
                            }
                            and dialog.is_channel
                            and (
                                dialog.entity.participants_count == 1
                                or dialog.entity.participants_count == 2
                                and dialog.name in {"Bampi-logs", "silent-tags"}
                            )
                            or (
                                self._client.loader.inline.init_complete
                                and dialog.entity.id
                                == self._client.loader.inline.bot_id
                            )
                            or dialog.entity.id
                            in [
                                1554874075,
                                1697279580,
                                1679998924,
                            ]  # official Bampi chats
                        ],
                        emoticon="๐ฑ",
                        exclude_peers=[],
                        contacts=False,
                        non_contacts=False,
                        groups=False,
                        broadcasts=False,
                        bots=False,
                        exclude_muted=False,
                        exclude_read=False,
                        exclude_archived=False,
                    ),
                )
            )
        except Exception:
            logger.critical(
                "Can't create Bampi folder. Possible reasons are:\n"
                "- User reached the limit of folders in Telegram\n"
                "- User got floodwait\n"
                "Ignoring error and adding folder addition to ignore list"
            )

    async def update_complete(self):
        logger.debug("Self update successful! Edit message")
        start = self.get("restart_ts")
        try:
            took = round(time.time() - start)
        except Exception:
            took = "n/a"

        msg = self.strings("success").format(utils.ascii_face(), took)
        ms = self.get("selfupdatemsg")

        if ":" in str(ms):
            chat_id, message_id = ms.split(":")
            chat_id, message_id = int(chat_id), int(message_id)
            await self._client.edit_message(chat_id, message_id, msg)
            return

        await self.inline.bot.edit_message_text(
            inline_message_id=ms,
            text=self.inline.sanitise_text(msg),
        )

    async def full_restart_complete(self, secure_boot: bool = False):
        start = self.get("restart_ts")

        try:
            took = round(time.time() - start)
        except Exception:
            took = "n/a"

        self.set("restart_ts", None)

        ms = self.get("selfupdatemsg")
        msg = self.strings(
            "secure_boot_complete" if secure_boot else "full_success"
        ).format(utils.ascii_face(), took)

        if ms is None:
            return

        self.set("selfupdatemsg", None)

        if ":" in str(ms):
            chat_id, message_id = ms.split(":")
            chat_id, message_id = int(chat_id), int(message_id)
            await self._client.edit_message(chat_id, message_id, msg)
            await asyncio.sleep(60)
            await self._client.delete_messages(chat_id, message_id)
            return

        await self.inline.bot.edit_message_text(
            inline_message_id=ms,
            text=self.inline.sanitise_text(msg),
        )


def restart(*argv):
    os.execl(
        sys.executable,
        sys.executable,
        "-m",
        os.path.relpath(utils.get_base_dir()),
        *argv,
    )
