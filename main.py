import os, json, random, string, ctypes, sys, pytz
from pystyle import Write, Colors, Colorate, Anime, System
from colorama import Fore, Style, init
from tls_client import Session
from datetime import datetime, timezone

# discord.gg/raducord
# t.me/RaduService

session = Session(client_identifier="chrome_122")

class ConsoleColor:
    red = Fore.RED
    yellow = Fore.YELLOW
    green = Fore.GREEN
    blue = Fore.BLUE
    orange = Fore.RED + Fore.YELLOW
    pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
    magenta = Fore.MAGENTA
    cyan = Fore.CYAN
    gray = Fore.LIGHTBLACK_EX + Fore.WHITE
    reset = Fore.RESET
    pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
    dark_green = Fore.GREEN + Style.BRIGHT
    light_gray = Fore.LIGHTWHITE_EX
    light_red = Fore.LIGHTRED_EX
    light_green = Fore.LIGHTGREEN_EX
    light_yellow = Fore.LIGHTYELLOW_EX
    light_blue = Fore.LIGHTBLUE_EX
    light_magenta = Fore.LIGHTMAGENTA_EX
    light_cyan = Fore.LIGHTCYAN_EX

class Checker:
    def __init__(self) -> None:
        self.owner = "H4cK3dR4Du"
        self.total_tokens = len(open('tokens.txt').readlines())
        self.time = datetime.now(timezone.utc)

    def _printBanner(self) -> str:
        System.Clear()
        Write.Print(f"""
______ _                       _ 
|  _  (_)                     | |
| | | |_ ___  ___ ___  _ __ __| |
| | | | / __|/ __/ _ \| '__/ _` |
| |/ /| \__ \ (_| (_) | | | (_| |
|___/ |_|___/\___\___/|_|  \__,_|
                                 
 _____     _                _____ _               _             
|_   _|   | |              /  __ \ |             | |            
  | | ___ | | _____ _ __   | /  \/ |__   ___  ___| | _____ _ __ 
  | |/ _ \| |/ / _ \ '_ \  | |   | '_ \ / _ \/ __| |/ / _ \ '__|
  | | (_) |   <  __/ | | | | \__/\ | | |  __/ (__|   <  __/ |   
  \_/\___/|_|\_\___|_| |_|  \____/_| |_|\___|\___|_|\_\___|_|
""", Colors.purple_to_red, interval=0.000)
        
    def _getTime(self) -> str:
        date = datetime.now()
        return "{:02d}:{:02d}:{:02d}".format(date.hour, date.minute, date.second)
    
    def _fetchTokens(self) -> dict:
        with open("tokens.txt", "r", encoding='utf-8') as f:
            return f.read().splitlines()
    
    def _putToken(self, token) -> str:
        return {"Authorization": token}
    
    def _checkTokens(self) -> None:
        tokens = self._fetchTokens()
        for token in tokens:
            try:
                headers = self._putToken(token)

                r = session.get(f"https://discord.com/api/v9/users/@me", headers=headers)
                if r.status_code == 200:
                    with open("Results/tokens.txt", "a+", encoding="utf-8") as f:
                        f.write(token + "\n")

                    id, username, global_name, email = r.json()['id'], r.json()['username'], r.json()['global_name'], r.json()['email']
                    hasNitro = r.json()['premium_type']
                    if hasNitro != 0:
                        availableBoosts = 0
                        r = session.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
                        for nitroToken in r.json():
                            ends_at = nitroToken.get('cooldown_ends_at')
                            if ends_at is None or datetime.fromisoformat(ends_at.split('+')[0] + '+00:00').replace(tzinfo=datetime.now(timezone.utc).tzinfo) <= self.time:
                                availableBoosts += 1
                        
                        text = f"Servers Boosted: None"
                        nitro = True
                        if r.json() and r.json()[0]['premium_guild_subscription'] is not None:
                            text = f"Servers Boosted: {r.json()[0]['premium_guild_subscription']['guild_id']}"
                            r = session.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers=headers)
                            with open("Results/tokens_full_capture.txt", "a+", encoding="utf-8") as f:
                                f.write(f"{token} | ID: {id} | Username / Global Name: {username}, {global_name} | Email: {email} | Nitro: {nitro} | Boosts: {availableBoosts} | {text} | Nitro Expire: {datetime.fromisoformat(r.json()[0]['trial_ends_at']).replace(tzinfo=datetime.now(timezone.utc).tzinfo).strftime('%d-%m-%Y %H:%M')}" + "\n")
                    else:
                        nitro = False
                        with open("Results/tokens_full_capture.txt", "a+", encoding="utf-8") as f:
                                f.write(f"{token} | ID: {id} | Username / Global Name: {username}, {global_name} | Email: {email} | Nitro: {nitro} | Boosts: 0 | Servers Boosted: None | Nitro Expire: Not Found" + "\n")

                        print(f"{ConsoleColor.cyan}[ {ConsoleColor.light_red}Token Checker{ConsoleColor.cyan} ] {ConsoleColor.yellow}({ConsoleColor.green}+{ConsoleColor.yellow}) {ConsoleColor.green}Valid {ConsoleColor.reset}-> {ConsoleColor.light_blue}{token[:50]}******")
                elif r.status_code == 401 or "Unauthorized" in r.text:
                    print(f"{ConsoleColor.cyan}[ {ConsoleColor.light_red}Token Checker{ConsoleColor.cyan} ] {ConsoleColor.yellow}({ConsoleColor.red}-{ConsoleColor.yellow}) {ConsoleColor.red}Invalid {ConsoleColor.reset}-> {ConsoleColor.light_blue}{token[:50]}******")
                else:
                    print(f"{ConsoleColor.cyan}[ {ConsoleColor.light_red}Token Checker{ConsoleColor.cyan} ] {ConsoleColor.yellow}({ConsoleColor.orange}*{ConsoleColor.yellow}) {ConsoleColor.yellow}Locked {ConsoleColor.reset}-> {ConsoleColor.light_blue}{token[:50]}******")
            except:
                pass

if __name__ == "__main__":
    i = Checker()
    i._printBanner()
    i._checkTokens()
    input("\n\n\nPress Enter To Exit: ")