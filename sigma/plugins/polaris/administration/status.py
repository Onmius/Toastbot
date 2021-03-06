import psutil
from humanfriendly.tables import format_pretty_table as boop


async def status(cmd, message, args):
    cpu_stats = []
    col_nam = []
    n = 1
    cpu_count = psutil.cpu_count()
    while n < (cpu_count + 1):
        col_nam.append('Core ' + str(n))
        n += 1
    for x in range(4):
        cpu_stat = psutil.cpu_percent(1, True)
        cpu_stats.append(cpu_stat)
    cpu_stats_text = 'CPU Stats:\n```haskell\n' + boop(cpu_stats, col_nam) + '\n```'
    await cmd.bot.send_message(message.channel, cpu_stats_text)
