'''
处理自动回复逻辑

每个消息都经过main_handl函数进行处理

replay_rules 是外部资源文件。
用来存储一个符合自动回复规则的字典

'''

from django.template.loader import render_to_string
import time
# 引入自动回复字典文件
from .replay_rules import rules
# 引入外部处理函数
from .ss_invite import code_back


nav_bar = '''公众号正在开发中...
 
回复「指南」
即可获得精品文章   
'''


def main_handle(xml):

    # 找到传来的消息事件：
    # 如果普通用户发来短信，则event字段不会被捕捉
    try:
        event = xml.find('Event').text
    except:
        event = '木有事件发生'

    try:
        # 找到此次传送的消息信息的类型和内容
        msg_type = xml.find('MsgType').text
        msg_content = xml.find('Content').text
    except:
        msg_type = ''
        msg_content = ''

    # 后台打印一下日志
    print(msg_type, msg_content, event)

    # 判断是否是新关注的用户
    if event == 'subscribe':
        text = '欢迎关注公众号，回复「指南」即可获得精品文章'
        return parser_text(xml, text)

    # 判断消息类型是否是文本
    # 目前只能自动回复文本类型的消息
    if msg_type == 'text':
        # 当收到的信息在处理规则之中时
        if msg_content in rules.keys():
            text = rules[msg_content]
            return parser_text(xml, text)
        # 针对邀请码特殊处理
        elif msg_content == '邀请码':
            return code_back(xml)
        # 当不属于规则是，返回一个功能引导菜单
        else:
            return parser_text(xml, text=nav_bar)

    else:
        return 'success'


def parser_text(xml, text):
    '''
    处理微信发来的文本数据
    返回处理过的xml
    '''
    print(text)
    # 我们翻转发件人和收件人的消息
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text
    # event事件是咩有msg id 的
    try:
        message_id = xml.find('MsgId').text
    except:
        message_id = ''
    # 我们来构造需要返回的时间戳
    nowtime = str(int(time.time()))

    context = {
        'FromUserName': fromUser,
        'ToUserName': toUser,
        'Content': text,
        'time': nowtime,
        'id': message_id,
    }
    # 我们来构造需要返回的xml
    respose_xml = render_to_string('SS/wx_text.xml', context=context)

    return respose_xml
