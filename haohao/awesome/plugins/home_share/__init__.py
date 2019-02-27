import pytz, os
from nonebot import on_command, CommandSession, get_bot, scheduler
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError

from .write_share_data import get_share_data, get_next_monday


@on_command('home_share', aliases=('研发分享', 'yffx'))
async def share(session: CommandSession):
    share_data = session.get('share_data', prompt='你想分享些什么呢~')
    us_data = await get_share_data(share_data,session.ctx)
    await session.send(us_data)


# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@share.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将参数名跟在命令名后面，作为参数传入
            session.state['share_data'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('你想分享些什么呢~')
    session.state[session.current_key] = stripped_arg


# 将大家的分享定时发送到群中
@scheduler.scheduled_job('interval', days=7, start_date='2019-03-04 19:59:01')
async def _():

    # 删除空字符串
    def not_empty(s):
        return s and s.strip()


    mon_time = get_next_monday()
    file_name = 'awesome/plugins/home_share/data/{}.txt'.format(str(mon_time))

    # 判断是否存在分享
    if os.path.isfile(file_name):
        bot = get_bot()
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        shares = open(file_name, 'r')
        share_list = shares.read()
        shares.close()
        shares_data = str(share_list).split('buhuizhemeqiaoba')

        # filter将列表中每个元素都执行第一个函数操作，返回一个生成器，生成器中的每一个对象是函数返回的
        real_data = filter(not_empty, shares_data)
        print(shares_data)
        what_send = ''

        # 组织语言 要发送的分享信息 发送的消息还不知道如何换行 正在想办法
        for i, item in enumerate(real_data):
            what_send = what_send + str(i+1) + '. ' + item + ' '*20

        try:
            groups_file = open('awesome/plugins/home_share/data/config.json', 'r')
            group_data = groups_file.read()
            groups_file.close()
            group_id = eval(group_data)['yanfa']
            await bot.send_group_msg(group_id=group_id, message=what_send)
        except CQHttpError:
            pass
