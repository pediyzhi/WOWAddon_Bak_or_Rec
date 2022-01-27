#注意 此文件需要放在备份的文件夹内
import sys
sys.path.append("..\\..\\")
from WOWAddon import CWOWAddon

wow = CWOWAddon()

#需要恢复的插件
wow.addon = [
			"Interface/AddOns/!Eva/",
			"Interface/AddOns/ClassicCy/",
			"Interface/AddOns/Dejunk/",
			"Interface/AddOns/Molinari/",
			"Interface/AddOns/OmniCC/",
			"Interface/AddOns/OmniCC_Config/",
			"Interface/AddOns/PallyPower/",
			"Interface/AddOns/ShortKey/",
			"Interface/AddOns/TradeSkillMaster/",
			"Interface/AddOns/BoomTime/",
			"Interface/AddOns/SpeedyAutoLoot/"
		]

#需要恢复的 wtf 配置
wow.wtf = [
	"layout-local",
	"MikScrollingBattleText",
	"Myslot",
	"AutoShop",
	"BoomTime",
	"Dejunk",
	"ala",
	# "ElvUI"
]

#需要删除的插件
wow.rm = [
	"Interface/AddOns/alaTradeSkill/",
	"Interface/AddOns/GogoWatch/",
	"Interface/AddOns/aux-addon/",
]

#WA
wow.WA = {
	#需要恢复的WA项
	'rec':[
		'小喵-T6-BT-阿克蒙德-空气爆裂-无脑版',
		'小喵-T6-BT-血沸', 
		'小喵-T6-BT-主母-致命吸引',
		'小喵-T6-BT-高阶督军-扔刺',
		'小喵-T6-BT-三脸-打断',
		'小喵-T6-盾反助手',
		'小喵-掉落占卜',
		'小喵-团队绯闻'
	],

	#需要删除的WA项
	'del':[
		'【标记】标记助手两侧',
		'【按钮】新微型菜单（露露改）',
		'【通用】点我吃面包（露露改）',
		'【露露】标记助手',
	]
}

wow.Restore("FAIRY011")