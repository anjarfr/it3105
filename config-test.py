import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

for section in cfg:
    print(section)

print(cfg['game']['type'])