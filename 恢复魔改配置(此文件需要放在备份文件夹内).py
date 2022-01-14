#注意 此文件需要放在备份的文件夹内
import sys
sys.path.append("..\\..\\")
from WOWAddon import CWOWAddon

wow = CWOWAddon()

#需要恢复的插件
wow.addon = [
			"Interface/AddOns/!Eva/",
			"Interface/AddOns/!Pig_classic/",
			"Interface/AddOns/ClassicCy/",
			"Interface/AddOns/CChatNotifier/",
			"Interface/AddOns/Dejunk/",
			"Interface/AddOns/ls_Toasts/",
			"Interface/AddOns/Leatrix_Plus/",
			"Interface/AddOns/KillCountBroadcast/",
			"Interface/AddOns/Molinari/",
			"Interface/AddOns/OmniCC/",
			"Interface/AddOns/OmniCC_Config/",
			"Interface/AddOns/PallyPower/",
			"Interface/AddOns/ShortKey/",
			"Interface/AddOns/TradeSkillMaster/",
			"Interface/AddOns/VuhDo/",
			"Interface/AddOns/VuhDoOptions/",
			"Interface/AddOns/WhatsTraining/",
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

#需要恢复的材质
wow.texture = [
	"Interface/AuctionFrame/",
	"Interface/Buttons/",
	"Interface/ClassTrainerFrame/",
	"Interface/Common/",
	"Interface/DialogFrame/",
	"Interface/FrameGeneral/",
	"Interface/FriendsFrame/",
	"Interface/Glues/",
	"Interface/HelpFrame/",
	"Interface/Icons/",
	"Interface/LFGFrame/",
	"Interface/MerchantFrame/",
	"Interface/MiniMap/",
	"Interface/PaperDollInfoFrame/",
	"Interface/QuestFrame/",
	"Interface/RaidFrame/",
	"Interface/SimpleChatEmojis/",
	"Interface/SpellBook/",
	"Interface/TargetingFrame/",
	"Interface/Tooltips/",
	"Interface/TradeFrame/",
	"Interface/WorldMap/"
]

#需要删除的插件
wow.rm = [
	"Interface/AddOns/alaTradeSkill/",
	"Interface/AddOns/GogoWatch/",
	"Interface/AddOns/aux-addon/",
]

wow.Restore()