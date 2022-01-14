import os
import shutil
from datetime import datetime
from zipfile import ZipFile
from pathlib import Path

class CZipFile:

	def __init__(self):
		self.getTime()
	
	def getTime(self, format="%Y%m%d%H%M%S"):
		now = datetime.now() # current date and time
		self.now = now.strftime(format)
		return self.now

	def mkdir(self, p):
		try:
			print(f"创建文件夹: {p}")
			os.makedirs(p)
		except FileExistsError:
			print(f"文件夹{p}已存在")
   
	def removedirs(self, path):
		"""删除文件夹(含子文件夹)

		Args:
			path ([type]): [路径]
		"""
		shutil.rmtree(path, ignore_errors=True) #递归删除文件夹
   
	def create_cmd(self, zipfile, filename):
		""" python命令行方式建立zip文件
		zip.create_cmd_python("tmp.zip", "interface wtf")
  
		Args:
			zipfile ([type]): [zip文件名.zip]
			filename ([type]): [文件名 多个文件用空格分隔]
		"""
		print(f"正在创建压缩文件: {zipfile} , 请稍等...", end=' ')
		os.system(f"python -m zipfile -c {zipfile} {filename}")
		print(f"\r压缩文件: {zipfile} , 创建完成              ")

	def create(self, zip_name, file):
		"""
		create("tst.zip", {"interface", "wtf"})

		Args:
			zip_name ([type]): [zip文件名(含路径)]
			file ([type]): [文件数组列表]
		"""
		with ZipFile(zip_name, 'w', ZipFile.ZIP_DEFLATED) as zip_ref:
			for dir in file:
				for folder_name, subfolders, filenames in os.walk(dir):
					for filename in filenames:
						file_path = os.path.join(folder_name, filename)
						print(f"添加文件: {file_path} ", end="")
						zip_ref.write(file_path)
						print("完成")


	def create_make_archivezipfile(self, zip_name, root_dir='./', base_dir=None):
		"""
		创建压缩包, 但是不能同时添加两个及以上目录, 单个目录的话比较好用
  		shutil.make_archive("zip_name", 'zip', "./" "interface")

		Args:
			zip_name ([type]): [zip文件名 不用带.zip 扩展名]
			root_dir (str, optional): [根目录]. Defaults to './'.
			base_dir ([type], optional): [子目录]. Defaults to None.
		"""
		print(f"正在创建压缩文件: {zip_name}.zip ,请稍等")
		shutil.make_archive(zip_name, 'zip', root_dir, base_dir)
		print("创建完成")
	
 
	def extract(self, zipfile, item_name, path):
		"""[解压压缩包内的某个文件/夹]
		extract("ElvUI年月日.zip", "Interface/AddOns/!Eva/", "../../")

		Args:
			zipfile ([string]): [压缩文件名]]
			item_name ([string]): [压缩包内的完整文件夹路径名(以/分隔路径层级)]]
			path ([string]): [压缩的目标路径]
		"""
		if path[-1] != "/": path+='/'
		# if item_name[-1] != '/':item_name+='/'

		with ZipFile(zipfile) as zf:
			for fileinfo in zf.infolist():
				#乱码转中文
				filename = fileinfo.filename.encode('cp437').decode('gbk')
				if item_name in filename:
					p =path+filename
					# if fileinfo.file_size >0: #判断是否文件夹(文件夹大小为0)
					try:
						with open(p, "wb") as outputfile:
							print(f"从{zipfile}中 释放文件: {p} ", end="") #采用复制文件的方式解压
							shutil.copyfileobj(zf.open(fileinfo.filename), outputfile)
							print("完成.")
					except FileNotFoundError:
						self.mkdir(p)
					except OSError:
						self.mkdir(p)
					# else:
					# 	self.mkdir(p)

	def extract2(self, zipfile, item_name, p):
		"""[释放文件, 在遇到已存在的文件时跳过释放]

		Args:
			zipfile ([type]): [zip文件]
			item_name ([type]): [压缩包中的文件名]
			p ([type]): [要释放的路径]
		"""
		if p[-1] != "/": p+='/'
		rdir=""
		with ZipFile(zipfile, 'r') as f:
			sign = False
			for fn in f.namelist():
				if item_name.upper() in fn.upper():
					try:
						fn_cn = fn.encode('cp437').decode('gbk')
						# if fn != fn_cn and sign == False:
						# 	rdir = p+fn
						# 	sign = True
						print(f"从{zipfile}中 释放 {p+fn_cn} ...", end="")
						extracted_path = Path(f.extract(fn, p))

						#判断目标路径是否存在文件, 如存在则删除, 防止改名失败
						if fn_cn != fn and os.path.isfile(p+fn_cn):
								# print(f"\r删除目标路径文件: {p+fn_cn}                                  ")
								os.remove(p+fn_cn)
						# extracted_path.rename(p+fn_cn)
						os.renames(p+fn, p+fn_cn)
						# if fn_cn != fn:
						# 	extracted_path.replace(p+fn_cn)
						print(f"完成")
					except FileExistsError:
						print(f"\r文件 {p+fn_cn} 已经存在,改名失败                            ")
					except PermissionError:
						print(f"\r文件 {p+fn_cn} 拒绝访问,改名失败                            ")
		
		# if os.path.exists(rdir):
		# 	print(f"删除乱码文件{rdir}")
		# 	self.removedirs(rdir)



class CBandizip(CZipFile):
	def __init__(self) -> None:
		super().__init__()
		self.bzpath = R"C:\Program Files\Bandizip\Bandizip.exe"
		self.bzIsExist = self.IsExistBandizip() #是否存在bz

	def IsExistBandizip(self):
		return os.path.exists(R"C:\Program Files\Bandizip\Bandizip.exe")

	def create(self, zipfile, filename):
		"""
		创建压缩文件, 如已存在则覆盖
		zipfile = 要创建的压缩包名称 (包含路径)
		filename = 要添加的压缩文件/夹 (包含路径) 多个文件/夹 用空格分隔
		示例: CZip.create(f"Bak\{CZip.now}\ElvUI{CZip.now}.zip", "Interface WTF")
		-cp:65001是utf-8编码
		"""
		print(f"正在创建压缩文件: {zipfile} , 请稍等...", end=' ')
		cmd = f"Bandizip.exe c {zipfile} {filename}"
		os.system(cmd)
		print(f"\r压缩文件: {zipfile} , 创建完成              ")

	def extractAllCMD(self, zipfile, path):
		cmd = f"Bandizip.exe x -o:{path} {zipfile} "
		os.system(cmd)


class CWOWAddon(CBandizip):
	def __init__(self):
		super().__init__()
		self.addon = [
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

		self.wtf = [
			"layout-local",
			"MikScrollingBattleText",
			"Myslot",
			"AutoShop",
			"BoomTime",
			"Dejunk",
			"ala",
			# "ElvUI"
		]

		self.texture = [
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

		self.rm = [
			"Interface/AddOns/alaTradeSkill/",
			"Interface/AddOns/GogoWatch/",
			"Interface/AddOns/aux-addon/",
		]

  

	def GetAddonName(self):
		fileName="Bak"

		if os.path.isdir(R"Interface\AddOns\NDUI"):
			fileName = 'NDUI'
		elif os.path.isdir(R"Interface\AddOns\ElvUI"):
			fileName = 'ElvUI'

		return fileName


	def GetZipFileName(self, dir='./', ext = '.zip'):  
		"""[获取指定类型的文件名]

		Args:
			dir (str, optional): [指定目录, 默认当前]. Defaults to './'.
			ext (str, optional): [扩展名, 默认.zip]. Defaults to '.zip'.

		Returns:
			[str]: [zip文件名] 或 None 
		"""
		for root, dirs, files in os.walk(dir): 
			# root当前目录路径  dirs当前路径下所有子目录  files当前路径下所有非目录子文件
			file= []
			for f in files:
				if ext in f:
					file.append(f)
			if len(file) >1:
				file.sort(reverse=True)
			return file[0]
		return None


	def removeAddon(self, path):
		for r in self.rm:
			p= path+r
			# dir_list = os.listdir(p)
			# os.removedirs(p)
			print(f"删除插件: {p} ")
			super().removedirs(p)

	def Bak(self):
		"""[备份WOW插件]
		"""
		path = f"Bak\{self.GetAddonName()}\{self.GetAddonName()}{self.now}.zip"

		if self.bzIsExist:
			self.create(path, "Interface WTF")
		else:
			super(CBandizip, self).create_cmd(path, "Interface WTF")
  


	def Restore(self, path= "../../"):
		"""[更新插件后的插件和配置恢复]
		"""
		zipfile= self.GetZipFileName()
		for a in self.addon:
			self.extract(zipfile, a, path)
		
		for w in self.wtf:
			self.extract2(zipfile, w, path)
		
		for t in self.texture:
			self.extract(zipfile, t, path)

		self.removeAddon(path)
		print(f"从 {zipfile} 中操作完毕")
  

