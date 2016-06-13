import requests
from cloudbot import hook

API_URL = "https://uthgard.org/herald/api/player/{}"

def format_data(data):
    """function which formats the data and returns it as a clean string for irc"""
    reply = data['name']
    # we cast realmrank to float here to account for integers showing up in the api data
    realmrank, realmlevel = str(float(data['realmrank'])).split('.')

    if data['guild']:
        reply += " <{}>".format(data['guild'])

    reply += " - Level {level} {race} {class} - Realm Rank {0}L{1}".format(realmrank, realmlevel, **data)

    if data['rp']:
        reply += " - RPs: {: ,}".format(data['rp'])

    return reply

@hook.command("h", "herald")
def herald(text, notice):
    """herald <player name> - Search for player info matching <player name>"""
    player_name = text.capitalize()
    request = requests.get(API_URL.format(player_name))

    # no error checking, fail silently if the data could not be fetched
    if request.status_code != requests.codes.ok:
        return
    
    data = request.json()
    player_data = {
        "name": data.get('FullName'),
        "guild": data['Raw'].get('GuildName'),
        "level": data.get('Level'),
        "race": data.get('RaceName'),
        "class": data.get('ClassName'),
        "realmrank": data.get('RealmRank'),
        "rp": data['Raw'].get('RP')
    }

    reply = format_data(player_data)

    notice(reply)
