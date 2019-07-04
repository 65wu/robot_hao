
import json,random
from typing import Optional

import aiohttp
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression

from .what_trash import trash_sorter

# 定义无法获取图灵回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)

keys_list = ["780ac68dd9ca4ba58374b0f3db1a9b18","6a26db99154248809f0b3b750d5098c6",
             "b6aab09b04ef41898b85f60e18b69940", "6d73e92a7e594687ad8f268b4cb3d2f4",
             "ae7caaf2308a40179476062a857615e4"]
# 注册一个仅内部使用的命令，不需要 aliases
@on_command('tuling')
async def tuling(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')

    # 通过封装的函数获取图灵机器人的回复
    reply = await call_tuling_api(session, message)

    def if_at():
        _at = [True,False,False,False]
        return random.choice(_at)
    if reply:
        # 如果调用图灵机器人成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        await session.send(escape(reply),at_sender=if_at())
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取图灵回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        await session.send(render_expression(EXPR_DONT_UNDERSTAND),at_sender=if_at())


@on_natural_language
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    # print(session.ctx['message'])# 消息内容
    print(session.ctx)
    msg = str(session.ctx['message'])
    msg_type = str(session.ctx['message_type'])
    to_me = str(session.ctx['to_me'])
    # print('-------------------------------')
    # print(msg,type(msg))
    # print(len(msg),msg[1:])
    # print('-------------------------------')

    if (len(msg) > 5) and ('什么垃圾' in msg[1:]):
        print('========')
        us_data = await trash_sorter(msg)
        if msg_type == 'group' and to_me == 'True':
            # print(2222222,str(session.ctx['user_id']))
            await session.send(us_data,at_sender=True)
            pass
        else:
            await session.send(us_data)
            pass
    else:
        return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})


async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    # 调用图灵机器人的 API 获取回复

    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    # 构造请求数据
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            # 'apiKey': session.bot.config.TULING_API_KEY,
            'apiKey': random.choice(keys_list[-2:]),
            'userId': context_id(session.ctx, use_hash=True)
        }
    }

    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # 返回文本类型的回复
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None