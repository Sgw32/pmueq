from configparser import ConfigParser

Parser = ConfigParser()
Parser.read('config.ini')

print(Parser.sections())

print(Parser.get('default values','temperature 1'))
