from discord import DiscordTokenGenerator

import json
import time

from datetime import datetime

import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)

settings = json.load(open('settings.json'))

dtg = DiscordTokenGenerator(settings['accounts']['password'])

while True:
    try:
        account = dtg.generate()

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if account['success']:
            with open('accounts.txt', 'a') as f:
                f.write(f"[{dt_string}] {account['token']} - {account['email']} - {account['tag']}\n")

            print(Fore.GREEN + f"[{dt_string}] {account['token']}")
        else:
            print(Fore.RED + f"[{dt_string}] ????????????????????????.??????.???????????????????????????")
    except:                                  
        pass

    time.sleep(300)
