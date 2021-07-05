import json as js

with open('./config.json','r') as f:
    config=js.load(f)
    f.close()

if __name__ == '__main__':
    None