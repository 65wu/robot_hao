from nonebot import on_notice, NoticeSession

import time, random, datetime, requests, multiprocessing
from .read_data import group_data, group_list, get_welcome_qq, write_data, get_last_time, empty_data


# 打印存在功能的群
print("-----------------------")
print(group_list)
for i in group_list:
    empty_data(i)
print("_______________________")



'''
# 创建一个队列
q = multiprocessing.Queue()


def control_msg(q):
    while True:
        print(11111111111111111)
        my_data0 = q.get()
        print(session)
        group_id = str(session.ctx['group_id'])
        print(22222222222222222)

        # 发送欢迎消息
        if (my_data0['notice_type'] == 'group_increase') and (group_id in group_list):
            user_id = str(my_data0['user_id'])
            now_time = str(my_data0['time'])
            print("------------")
            write_data(group_id,user_id,int(now_time))
            print("------------")
            # 处理时间
            now = int(time.time())
            this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            last_t = get_last_time(group_id)
            last_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_t))
            time1 = datetime.datetime.strptime(last_t,"%Y-%m-%d %H:%M:%S")
            time2 = datetime.datetime.strptime(this_time,"%Y-%m-%d %H:%M:%S")

            # 查看设置时间间隔
            set_time = group_data[group_id]["time_interval"]

            # 判断时间差是否大于设置时间
            while (time2 - time1).seconds < set_time:
                time.sleep(set_time - (time2 - time1).seconds)
                now = int(time.time())
                this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                last_t = get_last_time(group_id)
                last_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_t))
                time1 = datetime.datetime.strptime(last_t,"%Y-%m-%d %H:%M:%S")
                time2 = datetime.datetime.strptime(this_time,"%Y-%m-%d %H:%M:%S")
            if_wel = get_welcome_qq(group_id)
            if if_wel != False:

                welcome_word = random.choice(group_data[group_id]["welcome_word_list"])
                # await session.send(datas)
                at_data = ''
                for i in if_wel:
                    at_data += "%5bCQ%3aat%2cqq%3d{}%5d".format(i)
                res = requests.get('http://127.0.0.1:5700/send_group_msg?group_id={}&message={}%20{}&boolean=true'.format(group_id,at_data,welcome_word))
                empty_data(group_id)
                # requests.get("http://127.0.0.1:5700/send_private_msg?user_id=1097977702&message={}".format(res.text))
                # print(res.text)

'''

# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    group_id = str(session.ctx['group_id'])
    notice_type = str(session.ctx['notice_type'])
    user_id = str(session.ctx['user_id'])
    now_time = str(session.ctx['time'])
    my_data0 = {
        'group_id':group_id,
        "notice_type":notice_type,
        "user_id":user_id,
        "now_time":now_time
    }

    if (my_data0['notice_type'] == 'group_increase') and (group_id in group_list):
        user_id = str(my_data0['user_id'])
        now_time = str(my_data0['time'])
        print("------------")
        write_data(group_id,user_id,int(now_time))
        print("------------")
        # 处理时间
        now = int(time.time())
        this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        last_t = get_last_time(group_id)
        last_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_t))
        time1 = datetime.datetime.strptime(last_t,"%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(this_time,"%Y-%m-%d %H:%M:%S")

        # 查看设置时间间隔
        set_time = group_data[group_id]["time_interval"]

        # 判断时间差是否大于设置时间
        while (time2 - time1).seconds < set_time:
            time.sleep(set_time - (time2 - time1).seconds)
            now = int(time.time())
            this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            last_t = get_last_time(group_id)
            last_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_t))
            time1 = datetime.datetime.strptime(last_t,"%Y-%m-%d %H:%M:%S")
            time2 = datetime.datetime.strptime(this_time,"%Y-%m-%d %H:%M:%S")
        if_wel = get_welcome_qq(group_id)
        if if_wel != False:

            welcome_word = random.choice(group_data[group_id]["welcome_word_list"])
            # await session.send(datas)
            at_data = ''
            for i in if_wel:
                at_data += "%5bCQ%3aat%2cqq%3d{}%5d".format(i)
            res = requests.get('http://127.0.0.1:5700/send_group_msg?group_id={}&message={}%20{}&boolean=true'.format(group_id,at_data,welcome_word))
            empty_data(group_id)
            # requests.get("http://127.0.0.1:5700/send_private_msg?user_id=1097977702&message={}".format(res.text))
            # print(res.text)
    # q.put(my_data0)



# p = multiprocessing.Process(target=control_msg,args=(q,))

