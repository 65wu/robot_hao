from os import path
import nonebot
import config
from aiocqhttp import CQHttp

bot = CQHttp(api_root='http://127.0.0.1:5700/')

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    nonebot.run(host='127.0.0.1', port=8080)