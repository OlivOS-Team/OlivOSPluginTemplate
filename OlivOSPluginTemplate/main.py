import OlivOS
import OlivOSPluginTemplate

gProc = None

gPluginName = 'OlivOS插件默认模板'

class Event(object):
    def init(plugin_event, Proc):
        # 初始化流程
        pass

    def init_after(plugin_event, Proc):
        # 初始化后处理流程
        # 区别是前面的初始化流程不基于优先级
        # 而本流程基于优先级
        global gProc
        gProc = Proc

    def private_message(plugin_event, Proc):
        # 私聊消息事件入口
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        # 群消息事件入口
        unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        # 戳一戳事件入口
        poke_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        # 插件卸载时执行的保存流程
        pass

    def menu(plugin_event, Proc):
        # 插件菜单事件监听
        if plugin_event.data.namespace == 'OlivOSPluginTemplate':
            if plugin_event.data.event == 'OlivOSPluginTemplate_Menu_001':
                pass
            elif plugin_event.data.event == 'OlivOSPluginTemplate_Menu_002':
                pass

def unity_reply(plugin_event, Proc):
    # 被动回复消息示例
    if plugin_event.data.message == '/bot' or plugin_event.data.message == '.bot' or plugin_event.data.message == '[CQ:at,qq=' + str(plugin_event.base_info['self_id']) + '] .bot':
        plugin_event.reply('OlivOSPluginTemplate')
    # 主动发送消息示例
    elif plugin_event.data.message == '你好':
        if plugin_event.plugin_info['func_type'] == 'group_message':
            send_message_force(
                plugin_event.bot_info.hash,
                'group',
                plugin_event.data.group_id,
                '我好'
            )
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            send_message_force(
                plugin_event.bot_info.hash,
                'private',
                plugin_event.data.user_id,
                '我不好'
            )

def poke_reply(plugin_event, Proc):
    # 戳一戳回复消息示例
    if plugin_event.data.target_id == plugin_event.base_info['self_id']:
        plugin_event.reply('OlivOSPluginTemplate')
    elif plugin_event.data.target_id == plugin_event.data.user_id:
        plugin_event.reply('OlivOSPluginTemplate')
    elif plugin_event.data.group_id == -1:
        plugin_event.reply('OlivOSPluginTemplate')

# 主动发送消息示例实现
def send_message_force(botHash, send_type, target_id, message):
    global gProc
    global gPluginName
    Proc = gProc
    if Proc is not None \
    and botHash in Proc.Proc_data['bot_info_dict']:
        pluginName = gPluginName
        plugin_event = OlivOS.API.Event(
            OlivOS.contentAPI.fake_sdk_event(
                bot_info = Proc.Proc_data['bot_info_dict'][botHash],
                fakename = pluginName
            ),
            Proc.log
        )
        plugin_event.send(send_type, target_id, message)
