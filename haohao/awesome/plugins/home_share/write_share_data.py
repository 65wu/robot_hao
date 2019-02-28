import time,datetime,calendar
from requests import get


# 如果不是礼拜一返回下一个礼拜一，是礼拜一则判断是否8点前，是则返回今天，否则还是返回下个礼拜一
def get_next_monday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days = 1)
    m1 = calendar.MONDAY
    if (today.weekday() == m1) and (time.strftime('%H',time.localtime())<=20):
        return today.strftime('%Y%m%d')
    else:
        today += oneday
        while today.weekday() != m1:
            today += oneday
        next_monday = today.strftime('%Y%m%d')
    return next_monday


async def get_share_data(share_data: str, sender_data) -> str:
    group_id = eval(open('awesome/plugins/home_share/data/config.json','r').read())['yanfa']
    datas = get('http://127.0.0.1:5700/get_group_member_info?group_id={}&user_id={}'.
                format(group_id,sender_data['sender']['user_id']))
    card = eval(datas.text.replace('true','True').replace('false','False'))['data']['card']
    mon_time = get_next_monday()
    file = open('awesome/plugins/home_share/data/{}.txt'.format(str(mon_time)), 'a+')
    file.write(share_data + '@' + card + '\r\n'+'buhuizhemeqiaoba') # 不会这么巧吧 用于间隔不同的消息
    file.close()
    # print(open('awesome/plugins/home_share/data/{}.txt'.format(str(mon_time)), 'r').readlines())
    # 这里简单返回一个字符串
    return '好哒！ 谢谢你的分享!'

