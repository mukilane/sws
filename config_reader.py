# Reads config file
# Shared between all the modules

from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')