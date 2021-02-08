import json,os
PLUGIN_METADATA = {
	'id': 'betterwhitelist',
	'version': '20210116',
	'name': 'BetterWhitelist',
	'description': 'A highly customizable MCDR whitelist plugin',
	'author': 'Guang_Chen_',
	'link': 'https://github.com/GuangChen2333/BetterWhitelist',
	'dependencies': {
		'mcdreforged': '>=1.0.0',
	}
}
DefaultConfig = {
    'permission':2,
    'tip':'§4The server has enabled the whitelist. Please check your whitelist and try again.',
    'commands':[
        '!!whitelist',
        '!!wl'
    ],
    'whitelist':[]
}
config_path = '.\\config\\BetterWhitelist.json'
config = DefaultConfig.copy()

def WriteConfig(newconfig=[]):
    with open(config_path,'w',encoding='utf-8') as f:
        f.write(json.dumps(newconfig,sort_keys=True,indent=4,ensure_ascii=False,separators=(',', ': ')))

def LoadConfig():
    global config
    with open(config_path,'r',encoding='utf-8') as f:
        config = json.loads(f.read())

def on_load(server, old_module):
    if os.path.isfile(config_path):
        LoadConfig()
    else:
        WriteConfig(DefaultConfig)
    server.register_help_message(config['commands'][0], 'BetterWhitelist 白名单插件')

def on_player_joined(server, player, info):
    if not player in config['whitelist']:
        server.execute('/kick {} {}'.format(player,config['tip']))

def on_user_info(server, info):
    text = info.content.split()
    if server.get_permission_level(info) >= config['permission'] and text[0] in config['commands']:
        if len(text) == 1:
            HelpMessage = '''------Better Whitelist 白名单插件------
§6{0} §7显示帮助
§6{0} reload §7重载配置文件
§6{0} add <§6§oplayer§6> §7添加白名单
§6{0} remove/del <§6§oplayer§6> §7移除白名单'''.format(config['commands'][0])
            server.reply(info, HelpMessage)
        elif len(text) == 2:
            if text[1] == 'reload':
                LoadConfig()
                server.reply(info,'§6§l配置文件已重载')
            elif text[1] == 'list':
                for player in config['whitelist']:
                    server.reply(info,'§6{}'.format(player))
        elif len(text) == 3:
            if text[1] == 'add':
                if not text[2] in config['whitelist']:
                    config['whitelist'].append(text[2])
                    WriteConfig(config)
                    server.reply(info,'§6§l已将 {} 添加至白名单'.format(text[2]))
                else:
                    server.reply(info,'§4§l无操作，因为 {} 已在白名单内'.format(text[2]))
            elif text[1] == 'remove' or text[1] == 'del':
                if text[2] in config['whitelist']:
                    config['whitelist'].remove(text[2])
                    WriteConfig(config)
                    server.reply(info,'§6§l已移除 {} 的白名单'.format(text[2]))
                else:
                    server.reply(info,'§4§l无操作，因为 {} 不在白名单内'.format(text[2]))