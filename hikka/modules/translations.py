from .. import loader, utils, translations
from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


@loader.tds
class Translations(loader.Module):
    """Processes internal translations"""

    strings = {
        "name": "Translations",
        "lang_saved": "{} <b>Language saved!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Translate pack"
            " saved!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Incorrect language"
            " specified</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Translations reset"
            " to default ones</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Invalid pack format"
            " in url</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>You need to specify"
            " valid url containing a langpack</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>Command output seems"
            " to be too long, so it's sent in file.</b>"
        ),
        "opening_form": " <b>Opening form...</b>",
        "opening_gallery": " <b>Opening gallery...</b>",
        "opening_list": " <b>Opening list...</b>",
        "inline403": "đĢ <b>You can't send inline units in this chat</b>",
        "invoke_failed": "<b>đĢ Unit invoke failed! More info in logs</b>",
        "show_inline_cmds": "đ Show all available inline commands",
        "no_inline_cmds": "You have no available commands",
        "no_inline_cmds_msg": (
            "<b>đ There are no available inline commands or you lack access to them</b>"
        ),
        "inline_cmds": "âšī¸ You have {} available command(-s)",
        "inline_cmds_msg": "<b>âšī¸ Available inline commands:</b>\n\n{}",
        "run_command": "đī¸ Run command",
        "command_msg": "<b>đ Command ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ Command ÂĢ{}Âģ",
        "button403": "You are not allowed to press this button!",
        "keep_id": "â ī¸ Do not remove ID! {}",
    }

    strings_ru = {
        "lang_saved": "{} <b>Đ¯ĐˇŅĐē ŅĐžŅŅĐ°ĐŊŅĐŊ!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ĐĐ°ĐēĐĩŅ ĐŋĐĩŅĐĩĐ˛ĐžĐ´ĐžĐ˛"
            " ŅĐžŅŅĐ°ĐŊŅĐŊ!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ĐŖĐēĐ°ĐˇĐ°ĐŊ ĐŊĐĩĐ˛ĐĩŅĐŊŅĐš"
            " ŅĐˇŅĐē</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ĐĐĩŅĐĩĐ˛ĐžĐ´Ņ ŅĐąŅĐžŅĐĩĐŊŅ"
            " ĐŊĐ° ŅŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅĐĩ</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ĐĐĩĐ˛ĐĩŅĐŊŅĐš ŅĐžŅĐŧĐ°Ņ"
            " ĐŋĐ°ĐēĐĩŅĐ° ĐŋĐĩŅĐĩĐ˛ĐžĐ´ĐžĐ˛ Đ˛ ŅŅŅĐģĐēĐĩ</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ĐŅ Đ´ĐžĐģĐļĐŊŅ ŅĐēĐ°ĐˇĐ°ŅŅ"
            " ŅŅŅĐģĐēŅ, ŅĐžĐ´ĐĩŅĐļĐ°ŅŅŅ ĐŋĐ°ĐēĐĩŅ ĐŋĐĩŅĐĩĐ˛ĐžĐ´ĐžĐ˛</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>ĐŅĐ˛ĐžĐ´ ĐēĐžĐŧĐ°ĐŊĐ´Ņ ŅĐģĐ¸ŅĐēĐžĐŧ"
            " Đ´ĐģĐ¸ĐŊĐŊŅĐš, ĐŋĐžŅŅĐžĐŧŅ ĐžĐŊ ĐžŅĐŋŅĐ°Đ˛ĐģĐĩĐŊ Đ˛ ŅĐ°ĐšĐģĐĩ.</b>"
        ),
        "opening_form": " <b>ĐŅĐēŅŅĐ˛Đ°Ņ ŅĐžŅĐŧŅ...</b>",
        "opening_gallery": " <b>ĐŅĐēŅŅĐ˛Đ°Ņ ĐŗĐ°ĐģĐĩŅĐĩŅ...</b>",
        "opening_list": " <b>ĐŅĐēŅŅĐ˛Đ°Ņ ŅĐŋĐ¸ŅĐžĐē...</b>",
        "inline403": "đĢ <b>ĐŅ ĐŊĐĩ ĐŧĐžĐļĐĩŅĐĩ ĐžŅĐŋŅĐ°Đ˛ĐģŅŅŅ Đ˛ŅŅŅĐžĐĩĐŊĐŊŅĐĩ ŅĐģĐĩĐŧĐĩĐŊŅŅ Đ˛ ŅŅĐžĐŧ ŅĐ°ŅĐĩ</b>",
        "invoke_failed": "<b>đĢ ĐŅĐˇĐžĐ˛ ĐŧĐžĐ´ŅĐģŅ ĐŊĐĩ ŅĐ´Đ°ĐģŅŅ! ĐĐžĐ´ŅĐžĐąĐŊĐĩĐĩ Đ˛ ĐģĐžĐŗĐ°Ņ</b>",
        "show_inline_cmds": "đ ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ˛ŅĐĩ Đ´ĐžŅŅŅĐŋĐŊŅĐĩ Đ˛ŅŅŅĐžĐĩĐŊĐŊŅĐĩ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        "no_inline_cmds": "ĐŖ Đ˛Đ°Ņ ĐŊĐĩŅ Đ´ĐžŅŅŅĐŋĐŊŅŅ inline ĐēĐžĐŧĐ°ĐŊĐ´",
        "no_inline_cmds_msg": (
            "<b>đ ĐĐĩŅ Đ´ĐžŅŅŅĐŋĐŊŅŅ inline ĐēĐžĐŧĐ°ĐŊĐ´ Đ¸ĐģĐ¸ Ņ Đ˛Đ°Ņ ĐŊĐĩŅ Đ´ĐžŅŅŅĐŋĐ° Đē ĐŊĐ¸Đŧ</b>"
        ),
        "inline_cmds": "âšī¸ ĐŖ Đ˛Đ°Ņ {} Đ´ĐžŅŅŅĐŋĐŊĐ°Ņ(-ŅŅ) ĐēĐžĐŧĐ°ĐŊĐ´Đ°(-Ņ)",
        "inline_cmds_msg": "<b>âšī¸ ĐĐžŅŅŅĐŋĐŊŅĐĩ inline ĐēĐžĐŧĐ°ĐŊĐ´Ņ:</b>\n\n{}",
        "run_command": "đī¸ ĐŅĐŋĐžĐģĐŊĐ¸ŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        "command_msg": "<b>đ ĐĐžĐŧĐ°ĐŊĐ´Đ° ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ ĐĐžĐŧĐ°ĐŊĐ´Đ° ÂĢ{}Âģ",
        "button403": "ĐŅ ĐŊĐĩ ĐŧĐžĐļĐĩŅĐĩ ĐŊĐ°ĐļĐ°ŅŅ ĐŊĐ° ŅŅŅ ĐēĐŊĐžĐŋĐēŅ!",
        "keep_id": "â ī¸ ĐĐĩ ŅĐ´Đ°ĐģŅĐšŅĐĩ ID! {}",
    }

    strings_ua = {
        "lang_saved": "{} <b>ĐĐžĐ˛Đ° ĐˇĐąĐĩŅĐĩĐļĐĩĐŊĐ°!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ĐĐ°ĐēĐĩŅ ĐŋĐĩŅĐĩĐēĐģĐ°Đ´ŅĐ˛"
            " ĐˇĐąĐĩŅĐĩĐļĐĩĐŊ!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ĐĐēĐ°ĐˇĐ°ĐŊĐž ĐŊĐĩĐ˛ŅŅĐŊŅ"
            " ĐŧĐžĐ˛Ņ</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ĐĐĩŅĐĩĐēĐģĐ°Đ´Đ¸ ŅĐēĐ¸ĐŊŅŅĐž"
            " ĐŊĐ° ŅŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅ</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ĐĐĩĐ˛ŅŅĐŊĐ¸Đš ŅĐžŅĐŧĐ°Ņ"
            " ĐŋĐ°ĐēĐĩŅŅ ĐŋĐĩŅĐĩĐēĐģĐ°Đ´ŅĐ˛ ĐŊĐ° ĐˇĐ°ŅĐģĐ°ĐŊĐŊŅ</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ĐĐ¸ ĐŋĐžĐ˛Đ¸ĐŊĐŊŅ Đ˛ĐēĐ°ĐˇĐ°ŅĐ¸"
            " ĐŋĐžŅĐ¸ĐģĐ°ĐŊĐŊŅ, ŅĐž ĐŧŅŅŅĐ¸ŅŅ ĐŋĐ°ĐēĐĩŅ ĐŋĐĩŅĐĩĐēĐģĐ°Đ´ŅĐ˛</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>ĐĐ¸Đ˛ĐĩĐ´ĐĩĐŊĐŊŅ ĐēĐžĐŧĐ°ĐŊĐ´Đ¸ ĐˇĐ°ĐŊĐ°Đ´ŅĐž"
            " Đ´ĐžĐ˛ĐŗĐ¸Đš, ŅĐžĐŧŅ Đ˛ŅĐŊ Đ˛ŅĐ´ĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đš Ņ ŅĐ°ĐšĐģŅ.</b>"
        ),
        "opening_form": " <b>ĐŅĐ´ĐēŅĐ¸Đ˛Đ°Ņ ŅĐžŅĐŧŅ...</b>",
        "opening_gallery": " <b>ĐŅĐ´ĐēŅĐ¸Đ˛Đ°Ņ ĐŗĐ°ĐģĐĩŅĐĩŅ...</b>",
        "opening_list": " <b>ĐŅĐ´ĐēŅĐ¸Đ˛Đ°Ņ ŅĐŋĐ¸ŅĐžĐē...</b>",
        "inline403": "đĢ <b>ĐĐ¸ ĐŊĐĩ ĐŧĐžĐļĐĩŅĐĩ ĐŊĐ°Đ´ŅĐ¸ĐģĐ°ŅĐ¸ Đ˛ĐąŅĐ´ĐžĐ˛Đ°ĐŊŅ ĐĩĐģĐĩĐŧĐĩĐŊŅĐ¸ Đ˛ ŅŅĐžĐŧŅ ŅĐ°ŅŅ</b>",
        "invoke_failed": "<b>đĢ ĐĐ¸ĐēĐģĐ¸Đē ĐŧĐžĐ´ŅĐģŅ ĐŊĐĩ Đ˛Đ´Đ°Đ˛ŅŅ! ĐĐĩŅĐ°ĐģŅĐŊŅŅĐĩ Ņ ĐģĐžĐŗĐ°Ņ</b>",
        "show_inline_cmds": "đ ĐĐžĐēĐ°ĐˇĐ°ŅĐ¸ Đ˛ŅŅ Đ´ĐžŅŅŅĐŋĐŊŅ Đ˛ĐąŅĐ´ĐžĐ˛Đ°ĐŊŅ ĐēĐžĐŧĐ°ĐŊĐ´Đ¸",
        "no_inline_cmds": "ĐŖ Đ˛Đ°Ņ ĐŊĐĩĐŧĐ°Ņ Đ´ĐžŅŅŅĐŋĐŊĐ¸Ņ inline ĐēĐžĐŧĐ°ĐŊĐ´",
        "no_inline_cmds_msg": (
            "<b>đ ĐŠĐžĐą Đ˛Đ¸ĐēĐžŅĐ¸ŅŅĐ°ŅĐ¸ ĐēĐžĐŧĐ°ĐŊĐ´Đ¸ Đ˛Đ°Đŧ ĐŋĐžŅŅŅĐąĐŊĐž ĐˇŅĐžĐąĐ¸ŅĐ¸ Bampi"
        ),
        "inline_cmds": "âšī¸ ĐŖ Đ˛Đ°Ņ {} Đ´ĐžŅŅŅĐŋĐŊĐ°(-Đ¸Ņ) ĐēĐžĐŧĐ°ĐŊĐ´Đ°(-Đ¸)",
        "inline_cmds_msg": "<b>âšī¸ ĐĐžŅŅŅĐŋĐŊŅ inline ĐēĐžĐŧĐ°ĐŊĐ´Đ¸:</b>\n\n{}",
        "run_command": "đī¸ ĐĐ¸ĐēĐžĐŊĐ°ŅĐ¸ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        "command_msg": "<b>đ ĐĐžĐŧĐ°ĐŊĐ´Đ° ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ ĐĐžĐŧĐ°ĐŊĐ´Đ° ÂĢ{}Âģ",
        "button403": "ĐĐ¸ ĐŊĐĩ ĐŧĐžĐļĐĩŅĐĩ ĐŊĐ°ŅĐ¸ŅĐŊŅŅĐ¸ ĐŊĐ° ŅŅ ĐēĐŊĐžĐŋĐēŅ!",
        "keep_id": "â ī¸ ĐĐĩ Đ˛Đ¸Đ´Đ°ĐģŅĐšŅĐĩ ID! {}",
    }

    strings_de = {
        "lang_saved": "{} <b>Sprache gespeichert!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Ãbersetzungs"
            " Paket gespeichert!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Falsche Sprache"
            " angegeben</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Ãbersetzungen"
            " auf Standard zurÃŧckgesetzt</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>UngÃŧltiges"
            " Ãbersetzungs Paket in der URL</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Sie mÃŧssen eine"
            " gÃŧltige URL angeben, die ein Ãbersetzungs Paket enthÃ¤lt</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>Befehlsausgabe scheint"
            " zu lang zu sein, daher wird sie in einer Datei gesendet.</b>"
        ),
        "opening_form": " <b>Formular wird geÃļffnet...</b>",
        "opening_gallery": " <b>Galerie wird geÃļffnet...</b>",
        "opening_list": " <b>Liste wird geÃļffnet...</b>",
        "inline403": "đĢ <b>Sie kÃļnnen Inline-Einheiten in diesem Chat nicht senden</b>",
        "invoke_failed": (
            "<b>đĢ Modulaufruf fehlgeschlagen! Weitere Informationen in den"
            " Protokollen</b>"
        ),
        "show_inline_cmds": "đ Zeige alle verfÃŧgbaren Inline-Befehle",
        "no_inline_cmds": "Sie haben keine verfÃŧgbaren Inline-Befehle",
        "no_inline_cmds_msg": (
            "<b>đ Keine verfÃŧgbaren Inline-Befehle oder Sie haben keinen Zugriff"
            " auf sie</b>"
        ),
        "inline_cmds": "âšī¸ Sie haben {} verfÃŧgbare(n) Befehl(e)",
        "inline_cmds_msg": "<b>âšī¸ VerfÃŧgbare Inline-Befehle:</b>\n\n{}",
        "run_command": "đī¸ Befehl ausfÃŧhren",
        "command_msg": "<b>đ Befehl ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ Befehl ÂĢ{}Âģ",
        "button403": "Sie kÃļnnen auf diese SchaltflÃ¤che nicht klicken!",
        "keep_id": "â ī¸ LÃļschen sie das ID nicht! {}",
    }

    strings_tr = {
        "lang_saved": "{} <b>Dil kaydedildi!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Ãeviri paketi"
            " kaydedildi!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>YanlÄąÅ dil"
            " belirtildi</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Ãeviriler varsayÄąlan"
            " hale getirildi</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>URL'deki Ã§eviri"
            " paketi geÃ§ersiz</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>GeÃ§erli bir URL"
            " belirtmelisiniz</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>Komut Ã§ÄąktÄąsÄą Ã§ok uzun"
            " gÃļrÃŧnÃŧyor, bu yÃŧzden dosya olarak gÃļnderildi.</b>"
        ),
        "opening_form": " <b>Form aÃ§ÄąlÄąyor...</b>",
        "opening_gallery": " <b>Galeri aÃ§ÄąlÄąyor...</b>",
        "opening_list": " <b>Liste aÃ§ÄąlÄąyor...</b>",
        "inline403": "đĢ <b>Bu sohbete satÄąr iÃ§i birimler gÃļnderemezsin</b>",
        "invoke_failed": (
            "<b>đĢ ModÃŧl Ã§aÄrÄąsÄą baÅarÄąsÄąz! KayÄątlardan daha fazla bilgiye"
            " eriÅebilirsin</b>"
        ),
        "show_inline_cmds": "đ TÃŧm kullanÄąlabilir inline komutlarÄąnÄą gÃļster",
        "no_inline_cmds": "KullanÄąlabilir inline komutunuz yok",
        "no_inline_cmds_msg": (
            "<b>đ KullanÄąlabilir inline komutunuz yok veya eriÅiminiz yok</b>"
        ),
        "inline_cmds": "âšī¸ {} kullanÄąlabilir komutunuz var",
        "inline_cmds_msg": "<b>âšī¸ KullanÄąlabilir inline komutlar:</b>\n\n{}",
        "run_command": "đī¸ Komutu Ã§alÄąÅtÄąr",
        "command_msg": "<b>đ Komut ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ Komut ÂĢ{}Âģ",
        "button403": "Bu dÃŧÄmeye basamazsÄąnÄąz!",
        "keep_id": "â ī¸ ID'yi silmeyin! {}",
    }

    strings_uz = {
        "lang_saved": "{} <b>Til saqlandi!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Tarjima paketi"
            " saqlandi!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Noto'g'ri til"
            " belgilandi</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Tarjimalar"
            " standart holatga qaytarildi</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>URL'dagi tarjima"
            " paketi noto'g'ri</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Siz noto'g'ri URL"
            " belirtdingiz</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>Bajarilgan buyruq"
            " natijasi juda uzun, shuning uchun fayl sifatida yuborildi.</b>"
        ),
        "opening_form": " <b>Formani ochish...</b>",
        "opening_gallery": " <b>Galeriyani ochish...</b>",
        "opening_list": " <b>Ro'yxatni ochish...</b>",
        "inline403": (
            "đĢ <b>Siz bu guruhda inline obyektlarni yuborishingiz mumkin emas</b>"
        ),
        "invoke_failed": (
            "<b>đĢ Modulni chaqirish muvaffaqiyatsiz! Batafsil ma'lumotlar"
            " jurnallarda</b>"
        ),
        "show_inline_cmds": "đ Barcha mavjud inline buyruqlarini ko'rsatish",
        "no_inline_cmds": "Sizda mavjud inline buyruqlar yo'q",
        "no_inline_cmds_msg": (
            "<b>đ Sizda mavjud inline buyruqlar yo'q yoki ularga kirish huquqingiz"
            " yo'q</b>"
        ),
        "inline_cmds": "âšī¸ Sizda {} mavjud buyruq bor",
        "inline_cmds_msg": "<b>âšī¸ Mavjud inline buyruqlar:</b>\n\n{}",
        "run_command": "đī¸ Buyruqni bajarish",
        "command_msg": "<b>đ Buyruq ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ Buyruq ÂĢ{}Âģ",
        "button403": "Siz ushbu tugmani bosib bo'lmaysiz!",
        "keep_id": "â ī¸ ID-ni o'chirmang! {}",
    }

    strings_hi = {
        "lang_saved": "{} <b>ā¤­ā¤žā¤ˇā¤ž ā¤¸ā¤šāĨā¤ā¤ž ā¤ā¤¯ā¤ž!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ā¤ā¤¨āĨā¤ĩā¤žā¤Ļ ā¤ĒāĨā¤"
            " ā¤¸ā¤šāĨā¤ā¤ž ā¤ā¤¯ā¤ž!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ā¤ā¤˛ā¤¤ ā¤­ā¤žā¤ˇā¤ž"
            " ā¤¨ā¤ŋā¤°āĨā¤Ļā¤ŋā¤ˇāĨā¤ ā¤ā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤ž</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ā¤ā¤¨āĨā¤ĩā¤žā¤Ļ ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤"
            " ā¤Ēā¤° ā¤°āĨā¤¸āĨā¤ ā¤ā¤ŋā¤ ā¤ā¤</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ā¤¯āĨā¤ā¤°ā¤ā¤˛ ā¤ŽāĨā¤ ā¤ā¤˛ā¤¤"
            " ā¤ā¤¨āĨā¤ĩā¤žā¤Ļ ā¤ĒāĨā¤ ā¤¨ā¤ŋā¤°āĨā¤Ļā¤ŋā¤ˇāĨā¤ ā¤ā¤ŋā¤¯ā¤ž ā¤ā¤¯ā¤ž</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ā¤ā¤Ēā¤¨āĨ ā¤ā¤˛ā¤¤ ā¤¯āĨā¤ā¤°ā¤ā¤˛"
            " ā¤¨ā¤ŋā¤°āĨā¤Ļā¤ŋā¤ˇāĨā¤ ā¤ā¤ŋā¤¯ā¤ž ā¤šāĨ</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>ā¤ā¤Žā¤žā¤ā¤Ą ā¤ā¤ā¤ā¤ĒāĨā¤ ā¤Ŧā¤šāĨā¤¤ ā¤˛ā¤ā¤Ŧā¤ž"
            " ā¤˛ā¤ā¤¤ā¤ž ā¤šāĨ, ā¤ā¤¸ā¤˛ā¤ŋā¤ ā¤Ģā¤ŧā¤žā¤ā¤˛ ā¤ŽāĨā¤ ā¤­āĨā¤ā¤ž ā¤ā¤žā¤¤ā¤ž ā¤šāĨ.</b>"
        ),
        "opening_form": " <b>ā¤ĢāĨā¤°āĨā¤Ž ā¤āĨā¤˛ ā¤°ā¤šā¤ž ā¤šāĨ...</b>",
        "opening_gallery": " <b>ā¤āĨā¤˛ā¤°āĨ ā¤āĨā¤˛ ā¤°ā¤šā¤ž ā¤šāĨ...</b>",
        "opening_list": " <b>ā¤¸āĨā¤āĨ ā¤āĨā¤˛ ā¤°ā¤šā¤ž ā¤šāĨ...</b>",
        "inline403": "đĢ <b>ā¤ā¤Ē ā¤ā¤¸ ā¤āĨā¤°āĨā¤Ē ā¤ŽāĨā¤ ā¤ā¤¨ā¤˛ā¤žā¤ā¤¨ ā¤ā¤ā¤ā¤Ž ā¤¨ā¤šāĨā¤ ā¤­āĨā¤ ā¤¸ā¤ā¤¤āĨ ā¤šāĨā¤</b>",
        "invoke_failed": "<b>đĢ ā¤ŽāĨā¤ĄāĨā¤¯āĨā¤˛ ā¤ā¤¨āĨā¤ĩāĨā¤ ā¤ĩā¤ŋā¤Ģā¤˛! ā¤ĩā¤ŋā¤¸āĨā¤¤āĨā¤¤ ā¤ā¤žā¤¨ā¤ā¤žā¤°āĨ ā¤˛āĨā¤ ā¤ŽāĨā¤ ā¤šāĨ</b>",
        "show_inline_cmds": "đ ā¤¸ā¤­āĨ ā¤ā¤Ēā¤˛ā¤ŦāĨā¤§ ā¤ā¤¨ā¤˛ā¤žā¤ā¤¨ ā¤ā¤Žā¤žā¤ā¤Ą ā¤Ļā¤ŋā¤ā¤žā¤ā¤",
        "no_inline_cmds": "ā¤ā¤Ēā¤āĨ ā¤Ēā¤žā¤¸ ā¤āĨā¤ ā¤ā¤Ēā¤˛ā¤ŦāĨā¤§ ā¤ā¤¨ā¤˛ā¤žā¤ā¤¨ ā¤ā¤Žā¤žā¤ā¤Ą ā¤¨ā¤šāĨā¤ ā¤šāĨā¤",
        "no_inline_cmds_msg": (
            "<b>đ ā¤ā¤Ēā¤āĨ ā¤Ēā¤žā¤¸ ā¤āĨā¤ ā¤ā¤Ēā¤˛ā¤ŦāĨā¤§ ā¤ā¤¨ā¤˛ā¤žā¤ā¤¨ ā¤ā¤Žā¤žā¤ā¤Ą ā¤¯ā¤ž ā¤ā¤¨ā¤˛ā¤žā¤ā¤¨ ā¤ā¤Žā¤žā¤ā¤Ą ā¤āĨ ā¤˛ā¤ŋā¤ ā¤ā¤¨āĨā¤Žā¤¤ā¤ŋ ā¤¨ā¤šāĨā¤"
            " ā¤šāĨā¤</b>"
        ),
        "inline_cmds": "âšī¸ ā¤ā¤Ēā¤āĨ ā¤Ēā¤žā¤¸ {} ā¤ā¤Ēā¤˛ā¤ŦāĨā¤§ ā¤ā¤Žā¤žā¤ā¤Ą ā¤šāĨā¤",
        "inline_cmds_msg": "<b>âšī¸ ā¤ā¤Ēā¤˛ā¤ŦāĨā¤§ ā¤ā¤¨ā¤˛ā¤žā¤ā¤¨ ā¤ā¤Žā¤žā¤ā¤Ą:</b>\n\n{}",
        "run_command": "đī¸ ā¤ā¤Žā¤žā¤ā¤Ą ā¤ā¤˛ā¤žā¤ā¤",
        "command_msg": "<b>đ ā¤ā¤Žā¤žā¤ā¤Ą ÂĢ{}Âģ</b>\n\n<i>{}</i>",
        "command": "đ ā¤ā¤Žā¤žā¤ā¤Ą ÂĢ{}Âģ",
        "button403": "ā¤ā¤Ē ā¤ā¤¸ ā¤Ŧā¤ā¤¨ ā¤āĨ ā¤Ļā¤Ŧā¤ž ā¤¨ā¤šāĨā¤ ā¤¸ā¤ā¤¤āĨ!",
        "button404": "ā¤¯ā¤š ā¤Ŧā¤ā¤¨ ā¤ā¤Ŧ ā¤ā¤Ēā¤˛ā¤ŦāĨā¤§ ā¤¨ā¤šāĨā¤ ā¤šāĨ!",
    }

    strings_ja = {
        "lang_saved": "{} <b>č¨čĒãäŋå­ãããžããīŧ</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>įŋģč¨ŗããã¯ ãäŋå­ãããžããīŧ</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ä¸æ­ŖįĸēãĒč¨čĒ ãæåŽãããžãã</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>įŋģč¨ŗããããŠãĢããĢ"
            " ãĒãģãããããžãã</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>URLãŽįŋģč¨ŗããã¯ã ä¸æ­Ŗįĸēã§ã</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ä¸æ­ŖįĸēãĒURLãæåŽããžãã</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>ãŗããŗããŽåēåã"
            " éˇããããããããĄã¤ãĢã¨ããĻéäŋĄãããžãã.</b>"
        ),
        "opening_form": " <b>ããŠãŧã ãéããĻããžã...</b>",
        "opening_gallery": " <b>ãŽãŖãŠãĒãŧãéããĻããžã...</b>",
        "opening_list": " <b>ãĒãšããéããĻããžã...</b>",
        "inline403": "đĢ <b>ããĒãã¯ããŽã°ãĢãŧãã§ã¤ãŗãŠã¤ãŗãĸã¤ãã ãéäŋĄãããã¨ã¯ã§ããžãã</b>",
        "invoke_failed": "<b>đĢ ãĸã¸ãĨãŧãĢãŽåŧãŗåēããå¤ąæããžããīŧ čŠŗį´°ã¯ã­ã°ãĢč¨é˛ãããĻããžã</b>",
        "show_inline_cmds": "đ ããšãĻãŽåŠį¨å¯čŊãĒã¤ãŗãŠã¤ãŗãŗããŗããčĄ¨į¤ē",
        "no_inline_cmds": "åŠį¨å¯čŊãĒã¤ãŗãŠã¤ãŗãŗããŗãã¯ãããžãã",
        "no_inline_cmds_msg": "<b>đ åŠį¨å¯čŊãĒã¤ãŗãŠã¤ãŗãŗããŗããžãã¯ã¤ãŗãŠã¤ãŗãŗããŗãã¸ãŽãĸã¯ãģãšæ¨Šããããžãã</b>",
        "inline_cmds": "âšī¸ åŠį¨å¯čŊãĒãŗããŗãã {} ãããžã",
        "inline_cmds_msg": "<b>âšī¸ åŠį¨å¯čŊãĒã¤ãŗãŠã¤ãŗãŗããŗã:</b>\n\n{}",
        "run_command": "đī¸ ãŗããŗããåŽčĄ",
        "command_msg": "<b>đ ãŗããŗãã{}ã</b>\n\n<i>{}</i>",
        "command": "đ ãŗããŗãã{}ã",
        "button403": "ããĒãã¯ããŽããŋãŗãæŧããã¨ã¯ã§ããžããīŧ",
        "button404": "ããŽããŋãŗã¯ããåŠį¨ã§ããžããīŧ",
    }

    strings_kr = {
        "lang_saved": "{} <b>ė¸ė´ę° ė ėĨëėėĩëë¤!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ë˛ė­ íŠė´ ė ėĨëėėĩëë¤!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ėëĒģë ė¸ė´ę° ė§ė ëėėĩëë¤</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ë˛ė­ė´ ę¸°ëŗ¸ę°ėŧëĄ ėŦė¤ė ëėėĩëë¤</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>URLė ë˛ė­ íŠė´ ėëĒģëėėĩëë¤</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ėëĒģë URLė ė§ė íė¨ėĩëë¤</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>ëĒë šė ėļë Ĩė´"
            " ëëŦ´ ęšëë¤. íėŧëĄ ė ėĄëėėĩëë¤.</b>"
        ),
        "opening_form": " <b>íŧė ė´ęŗ  ėėĩëë¤...</b>",
        "opening_gallery": " <b>ę°¤ëŦëĻŦëĨŧ ė´ęŗ  ėėĩëë¤...</b>",
        "opening_list": " <b>ëĻŦė¤í¸ëĨŧ ė´ęŗ  ėėĩëë¤...</b>",
        "inline403": "đĢ <b>ė´ ęˇ¸ëŖšėė ė¸ëŧė¸ ėė´íė ëŗ´ë´ë ę˛ė íėŠëė§ ėėĩëë¤</b>",
        "invoke_failed": "<b>đĢ ëĒ¨ë í¸ėļė´ ė¤í¨íėĩëë¤! ėė¸í ë´ėŠė ëĄęˇ¸ė ę¸°ëĄëė´ ėėĩëë¤</b>",
        "show_inline_cmds": "đ ëĒ¨ë  ėŦėŠ ę°ëĨí ė¸ëŧė¸ ëĒë šė íė",
        "no_inline_cmds": "ėŦėŠ ę°ëĨí ė¸ëŧė¸ ëĒë šė´ ėėĩëë¤",
        "no_inline_cmds_msg": "<b>đ ėŦėŠ ę°ëĨí ė¸ëŧė¸ ëĒë šė´ ėęą°ë ė¸ëŧė¸ ëĒë šė ëí ėĄė¸ė¤ ęļíė´ ėėĩëë¤</b>",
        "inline_cmds": "âšī¸ ėŦėŠ ę°ëĨí ëĒë šė´ {} ę° ėėĩëë¤",
        "inline_cmds_msg": "<b>âšī¸ ėŦėŠ ę°ëĨí ė¸ëŧė¸ ëĒë š:</b>\n\n{}",
        "run_command": "đī¸ ëĒë šė ė¤í",
        "command_msg": "<b>đ ëĒë š '{}' </b>\n\n<i>{}</i>",
        "command": "đ ëĒë š '{}'",
        "button403": "ė´ ë˛íŧė ëëĨŧ ė ėėĩëë¤!",
        "button404": "ė´ ë˛íŧė ë ė´ė ėŦėŠí  ė ėėĩëë¤!",
    }

    strings_ar = {
        "lang_saved": "{} <b>ØĒŲ Ø­ŲØ¸ Ø§ŲŲØēØŠ!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ØĒŲ Ø­ŲØ¸ Ø­Ø˛ŲØŠ"
            " Ø§ŲØĒØąØŦŲØŠ!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ØĒŲ ØĒØ­Ø¯ŲØ¯ ŲØēØŠ"
            " ØēŲØą ØĩØ­ŲØ­ØŠ</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ØĒŲ ØĨØšØ§Ø¯ØŠ ØĒØšŲŲŲ"
            " Ø§ŲØĒØąØŦŲØŠ ØĨŲŲ Ø§ŲØ§ŲØĒØąØ§ØļŲ</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ØĒŲ ØĒØ­Ø¯ŲØ¯ Ø­Ø˛ŲØŠ"
            " Ø§ŲØĒØąØŦŲØŠ ØēŲØą ØĩØ­ŲØ­ØŠ</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>ØĒŲ ØĒØ­Ø¯ŲØ¯ URL"
            " ØēŲØą ØĩØ­ŲØ­</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>ØĒŲ ØĒØŦØ§ŲØ˛ Ø§ŲŲØ§ØĒØŦ"
            " ŲŲØŖŲØą. ØĒŲ ØĨØąØŗØ§ŲŲ ŲŲŲŲ.</b>"
        ),
        "opening_form": " <b>ŲØĒŲ ŲØĒØ­ Ø§ŲŲŲŲØ°ØŦ...</b>",
        "opening_gallery": " <b>ŲØĒŲ ŲØĒØ­ Ø§ŲØĩØ§ŲØŠ...</b>",
        "opening_list": " <b>ŲØĒŲ ŲØĒØ­ Ø§ŲŲØ§ØĻŲØŠ...</b>",
        "inline403": "đĢ <b>ŲØ§ ŲØŗŲØ­ Ø¨ØĨØąØŗØ§Ų ØšŲØ§ØĩØą Ø§ŲŲØ§ØŦŲØŠ Ø§ŲØŗØˇØ­ŲØŠ ŲŲ ŲØ°Ų Ø§ŲŲØŦŲŲØšØŠ</b>",
        "invoke_failed": "<b>đĢ ŲØ´Ų Ø§ØŗØĒØ¯ØšØ§ØĄ Ø§ŲŲØ­Ø¯ØŠ! Ø§ŲØ¸Øą Ø§ŲØŗØŦŲ ŲŲØ­ØĩŲŲ ØšŲŲ ØĒŲØ§ØĩŲŲ</b>",
        "show_inline_cmds": "đ ØšØąØļ ØŦŲŲØš Ø§ŲØŖŲØ§ŲØą Ø§ŲŲØĒØ§Ø­ØŠ",
        "no_inline_cmds": "ŲØ§ ØĒŲØŦØ¯ ØŖŲØ§ŲØą ŲØĒØ§Ø­ØŠ",
        "no_inline_cmds_msg": (
            "<b>đ ŲØ§ ØĒŲØŦØ¯ ØŖŲØ§ŲØą ŲØĒØ§Ø­ØŠ ØŖŲ ŲŲØŗ ŲØ¯ŲŲ ØĨØ°Ų ŲŲŲØĩŲŲ ØĨŲŲ Ø§ŲØŖŲØ§ŲØą</b>"
        ),
        "inline_cmds": "âšī¸ {} ØŖŲØ§ŲØą ŲØĒØ§Ø­ØŠ",
        "inline_cmds_msg": "<b>âšī¸ ØŖŲØ§ŲØą ŲØĒØ§Ø­ØŠ:</b>\n\n{}",
        "run_command": "đī¸ ØĒØ´ØēŲŲ Ø§ŲØŖŲØą",
        "command_msg": "<b>đ Ø§ŲØŖŲØą '{}' </b>\n\n<i>{}</i>",
        "command": "đ Ø§ŲØŖŲØą '{}'",
        "button403": "ŲØ§ ŲŲŲŲŲ Ø§ŲØļØēØˇ ØšŲŲ ŲØ°Ø§ Ø§ŲØ˛Øą!",
        "button404": "ŲØ§ ŲŲŲŲŲ Ø§ŲØļØēØˇ ØšŲŲ ŲØ°Ø§ Ø§ŲØ˛Øą Ø¨ØšØ¯ Ø§ŲØĸŲ!",
    }

    strings_es = {
        "lang_saved": "{} <b>ÂĄIdioma guardado!</b>",
        "pack_saved": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>ÂĄPaquete de"
            " traducciÃŗn guardado!</b>"
        ),
        "incorrect_language": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Idioma"
            " incorrecto seleccionado</b>"
        ),
        "lang_removed": (
            "<emoji document_id=5368324170671202286>đ</emoji> <b>Restablecer la"
            " traducciÃŗn a los valores predeterminados</b>"
        ),
        "check_pack": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>Paquete de"
            " traducciÃŗn seleccionado incorrecto</b>"
        ),
        "check_url": (
            "<emoji document_id=5436162517686557387>đĢ</emoji> <b>URL incorrecta"
            " seleccionada</b>"
        ),
        "too_long": (
            "<emoji document_id=5433653135799228968>đ</emoji> <b>El resultado del"
            " comando excede el lÃ­mite. Enviado como archivo.</b>"
        ),
        "opening_form": " <b>Abriendo formulario...</b>",
        "opening_gallery": " <b>Abriendo galerÃ­a...</b>",
        "opening_list": " <b>Abriendo lista...</b>",
        "inline403": (
            "đĢ <b>No se permiten elementos de interfaz de usuario en este grupo</b>"
        ),
        "invoke_failed": (
            "<b>đĢ ÂĄError al invocar la unidad! Consulte el registro"
            " para obtener mÃĄs detalles</b>"
        ),
        "show_inline_cmds": "đ Mostrar todos los comandos disponibles",
        "no_inline_cmds": "No hay comandos disponibles",
        "no_inline_cmds_msg": (
            "<b>đ No hay comandos disponibles o no tienes permiso para acceder a"
            " los comandos</b>"
        ),
        "inline_cmds": "âšī¸ {} comandos disponibles",
        "inline_cmds_msg": "<b>âšī¸ Comandos disponibles:</b>\n\n{}",
        "run_command": "đī¸ Ejecutar comando",
        "command_msg": "<b>đ Comando '{}'</b>\n\n<i>{}</i>",
        "command": "đ Comando '{}'",
        "button403": "ÂĄNo puedes presionar este botÃŗn!",
        "button404": "ÂĄNo puedes presionar este botÃŗn ahora!",
    }

    @loader.command(
        ru_doc="[ŅĐˇŅĐēĐ¸] - ĐĐˇĐŧĐĩĐŊĐ¸ŅŅ ŅŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅĐš ŅĐˇŅĐē",
        de_doc="[Sprachen] - Ãndere die Standard-Sprache",
        tr_doc="[Diller] - VarsayÄąlan dili deÄiÅtir",
        uz_doc="[til] - Standart tili o'zgartirish",
        hi_doc="[ā¤­ā¤žā¤ˇā¤žā¤ā¤] - ā¤Ąā¤ŋā¤Ģā¤ŧāĨā¤˛āĨā¤ ā¤­ā¤žā¤ˇā¤ž ā¤Ŧā¤Ļā¤˛āĨā¤",
        ja_doc="[č¨čĒ] - ãããŠãĢããŽč¨čĒãå¤æ´ããžã",
        kr_doc="[ė¸ė´] - ę¸°ëŗ¸ ė¸ė´ëĨŧ ëŗę˛ŊíŠëë¤",
        ar_doc="[Ø§ŲŲØēØ§ØĒ] - ØĒØēŲŲØą Ø§ŲŲØēØŠ Ø§ŲØ§ŲØĒØąØ§ØļŲØŠ",
        es_doc="[Idiomas] - Cambiar el idioma predeterminado",
    )
    async def setlang(self, message: Message):
        """[languages in the order of priority] - Change default language"""
        args = utils.get_args_raw(message)
        if not args or any(len(i) != 2 for i in args.split(" ")):
            await utils.answer(message, self.strings("incorrect_language"))
            return

        self._db.set(translations.__name__, "lang", args.lower())
        await self.translator.init()

        for module in self.allmodules.modules:
            try:
                module.config_complete(reload_dynamic_translate=True)
            except Exception as e:
                logger.debug(
                    "Can't complete dynamic translations reload of %s due to %s",
                    module,
                    e,
                )

        lang2country = {"en": "gb", "hi": "in", "ja": "jp", "ar": "sa"}

        await utils.answer(
            message,
            self.strings("lang_saved").format(
                "".join(
                    [
                        utils.get_lang_flag(lang2country.get(lang, lang))
                        for lang in args.lower().split(" ")
                    ]
                )
            ),
        )

    @loader.command(
        ru_doc="[ŅŅŅĐģĐēĐ° ĐŊĐ° ĐŋĐ°Đē | ĐŋŅŅŅĐžĐĩ ŅŅĐžĐąŅ ŅĐ´Đ°ĐģĐ¸ŅŅ] - ĐĐˇĐŧĐĩĐŊĐ¸ŅŅ Đ˛ĐŊĐĩŅĐŊĐ¸Đš ĐŋĐ°Đē ĐŋĐĩŅĐĩĐ˛ĐžĐ´Đ°",
        de_doc=(
            "[Link zum Paket | leer um zu entfernen] - Ãndere das externe Ãbersetzungs"
            " Paket"
        ),
        tr_doc=(
            "[Ãeviri paketi baÄlantÄąsÄą | boÅ bÄąrakmak varsayÄąlan hale getirir] - Harici"
            " Ã§eviri paketini deÄiÅtir"
        ),
        uz_doc=(
            "[tarjima paketi havolasini | bo'sh qoldirish standart holatga qaytaradi] -"
            " Tashqi tarjima paketini o'zgartirish"
        ),
        hi_doc="[ā¤ā¤¨āĨā¤ĩā¤žā¤Ļ ā¤ĒāĨā¤ ā¤ā¤ž ā¤˛ā¤ŋā¤ā¤ | ā¤ā¤žā¤˛āĨ ā¤āĨā¤Ąā¤ŧ ā¤ĻāĨā¤] - ā¤Ŧā¤žā¤šā¤°āĨ ā¤ā¤¨āĨā¤ĩā¤žā¤Ļ ā¤ĒāĨā¤ ā¤Ŧā¤Ļā¤˛āĨā¤",
        ja_doc="[ãããąãŧã¸ã¸ãŽãĒãŗã¯ | įŠēįŊã§åé¤] - å¤é¨įŋģč¨ŗãããąãŧã¸ãå¤æ´ããžã",
        kr_doc="[í¨í¤ė§ ë§íŦ | ëšėëëŠ´ ė­ė ] - ė¸ëļ ë˛ė­ í¨í¤ė§ëĨŧ ëŗę˛ŊíŠëë¤",
        ar_doc="[ØąØ§Ø¨Øˇ Ø§ŲØ­Ø˛ŲØŠ | Ø§ØĒØąŲŲ ŲØ§ØąØēØ§ ŲØ­Ø°ŲŲ] - ØĒØēŲŲØą Ø­Ø˛ŲØŠ Ø§ŲØĒØąØŦŲØŠ Ø§ŲØŽØ§ØąØŦŲØŠ",
        es_doc="[Enlace al paquete | vacÃ­o para eliminar] - Cambiar el paquete de",
    )
    async def dllangpackcmd(self, message: Message):
        """[link to a langpack | empty to remove] - Change Bampi translate pack (external)
        """
        args = utils.get_args_raw(message)

        if not args:
            self._db.set(translations.__name__, "pack", False)
            await self.translator.init()
            await utils.answer(message, self.strings("lang_removed"))
            return

        if not utils.check_url(args):
            await utils.answer(message, self.strings("check_url"))
            return

        self._db.set(translations.__name__, "pack", args)
        success = await self.translator.init()

        for module in self.allmodules.modules:
            try:
                module.config_complete(reload_dynamic_translate=True)
            except Exception as e:
                logger.debug(
                    "Can't complete dynamic translations reload of %s due to %s",
                    module,
                    e,
                )

        await utils.answer(
            message,
            self.strings("pack_saved" if success else "check_pack"),
        )
