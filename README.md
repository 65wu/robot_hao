# robot_hao
浩浩机器人是基于 nonebot 框架编写的一款多功能的机器人demo。
### pull 后需要注意修改的地方：

1.config.py 中的 SUPERUSERS 和 NICKNAME。

2.CoolQ插件中qq.json中 把测试qq替换为正式上线qq号。

3.定时任务需要 pip install "nonebot[scheduler]"

### home_share 插件

用户以命令开头做分享，机器人收集分享内容并定时发生到某个群（比如是研发群）

插件从home_share > data > config.json 中获取 group_id，读取data下txt文件后组织分享信息格式发送到对应的群。

间隔定时任务测试时使用 seconds=7 上传时记得修改为 days=7 一周一次发送。

