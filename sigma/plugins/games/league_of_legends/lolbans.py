import lxml.html as l
import requests
from humanfriendly.tables import format_pretty_table as boop


async def lolbans(cmd, message, args):
    try:
        url = 'http://www.bestbans.com/'
        page = requests.get(url)
        root = l.fromstring(page.content)
        tiers = root.cssselect('.tier-row')[:-1]
        tier_list = []
        out_list = []
        for tier in tiers:
            header = tier.cssselect('.tier-header div h2')[0].text.strip()
            header = header[4:-5]
            tier_list.append(header)
            bans = tier.cssselect('.tier-body .col-xs-3')
            row = [header]
            for ban in bans:
                champion = ban.cssselect('.index-champ-name b')[1].text.strip()
                row.append('\"' + champion + '\"')
            out_list.append(row)
        out = boop(out_list)
        await cmd.bot.send_message(message.channel, '```haskell\n' + out + '\n```')
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'There was an error parsing the page.\n' + str(e))


