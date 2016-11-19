async def level(cmd, message, args):
    try:
        user_id = message.mentions[0].id
        mid_msg = ' is'
        end_msg = 'has'
    except:
        user_id = message.author.id
        mid_msg = '. You are'
        end_msg = 'have'

    query = {
        'UserID': user_id,
        'ServerID': message.server.id
    }
    number_grabber = cmd.db.find('PointSystem', query)
    points = 0
    for result in number_grabber:
        try:
            points = result['Points']
        except:
            pass
    level = points / 1690
    points = str(points)
    level = str(level).split('.')[0]
    msg = 'Okay, <@{:s}>{:s} **Level {:s}** and currently {:s} **{:s} Points**!'
    await cmd.bot.send_message(message.channel, msg.format(user_id, mid_msg, level, end_msg, points))
