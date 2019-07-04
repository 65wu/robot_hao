import os,json,time,datetime


with open('awesome/plugins/group_come/setting.json','r',encoding='utf8') as set_data:
    my_data = json.load(set_data)

group_list = my_data["group_list"]
group_data = my_data["data"]



def write_data(group_id: str, user_id: str, time: int) -> None:
    file_name = 'awesome/plugins/group_come/data/' + group_id + '.txt'

    if os.path.isfile(file_name):
        f0 = open(file_name,'r')
        if f0.read() == '':
            now_data = []
        else:
            now_data = eval(f0.read())
        now_data["qq_list"].append(user_id)
        now_data["last_time"] = time
        f0.close()
        f1 = open(file_name, 'w')
        f1.write(str(now_data))
        f1.close()
    else:
        now_data = {
            "qq_list":[user_id],
            "last_time": time
        }
        f = open(file_name, 'w')
        f.write(str(now_data))
        f.close()

def get_last_time(group_id: str):
    file_name = 'awesome/plugins/group_come/data/' + group_id + '.txt'
    if os.path.isfile(file_name):
        f = open(file_name,'r')
        up_time = eval(f.read())["last_time"]
        f.close()
        return up_time
    else:
        return int(time.time()-5)


def get_welcome_qq(group_id: str) -> False or list:
    file_name = 'awesome/plugins/group_come/data/' + group_id + '.txt'
    if os.path.isfile(file_name):
        f = open(file_name,'r')
        up_time = eval(f.read())["last_time"]
        f.close()
        # before_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(up_time))
        # this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(this_time))
        # time1 = datetime.datetime.strptime(before_time,"%Y-%m-%d %H:%M:%S")
        # time2 = datetime.datetime.strptime(this_time,"%Y-%m-%d %H:%M:%S")


        # pass_time = (time2 - time1).seconds
        # set_time = group_data[group_id]["time_interval"]

        f0 = open(file_name,'r')
        now_data = eval(f0.read())
        f0.close()
        return now_data["qq_list"]

    else:
        return False




def empty_data(group_id: str):
    file_name = 'awesome/plugins/group_come/data/' + group_id + '.txt'
    f = open(file_name, 'w')
    f.close()











