import os
import yaml
from itertools import dropwhile

from .command import Command
from .logger import create_logger


class PluginNotEnabled(RuntimeError):
    pass


class Plugin(object):
    def __init__(self, bot, path):
        self.loaded = False
        self.help = 'No help available, sorry :('
        self.commands = {}
        self.modules = []
        self.path = path

        try:
            self.load_info(bot)
        except PluginNotEnabled:
            return

        self.log = create_logger(self.name)
        self.db = bot.db
        self.bot = bot

        self.load_commands()
        self.loaded = True

    def load_info(self, bot):
        with open(os.path.join(self.path, 'plugin.yml')) as yml_file:
            yml = yaml.load(yml_file)

            if 'enabled' not in yml or not yml['enabled']:
                raise PluginNotEnabled

            path = self.path.split('/')
            name = path.pop()

            # use the directory as plugin name if it is not set
            if 'name' not in yml:
                yml['name'] = name

            self.name = yml['name']

            # set categories from rest of pathname
            if 'categories' not in yml:
                it = iter(path)
                cat = [dropwhile(lambda x: x != 'plugins', it)][1:]
                yml['categories'] = cat

            self.categories = yml['categories']

            if 'commands' in yml:
                self.commands_info = yml['commands']

    def load_commands(self):
        for cmd_info in self.commands_info:
            cmd = Command(self, cmd_info)

            if cmd.enabled:
                self.commands.update({cmd_info['name']: cmd})
                self.modules.append(cmd.module)
