# # 将大家的分享定时发送到群中
# from datetime import datetime,timedelta,date
# import time, calendar
# import pytz, os
# from aiocqhttp.exceptions import Error as CQHttpError
# import nonebot
#
#
# def get_next_monday():
#     today = date.today()
#     oneday = timedelta(days = 1)
#     m1 = calendar.MONDAY
#     if (today.weekday() == m1) and (time.strftime('%H',time.localtime())<=20):
#         return today.strftime('%Y%m%d')
#     else:
#         today += oneday
#         while today.weekday() != m1:
#             today += oneday
#         next_monday = today.strftime('%Y%m%d')
#     return next_monday
#
#
# @nonebot.scheduler.scheduled_job('interval', seconds=5, start_date='2019-02-27 17:37:01')
# async def _():
#     bot = nonebot.get_bot()
#     now = datetime.now(pytz.timezone('Asia/Shanghai'))
#     mon_time = get_next_monday()
#     file_name = 'awesome/plugins/home_share/data/{}.txt'.format(str(mon_time))
#     # 判断是否存在分享
#     if os.path.isfile(file_name):
#         shares = open(file_name, 'r')
#         share_list = shares.readlines()
#         shares.close()
#         shares_data = eval(str(share_list).replace('\\n',''))
#         what_send = ''
#         # 组织语言 要发送的分享信息
#         for i, item in enumerate(shares_data):
#             what_send = what_send + str(i+1) + '. ' + item + ' '*12
#             # 发送的消息还不知道如何换行 正在想办法
#         try:
#             groups_file = open('awesome/plugins/home_share/data/config.json', 'r')
#             group_data = groups_file.read()
#             group_id = eval(group_data)['yanfa']
#             await bot.send_group_msg(group_id=group_id,message=what_send)
#         except CQHttpError:
#             pass