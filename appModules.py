import pandas as pd
import urllib
from urllib.request import urlopen
import ssl

import time
import webbrowser as web
from datetime import datetime
from re import fullmatch
from urllib.parse import quote
import pyautogui as pg
from core import core, exceptions, log

# SSL Verification
ssl._create_default_https_context = ssl._create_unverified_context

# Read gsheets
def read_gsheet(sheetId,sheetName):
    url = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"
    data = pd.read_csv(urllib.request.urlopen(url))
    return data



pg.FAILSAFE = False

core.check_connection()


def sendwhatmsg_instantly(
    phone_no: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send WhatsApp Message Instantly"""

    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{10}$", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(4)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(wait_time - 4)
    core.findtextbox()
    pg.press("enter")
    log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)