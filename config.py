import configparser

config = configparser.ConfigParser()
config['BOT'] = {'BOT_TOKEN': 'Вставьте API TOKEN бота'}
with open(r"config.ini", 'w') as configfile:
    config.write(configfile)