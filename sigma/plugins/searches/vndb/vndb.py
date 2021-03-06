import os
import sys
import requests
import Shosetsu
from PIL import Image
from io import BytesIO

setsu = Shosetsu.Shosetsu()


async def vndb(cmd, message, args):
    vndb_input = ' '.join(args)

    try:
        sdata = await setsu.search_vndb('v', vndb_input)
        n = 0
        list_text = '```'

        for entry in sdata:
            n += 1
            list_text += '\n#' + str(n) + ' ' + entry['name']

        if len(sdata) > 1:
            await cmd.bot.send_message(message.channel, list_text + '\n```')
            choice = await cmd.bot.wait_for_message(author=message.author, channel=message.channel,
                                                        timeout=20)
            await cmd.bot.send_typing(message.channel)

            try:
                nh_no = int(choice.content) - 1
            except:
                await cmd.bot.send_message(message.channel, 
                                               'Not a number or timed out... Please start over')
        else:
            nh_no = 0
        kill = 0
    except Shosetsu.VNDBOneResult as err:
        choice_id = str(err)[len(vndb_input) + len('Search ') + len(' only had one result at ID '):].replace(
            '.', '')
        kill = 1
    except Shosetsu.VNDBNoResults as err:
        await cmd.bot.send_message(message.channel, str(err))
        kill = 0
    except Exception as e:
        await cmd.bot.send_message(message.channel, 'Error: ' + str(e))
        kill = 0

    if kill == 1:
        pass
    else:
        choice_id = sdata[nh_no]['id']

    data = await setsu.get_novel(choice_id)
    vn_title = data['titles']['english']
    vn_img = data['img']
    vn_devs = ''

    for dev in data['developers']:
        vn_devs += str(dev)

    vn_desc = data['description']
    vn_id = data['id']

    if len(vn_desc) > 300:
        suffix = '...'
    else:
        suffix = ''

    vn_cover_raw = requests.get(vn_img).content
    vn_cover_res = Image.open(BytesIO(vn_cover_raw))
    vn_cover = vn_cover_res.resize((231, 321), Image.ANTIALIAS)
    base = Image.open(cmd.resource('img/base_vn.png'))
    overlay = Image.open(cmd.resource('img/overlay_vn.png'))
    base.paste(vn_cover, (110, 0))
    base.paste(overlay, (0, 0), overlay)
    base.save('cache/ani/vn_' + message.author.id + '.png')

    try:
        await cmd.bot.send_file(message.channel, 'cache/ani/vn_' + message.author.id + '.png')
        await cmd.bot.send_message(message.channel, 'Title: `' + vn_title + '`\nDescription:```\n' + vn_desc[:300] + suffix + '\n```\nMore at: <https://vndb.org/' + vn_id + '>')
        os.remove('cache/ani/vn_' + message.author.id + '.png')
    except:
        await cmd.bot.send_message(message.channel, 'Error: It goofed... =P')
