import os
import requests
from io import BytesIO
from PIL import Image


async def mtg(cmd, message, args):
    q = ' '.join(args)

    cards = requests.get('https://api.magicthegathering.io/v1/cards?name=' + q).json()

    n = 0
    list_text = 'List of cards found for `' + str(q) + '`:\n```'

    if len(cards['cards']) > 1:
        for entry in cards['cards']:
            n += 1
            list_text += '\n#' + str(n) + ' ' + entry['name']
        try:
            await cmd.bot.send_message(message.channel, list_text + '\n```\nPlease type the number corresponding to the card of your choice `(1 - ' + str(
                                len(cards)) + ')`')
        except:
            await cmd.bot.send_message(message.channel, 'The list is way too big, please be more specific...')
            return

        choice = await cmd.bot.wait_for_message(author=message.author, channel=message.channel, timeout=20)
        await cmd.bot.send_typing(message.channel)

        try:
            card_no = int(choice.content) - 1
        except:
            await cmd.bot.send_message(message.channel, 'Not a number or timed out... Please start over')
            return
        if choice is None:
            return
    else:
        card_no = 0

    try:
        try:
            card_img_url = cards['cards'][card_no]['imageUrl']
            card_img_request = requests.get(card_img_url).content
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'I was not able to get the image for the selected card...')
            return
        card_img = Image.open(BytesIO(card_img_request))
        card_img.save('cache/mtg_' + message.author.id + '.png')
        await cmd.bot.send_file(message.channel, 'cache/mtg_' + message.author.id + '.png')
        os.remove('cache/mtg_' + message.author.id + '.png')
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'Something went wrong...')
