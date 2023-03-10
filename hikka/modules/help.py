import difflib
import inspect
import logging

from telethon.tl.types import Message
from telethon.extensions.html import CUSTOM_EMOJIS

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class HelpMod(loader.Module):
    """Shows help for modules and commands"""

    strings = {
        "name": "Help",
        "bad_module": "<b>š« <b>Module</b> <code>{}</code> <b>not found</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ No docs",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} mods available,"
            " {} hidden:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>Specify module to hide</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} modules hidden,"
            " {} modules shown:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ No docs",
        "support": (
            "{} <b>Link to </b><a href='https://t.me/Bampi_talks'>support chat</a></b>"
        ),
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Userbot is not"
            " fully loaded, so not all modules are shown</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>No exact match"
            " occured, so the closest result is shown instead</b>"
        ),
        "request_join": "You requested link for Bampi support chat",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>This is a core"
            " module. You can't unload it nor replace</b>"
        ),
    }

    strings_ru = {
        "bad_module": "<b>š« <b>ŠŠ¾Š“ŃŠ»Ń</b> <code>{}</code> <b>Š½Šµ Š½Š°Š¹Š“ŠµŠ½</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ ŠŠµŃ Š¾ŠæŠøŃŠ°Š½ŠøŃ",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} Š¼Š¾Š“ŃŠ»ŠµŠ¹ Š“Š¾ŃŃŃŠæŠ½Š¾,"
            " {} ŃŠŗŃŃŃŠ¾:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>Š£ŠŗŠ°Š¶Šø Š¼Š¾Š“ŃŠ»Ń(-Šø), ŠŗŠ¾ŃŠ¾ŃŃŠµ Š½ŃŠ¶Š½Š¾ ŃŠŗŃŃŃŃ</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} Š¼Š¾Š“ŃŠ»ŠµŠ¹ ŃŠŗŃŃŃŠ¾,"
            " {} Š¼Š¾Š“ŃŠ»ŠµŠ¹ ŠæŠ¾ŠŗŠ°Š·Š°Š½Š¾:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ ŠŠµŃ Š¾ŠæŠøŃŠ°Š½ŠøŃ",
        "support": (
            "{} <b>Š”ŃŃŠ»ŠŗŠ° Š½Š° </b><a href='https://t.me/Bampi_talks'>ŃŠ°Ń ŠæŠ¾Š¼Š¾ŃŠø</a></b>"
        ),
        "_cls_doc": "ŠŠ¾ŠŗŠ°Š·ŃŠ²Š°ŠµŃ ŠæŠ¾Š¼Š¾ŃŃ ŠæŠ¾ Š¼Š¾Š“ŃŠ»ŃŠ¼",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Š®Š·ŠµŃŠ±Š¾Ń ŠµŃŠµ Š½Šµ"
            " Š·Š°Š³ŃŃŠ·ŠøŠ»ŃŃ ŠæŠ¾Š»Š½Š¾ŃŃŃŃ, ŠæŠ¾ŃŃŠ¾Š¼Ń ŠæŠ¾ŠŗŠ°Š·Š°Š½Ń Š½Šµ Š²ŃŠµ Š¼Š¾Š“ŃŠ»Šø</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Š¢Š¾ŃŠ½Š¾Š³Š¾ ŃŠ¾Š²ŠæŠ°Š“ŠµŠ½ŠøŃ"
            " Š½Šµ Š½Š°ŃŠ»Š¾ŃŃ, ŠæŠ¾ŃŃŠ¾Š¼Ń Š±ŃŠ»Š¾ Š²ŃŠ±ŃŠ°Š½Š¾ Š½Š°ŠøŠ±Š¾Š»ŠµŠµ ŠæŠ¾Š“ŃŠ¾Š“ŃŃŠµŠµ</b>"
        ),
        "request_join": "ŠŃ Š·Š°ŠæŃŠ¾ŃŠøŠ»Šø ŃŃŃŠ»ŠŗŃ Š½Š° ŃŠ°Ń ŠæŠ¾Š¼Š¾ŃŠø Bampi",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Š­ŃŠ¾ Š²ŃŃŃŠ¾ŠµŠ½Š½ŃŠ¹"
            " Š¼Š¾Š“ŃŠ»Ń. ŠŃ Š½Šµ Š¼Š¾Š¶ŠµŃŠµ ŠµŠ³Š¾ Š²ŃŠ³ŃŃŠ·ŠøŃŃ ŠøŠ»Šø Š·Š°Š¼ŠµŠ½ŠøŃŃ</b>"
        ),
    }

    strings_de = {
        "bad_module": "<b>š« <b>Modul</b> <code>{}</code> <b>nicht gefunden</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ Keine Dokumentation",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} Module verfĆ¼gbar,"
            " {} versteckt:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>Gib das Modul an, das du verstecken willst</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} Module versteckt,"
            " {} Module angezeigt:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ Keine Dokumentation",
        "support": (
            "{} <b>Link zum </b><a href='https://t.me/Bampi_talks'>Supportchat</a></b>"
        ),
        "_cls_doc": "Zeigt Hilfe zu Modulen an",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Der Userbot ist noch"
            " nicht vollstĆ¤ndig geladen, daher werden nicht alle Module angezeigt</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Es wurde kein exakter"
            " Treffer gefunden, daher wird das nĆ¤chstbeste Ergebnis angezeigt</b>"
        ),
        "request_join": "Du hast den Link zum Supportchat angefordert",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Dies ist ein"
            " eingebauter Modul. Du kannst ihn nicht entladen oder ersetzen</b>"
        ),
    }

    strings_tr = {
        "bad_module": "<b>š« <b>ModĆ¼l</b> <code>{}</code> <b>bulunamadÄ±</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ DokĆ¼mantasyon yok",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} adet modĆ¼l mevcut,"
            " {} gizli:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>Gizlemek istediÄin modĆ¼lĆ¼ belirt</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} adet modĆ¼l"
            " gizlendi, {} adet modĆ¼l gĆ¶sterildi:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ DokĆ¼mantasyon yok",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>Destek sohbeti</a></b>",
        "_cls_doc": "ModĆ¼l yardÄ±mÄ±nÄ± gĆ¶sterir",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>KullanÄ±cÄ± botu"
            " henĆ¼z tam olarak yĆ¼klenmediÄinden, tĆ¼m modĆ¼ller gĆ¶rĆ¼ntĆ¼lenmez</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Herhangi bir"
            " eÅleÅme bulunamadÄ±ÄÄ±ndan, en uygun sonuĆ§ gĆ¶sterildi</b>"
        ),
        "request_join": "Bampi Destek sohbetinin davet baÄlantÄ±sÄ±nÄ± istediniz",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Bu dahili"
            " b,r modĆ¼l. Bu modĆ¼lĆ¼ kaldÄ±ramaz veya deÄiÅtiremezsin</b>"
        ),
    }

    strings_hi = {
        "bad_module": "<b>š« <b>ą¤®ą„ą¤”ą„ą¤Æą„ą¤²</b> <code>{}</code> <b>ą¤Øą¤¹ą„ą¤ ą¤®ą¤æą¤²ą¤¾</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ ą¤¦ą¤øą„ą¤¤ą¤¾ą¤µą„ą¤ą¤¼ą„ą¤ą¤°ą¤£ ą¤Øą¤¹ą„ą¤",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤ą¤Ŗą¤²ą¤¬ą„ą¤§ ą¤¹ą„ą¤,"
            " {} ą¤ą¤æą¤Ŗą¤¾ ą¤¹ą„ą¤:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>ą¤ą¤æą¤Ŗą¤¾ą¤Øą„ ą¤ą„ ą¤²ą¤æą¤ ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤¦ą¤°ą„ą¤ ą¤ą¤°ą„ą¤</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤ą¤æą¤Ŗą¤¾ ą¤¹ą„ą¤,"
            " {} ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤¦ą¤æą¤ą¤¾ą¤Æą¤¾ ą¤ą¤Æą¤¾:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ ą¤¦ą¤øą„ą¤¤ą¤¾ą¤µą„ą¤ą¤¼ą„ą¤ą¤°ą¤£ ą¤Øą¤¹ą„ą¤",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>ą¤øą¤Ŗą„ą¤°ą„ą¤ ą¤ą„ą¤</a></b>",
        "_cls_doc": "ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤øą¤¹ą¤¾ą¤Æą¤¤ą¤¾ ą¤¦ą¤æą¤ą¤¾ą¤¤ą¤¾ ą¤¹ą„",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ą¤ą¤Ŗą¤Æą„ą¤ą¤ą¤°ą„ą¤¤ą¤¾ ą¤¬ą„ą¤ ą¤ą¤­ą„ ą¤­ą„"
            " ą¤Ŗą„ą¤°ą„ ą¤¤ą¤°ą¤¹ ą¤øą„ ą¤²ą„ą¤” ą¤Øą¤¹ą„ą¤ ą¤¹ą„ą¤ ą¤¹ą„, ą¤ą¤øą¤²ą¤æą¤ ą¤øą¤­ą„ ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤¦ą¤æą¤ą¤¾ą¤ ą¤Øą¤¹ą„ą¤ ą¤¦ą„ą¤¤ą„ ą¤¹ą„ą¤</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ą¤ą„ą¤ ą¤®ą„ą¤ ą¤Øą¤¹ą„ą¤ ą¤®ą¤æą¤²ą¤¾,"
            " ą¤ą¤øą¤²ą¤æą¤ ą¤øą¤¬ą¤øą„ ą¤ą¤Øą„ą¤ą„ą¤² ą¤Ŗą¤°ą¤æą¤£ą¤¾ą¤® ą¤¦ą¤æą¤ą¤¾ą¤Æą¤¾ ą¤ą¤Æą¤¾ ą¤¹ą„</b>"
        ),
        "request_join": "ą¤ą¤Ŗą¤Øą„ ą¤øą¤Ŗą„ą¤°ą„ą¤ ą¤ą„ą¤ ą¤²ą¤æą¤ą¤ ą¤ą¤¾ ą¤ą¤Øą„ą¤°ą„ą¤§ ą¤ą¤æą¤Æą¤¾ ą¤¹ą„",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ą¤Æą¤¹ ą¤ą¤ ą¤ą¤ą¤¤ą¤°ą„ą¤Øą¤æą¤¹ą¤æą¤¤"
            " ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤¹ą„, ą¤ą¤Ŗ ą¤ą¤øą„ ą¤Øą¤¹ą„ą¤ ą¤ą¤ą¤ ą¤øą¤ą¤¤ą„ ą¤Æą¤¾ ą¤¬ą¤¦ą¤² ą¤øą¤ą¤¤ą„ ą¤¹ą„ą¤</b>"
        ),
    }

    strings_uz = {
        "bad_module": "<b>š« <b>Modul</b> <code>{}</code> <b>topilmadi</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ Hujjatlanmagan",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} Umumiy modullar,"
            " yashirin {}:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>Yashirish uchun modul kiriting</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} yashirin,"
            " {} modullar ko'rsatilgan:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ Hujjatlanmagan",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>Yordam chat</a></b>",
        "_cls_doc": "Modul yordamini ko'rsatadi",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Foydalanuvchi boti"
            " hali to'liq yuklanmaganligi sababli, barcha modullar ko'rsatilmaydi</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Hech qanday moslik"
            " topilmadi, shuning uchun eng mos natija ko'rsatildi</b>"
        ),
        "request_join": "Siz yordam chat havolasini so'radingiz",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Bu bir qo'shimcha"
            " modul, uni o'chirib yoki o'zgartirib bo'lmaysiz</b>"
        ),
    }

    strings_ja = {
        "bad_module": "<b>š« <b>ć¢ćøć„ć¼ć«</b> <code>{}</code> <b>č¦ć¤ććć¾ććć§ćć</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ ćć­ć„ć”ć³ćåććć¦ćć¾ćć",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ć¢ćøć„ć¼ć«ć®ē·ę°,"
            " é ććć {}:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>é ćć¢ćøć„ć¼ć«ćå„åćć¦ćć ćć</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} é ććć,"
            " {} ć¢ćøć„ć¼ć«ćč”Øē¤ŗććć¾ćć:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ ćć­ć„ć”ć³ćåććć¦ćć¾ćć",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>ćµćć¼ććć£ćć</a></b>",
        "_cls_doc": "ć¢ćøć„ć¼ć«ć®ćć«ććč”Øē¤ŗćć¾ć",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ć¦ć¼ć¶ć¼ććććÆć¾ć å®åØć«"
            "čŖ­ćæč¾¼ć¾ćć¦ććŖćććććć¹ć¦ć®ć¢ćøć„ć¼ć«ćč”Øē¤ŗććć¾ćć</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>äøč“ćććć®ćč¦ć¤ććć¾ććć§ććć"
            "ćććć£ć¦ćęćäøč“ććēµęćč”Øē¤ŗććć¾ćć</b>"
        ),
        "request_join": "ćµćć¼ććć£ćććøć®ćŖć³ćÆććŖćÆćØć¹ććć¾ćć",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ćććÆčæ½å ć¢ćøć„ć¼ć«ć§ććć"
            "åé¤ć¾ććÆå¤ę“ć§ćć¾ćć</b>"
        ),
    }

    strings_kr = {
        "bad_module": "<b>š« <b>ėŖØė</b> <code>{}</code> <b>ģ°¾ģ ģ ģģµėė¤</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ ė¬øģķėģ§ ģģ",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ģ“ ėŖØė, ģØź²Øģ§ {}:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>ģØźø°ė ¤ė ėŖØėģ ģė „ķģ­ģģ¤</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ģØź²Øģ§,"
            " {} ėŖØėģ“ ķģėģģµėė¤:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ ė¬øģķėģ§ ģģ",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>ģ§ģ ģ±ķ</a></b>",
        "_cls_doc": "ėŖØė ėģė§ģ ķģķ©ėė¤",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ģ¬ģ©ģ ė“ģ“ ģģ§ ģģ ķ"
            "ė”ėėģ§ ģģģ¼ėÆė” ėŖØė  ėŖØėģ“ ķģėģ§ ģģµėė¤</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ģ¼ģ¹ķė ź²ģ“ ģģ¼ėÆė”"
            "ź°ģ„ ģ¼ģ¹ķė ź²°ź³¼ź° ķģė©ėė¤</b>"
        ),
        "request_join": "ģ§ģ ģ±ķ ė§ķ¬ė„¼ ģģ²­ķģµėė¤",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ģ“ź²ģ ģ¶ź° ėŖØėģ“ėÆė”"
            "ģ­ģ  ėė ė³ź²½ķ  ģ ģģµėė¤</b>"
        ),
    }

    strings_ar = {
        "bad_module": "<b>š« <b>Ų§ŁŁŁŲÆŁŁŁ</b> <code>{}</code> <b>ŲŗŁŲ± ŁŁŲ¬ŁŲÆ</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ ŁŁ ŁŲŖŁ ŲŖŁŲ«ŁŁŁ",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ŁŁŲÆŁŁŁŲ§ŲŖ,"
            " {} ŁŲ®ŁŁŲ©:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>ŁŁ ŁŲ¶ŁŁ ŁŁ ŲØŲ„ŲÆŲ®Ų§Ł Ų§ŁŁŁŲÆŁŁŁ Ų§ŁŁŲ±Ų§ŲÆ Ų„Ų®ŁŲ§Ų¦Ł</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ŁŲ®ŁŁŲ©,"
            " {} Ų§ŁŁŁŲÆŁŁŁŲ§ŲŖ Ų§ŁŁŲ¹Ų±ŁŲ¶Ų©:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ ŁŁ ŁŲŖŁ ŲŖŁŲ«ŁŁŁ",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>ŲÆŲ±ŲÆŲ“Ų© Ų§ŁŲÆŲ¹Ł</a></b>",
        "_cls_doc": "Ų¹Ų±Ų¶ ŁŲ³Ų§Ų¹ŲÆŲ© Ų§ŁŁŁŲÆŁŁŁ",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ŁŁ ŁŲŖŁ ŲŖŲ­ŁŁŁ Ų§ŁŲØŁŲŖ"
            " ŲØŲ¹ŲÆ ŲØŲ§ŁŁŲ§ŁŁ, ŁŲ°ŁŁ ŁŲ§ ŁŁŁŁ Ų¹Ų±Ų¶ Ų¬ŁŁŲ¹ Ų§ŁŁŁŲÆŁŁŁŲ§ŲŖ</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ŁŁ ŁŲŖŁ Ų§ŁŲ¹Ų«ŁŲ± Ų¹ŁŁ"
            " ŁŲŖŲ§Ų¦Ų¬ ŁŲ·Ų§ŲØŁŲ©, ŁŲ°ŁŁ ŁŲŖŁ Ų¹Ų±Ų¶ Ų§ŁŁŲŖŲ§Ų¦Ų¬ Ų§ŁŲ£ŁŲ«Ų± ŲŖŲ·Ų§ŲØŁŲ§</b>"
        ),
        "request_join": "ŲŖŁ Ų·ŁŲØ Ų±Ų§ŲØŲ· ŲÆŲ±ŲÆŲ“Ų© Ų§ŁŲÆŲ¹Ł",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>ŁŲ°Ų§ ŁŁŲÆŁŁŁ Ų„Ų¶Ų§ŁŁ ŁŲ°ŁŁ"
            " ŁŲ§ ŁŁŁŁŁŲ­Ų°ŁŁ Ų£Ł ŲŖŲ¹ŲÆŁŁŁ</b>"
        ),
    }

    strings_es = {
        "bad_module": "<b>š« <b>El mĆ³dulo</b> <code>{}</code> <b>no existe</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\nā«ļø <code>{}{}</code> {}",
        "undoc_cmd": "š¦„ Sin documentar",
        "all_header": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} mĆ³dulos,"
            " {} ocultos:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "š« <b>Por favor, introduce el mĆ³dulo que deseas ocultar</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>š</emoji> <b>{} ocultos,"
            " {} mĆ³dulos mostrados:</b>\n{}\n{}"
        ),
        "ihandler": "\nš¹ <code>{}</code> {}",
        "undoc_ihandler": "š¦„ Sin documentar",
        "support": "{} <b><a href='https://t.me/Bampi_talks'>Chat de soporte</a></b>",
        "_cls_doc": "Muestra la ayuda del mĆ³dulo",
        "partial_load": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>El bot no se ha"
            " cargado por completoaĆŗn, por lo que no se muestran todos los mĆ³dulos</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>No se encontraron"
            " resultados exactos, por lo que se muestran los resultados mĆ”s"
            " relevantes</b>"
        ),
        "request_join": "Se ha solicitado el enlace al chat de soporte",
        "core_notice": (
            "<emoji document_id=5472105307985419058>āļø</emoji> <b>Este es un mĆ³dulo"
            " adicional, por loque no se puede eliminar o modificar</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "core_emoji",
                "āŖļø",
                lambda: "Core module bullet",
                validator=loader.validators.Emoji(length=1),
            ),
            loader.ConfigValue(
                "Bampi_emoji",
                "š",
                lambda: "Bampi-only module bullet",
                validator=loader.validators.Emoji(length=1),
            ),
            loader.ConfigValue(
                "plain_emoji",
                "ā«ļø",
                lambda: "Plain module bullet",
                validator=loader.validators.Emoji(length=1),
            ),
            loader.ConfigValue(
                "empty_emoji",
                "š",
                lambda: "Empty modules bullet",
                validator=loader.validators.Emoji(length=1),
            ),
        )

    @loader.command(
        ru_doc=(
            "<Š¼Š¾Š“ŃŠ»Ń ŠøŠ»Šø Š¼Š¾Š“ŃŠ»Šø> - Š”ŠæŃŃŃŠ°ŃŃ Š¼Š¾Š“ŃŠ»Ń(-Šø) ŠøŠ· ŠæŠ¾Š¼Š¾ŃŠø\n*Š Š°Š·Š“ŠµŠ»ŃŠ¹ Š¼Š¾Š“ŃŠ»Šø"
            " ŠæŃŠ¾Š±ŠµŠ»Š°Š¼Šø"
        ),
        de_doc=(
            "<Modul oder Module> - Verstecke Modul(-e) aus der Hilfe\n*Modulnamen"
            " mit Leerzeichen trennen"
        ),
        tr_doc=(
            "<modĆ¼l veya modĆ¼ller> - YardÄ±mdan modĆ¼l(-ler) gizle\n*ModĆ¼lleri boÅluk"
            " ile ayÄ±r"
        ),
        uz_doc=(
            "<modul yoki modullar> - Modul(-lar) yordamidan yashirish\n*Modullarni"
            " bo'sh joy bilan ajratish"
        ),
        hi_doc=(
            "<ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤Æą¤¾ ą¤®ą„ą¤”ą„ą¤Æą„ą¤²ą„ą¤ø> - ą¤®ą„ą¤”ą„ą¤Æą„ą¤²(-ą¤ø) ą¤ą„ ą¤ą¤æą¤Ŗą¤¾ą¤ą¤\n*ą¤®ą„ą¤”ą„ą¤Æą„ą¤² ą¤ą„ ą¤ą¤²ą¤ ą¤ą¤°ą¤Øą„ ą¤ą„"
            " ą¤²ą¤æą¤ ą¤°ą¤æą¤ą„ą¤¤ ą¤øą„ą¤„ą¤¾ą¤Ø ą¤¬ą¤Øą¤¾ą¤ą¤"
        ),
        ja_doc="<ć¢ćøć„ć¼ć«ć¾ććÆć¢ćøć„ć¼ć«> - ćć«ćććć¢ćøć„ć¼ć«ćé ćć¾ć\n*ć¢ćøć„ć¼ć«ćć¹ćć¼ć¹ć§åŗåć£ć¦ćć ćć",
        kr_doc="<ėŖØė ėė ėŖØė> - ėģė§ģģ ėŖØėģ ģØź¹ėė¤\n*ėŖØėģ ź³µė°±ģ¼ė” źµ¬ė¶ķģ­ģģ¤",
        ar_doc="<Ų§ŁŁŲ­ŲÆŲ© Ų£Ł Ų§ŁŁŲ­ŲÆŲ§ŲŖ> - Ų„Ų®ŁŲ§Ų” ŁŲ­ŲÆŲ©(-Ų§ŲŖ) ŁŁ Ų§ŁŁŲ³Ų§Ų¹ŲÆŲ©\n*ŁŲµŁ Ų§ŁŁŲ­ŲÆŲ§ŲŖ ŲØŁŲ±Ų§Ųŗ",
        es_doc=(
            "<mĆ³dulo o mĆ³dulos> - Oculta el mĆ³dulo (-s) de la ayuda\n*Separa los"
            " mĆ³dulos con espacios"
        ),
    )
    async def helphide(self, message: Message):
        """<module or modules> - Hide module(-s) from help
        *Split modules by spaces"""
        modules = utils.get_args(message)
        if not modules:
            await utils.answer(message, self.strings("no_mod"))
            return

        mods = [i.__class__.__name__ for i in self.allmodules.modules]

        modules = list(filter(lambda module: module in mods, modules))
        currently_hidden = self.get("hide", [])
        hidden, shown = [], []
        for module in modules:
            if module in currently_hidden:
                currently_hidden.remove(module)
                shown += [module]
            else:
                currently_hidden += [module]
                hidden += [module]

        self.set("hide", currently_hidden)

        await utils.answer(
            message,
            self.strings("hidden_shown").format(
                len(hidden),
                len(shown),
                "\n".join([f"šāšØ <i>{m}</i>" for m in hidden]),
                "\n".join([f"š <i>{m}</i>" for m in shown]),
            ),
        )

    async def modhelp(self, message: Message, args: str):
        exact = True
        module = self.lookup(args)

        if not module:
            _args = args.lower()
            _args = _args[1:] if _args.startswith(self.get_prefix()) else _args
            if _args in self.allmodules.commands:
                module = self.allmodules.commands[_args].__self__

        if not module:
            module = self.lookup(
                next(
                    (
                        reversed(
                            sorted(
                                [
                                    module.strings["name"]
                                    for module in self.allmodules.modules
                                ],
                                key=lambda x: difflib.SequenceMatcher(
                                    None,
                                    args.lower(),
                                    x,
                                ).ratio(),
                            )
                        )
                    ),
                    None,
                )
            )

            exact = False

        try:
            name = module.strings("name")
        except KeyError:
            name = getattr(module, "name", "ERROR")

        _name = (
            "{} (v{}.{}.{})".format(
                utils.escape_html(name),
                module.__version__[0],
                module.__version__[1],
                module.__version__[2],
            )
            if hasattr(module, "__version__")
            else utils.escape_html(name)
        )

        reply = self.strings("single_mod_header").format(_name)
        if module.__doc__:
            reply += "<i>\nā¹ļø " + utils.escape_html(inspect.getdoc(module)) + "\n</i>"

        commands = {
            name: func
            for name, func in module.commands.items()
            if await self.allmodules.check_security(message, func)
        }

        if hasattr(module, "inline_handlers"):
            for name, fun in module.inline_handlers.items():
                reply += self.strings("ihandler").format(
                    f"@{self.inline.bot_username} {name}",
                    (
                        utils.escape_html(inspect.getdoc(fun))
                        if fun.__doc__
                        else self.strings("undoc_ihandler")
                    ),
                )

        for name, fun in commands.items():
            reply += self.strings("single_cmd").format(
                self.get_prefix(),
                name,
                (
                    utils.escape_html(inspect.getdoc(fun))
                    if fun.__doc__
                    else self.strings("undoc_cmd")
                ),
            )

        await utils.answer(
            message,
            reply
            + (f"\n\n{self.strings('not_exact')}" if not exact else "")
            + (
                f"\n\n{self.strings('core_notice')}"
                if module.__origin__.startswith("<core")
                else ""
            ),
        )

    @loader.unrestricted
    @loader.command(
        ru_doc="[Š¼Š¾Š“ŃŠ»Ń] [-f] - ŠŠ¾ŠŗŠ°Š·Š°ŃŃ ŠæŠ¾Š¼Š¾ŃŃ",
        de_doc="[Modul] [-f] - Hilfe anzeigen",
        tr_doc="[modĆ¼l] [-f] - YardÄ±mÄ± gĆ¶ster",
        uz_doc="[modul] [-f] - Yordamni ko'rsatish",
        hi_doc="[ą¤®ą„ą¤”ą„ą¤Æą„ą¤²] [-f] - ą¤®ą¤¦ą¤¦ ą¤¦ą¤æą¤ą¤¾ą¤ą¤",
        ja_doc="[ć¢ćøć„ć¼ć«] [-f] - ćć«ććč”Øē¤ŗćć¾ć",
        kr_doc="[ėŖØė] [-f] - ėģė§ ķģ",
        ar_doc="[Ų§ŁŁŲ­ŲÆŲ©] [-f] - Ų„ŲøŁŲ§Ų± Ų§ŁŁŲ³Ų§Ų¹ŲÆŲ©",
        es_doc="[mĆ³dulo] [-f] - Mostrar ayuda",
    )
    async def help(self, message: Message):
        """[module] [-f] - Show help"""
        args = utils.get_args_raw(message)
        force = False
        if "-f" in args:
            args = args.replace(" -f", "").replace("-f", "")
            force = True

        if args:
            await self.modhelp(message, args)
            return

        count = 0
        for i in self.allmodules.modules:
            try:
                if i.commands or i.inline_handlers:
                    count += 1
            except Exception:
                pass

        hidden = self.get("hide", [])

        reply = self.strings("all_header").format(
            count,
            0
            if force
            else len(
                [
                    module
                    for module in self.allmodules.modules
                    if module.__class__.__name__ in hidden
                ]
            ),
        )
        shown_warn = False

        plain_ = []
        core_ = []
        inline_ = []
        no_commands_ = []

        for mod in self.allmodules.modules:
            if not hasattr(mod, "commands"):
                logger.debug("Module %s is not inited yet", mod.__class__.__name__)
                continue

            if mod.__class__.__name__ in self.get("hide", []) and not force:
                continue

            tmp = ""

            try:
                name = mod.strings["name"]
            except KeyError:
                name = getattr(mod, "name", "ERROR")

            inline = (
                hasattr(mod, "callback_handlers")
                and mod.callback_handlers
                or hasattr(mod, "inline_handlers")
                and mod.inline_handlers
            )

            if not inline:
                for cmd_ in mod.commands.values():
                    try:
                        inline = "await self.inline.form(" in inspect.getsource(
                            cmd_.__code__
                        )
                    except Exception:
                        pass

            core = mod.__origin__.startswith("<core")

            if core:
                emoji = self.config["core_emoji"]
            elif inline:
                emoji = self.config["Bampi_emoji"]
            else:
                emoji = self.config["plain_emoji"]

            if (
                not getattr(mod, "commands", None)
                and not getattr(mod, "inline_handlers", None)
                and not getattr(mod, "callback_handlers", None)
            ):
                no_commands_ += [
                    self.strings("mod_tmpl").format(self.config["empty_emoji"], name)
                ]
                continue

            tmp += self.strings("mod_tmpl").format(emoji, name)
            first = True

            commands = [
                name
                for name, func in mod.commands.items()
                if await self.allmodules.check_security(message, func) or force
            ]

            for cmd in commands:
                if first:
                    tmp += self.strings("first_cmd_tmpl").format(cmd)
                    first = False
                else:
                    tmp += self.strings("cmd_tmpl").format(cmd)

            icommands = [
                name
                for name, func in mod.inline_handlers.items()
                if await self.inline.check_inline_security(
                    func=func,
                    user=message.sender_id,
                )
                or force
            ]

            for cmd in icommands:
                if first:
                    tmp += self.strings("first_cmd_tmpl").format(f"š¹ {cmd}")
                    first = False
                else:
                    tmp += self.strings("cmd_tmpl").format(f"š¹ {cmd}")

            if commands or icommands:
                tmp += " )"
                if core:
                    core_ += [tmp]
                elif inline:
                    inline_ += [tmp]
                else:
                    plain_ += [tmp]
            elif not shown_warn and (mod.commands or mod.inline_handlers):
                reply = (
                    "<i>You have permissions to execute only these"
                    f" commands</i>\n{reply}"
                )
                shown_warn = True

        plain_.sort(key=lambda x: x.split()[1])
        core_.sort(key=lambda x: x.split()[1])
        inline_.sort(key=lambda x: x.split()[1])
        no_commands_.sort(key=lambda x: x.split()[1])
        no_commands_ = "".join(no_commands_) if force else ""

        partial_load = (
            ""
            if self.lookup("Loader")._fully_loaded
            else f"\n\n{self.strings('partial_load')}"
        )

        await utils.answer(
            message,
            "{}\n{}{}{}{}{}".format(
                reply,
                "".join(core_),
                "".join(plain_),
                "".join(inline_),
                no_commands_,
                partial_load,
            ),
        )

    @loader.command(
        ru_doc="ŠŠ¾ŠŗŠ°Š·Š°ŃŃ ŃŃŃŠ»ŠŗŃ Š½Š° ŃŠ°Ń ŠæŠ¾Š¼Š¾ŃŠø Bampi",
        de_doc="Zeige den Link zum Bampi-Hilfe-Chat",
        tr_doc="Bampi yardÄ±m sohbetinin baÄlantÄ±sÄ±nÄ± gĆ¶ster",
        uz_doc="Bampi yordam sohbatining havolasini ko'rsatish",
        hi_doc="ą¤¹ą¤æą¤ą„ą¤ą¤¾ ą¤øą¤¹ą¤¾ą¤Æą¤¤ą¤¾ ą¤ą„ą¤ ą¤ą¤¾ ą¤²ą¤æą¤ą¤ ą¤¦ą¤æą¤ą¤¾ą¤ą¤",
        ja_doc="ććć«ć®ćć«ććć£ćććøć®ćŖć³ćÆćč”Øē¤ŗćć¾ć",
        kr_doc="ķģ¹“ ėģė§ ģ±ķ ė§ķ¬ė„¼ ķģķ©ėė¤",
        ar_doc="Ų„ŲøŁŲ§Ų± Ų±Ų§ŲØŲ· ŲÆŲ±ŲÆŲ“Ų© ŁŲ³Ų§Ų¹ŲÆŲ© ŁŁŁŲ§",
        es_doc="Mostrar enlace al chat de ayuda de Bampi",
    )
    async def support(self, message):
        """Get link of Bampi support chat"""
        if message.out:
            await self.request_join("@Bampi_talks", self.strings("request_join"))

        await utils.answer(
            message,
            self.strings("support").format(
                (
                    utils.get_platform_emoji(self._client)
                    if self._client.Bampi_me.premium and CUSTOM_EMOJIS
                    else "š"
                )
            ),
        )
