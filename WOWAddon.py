from ast import Assign
import os
import re
import shutil
from datetime import datetime
from zipfile import ZipFile
# from pathlib import Path
from zipfile import Path as zPath

def IsFont_Texture(path):
    ret = re.match("Interface/.*?/", path)
    return "Fonts" in path or ret != None and "Interface/AddOns/" not in path


class ZFile():
    def __init__(self):
        self.files= {'fList':[], 'dList':[]} #文件/夹列表字典


    def GetPathList(self, rootPath):
        """[递归遍历文件夹里面所有文件夹和文件，将它们保存在成员变量files中]

        Args:
            rootPath ([string]): [要检索的根目录]
        """
        dirs = os.listdir(rootPath)
        for file in dirs:
            # 获取目录或者文件的路径
            path = os.path.join(rootPath, file)
            # 判断该路径为文件还是路径
            if os.path.isdir(path):
                self.files['dList'].append(path)
                # 递归获取所有文件和目录的路径
                self.GetPathList(path)
            else:
                self.files['fList'].append(path)
        

    def RemoveFile(self, rootPath, rFile):
        """
        将历好的文件列表中里面某些需要删除的文件进行删除操作

        Args:
            rootPath ([string]): [遍历的根目录路径]]
            rFile ([string]]): [删除的文件名(可模糊))]
        """
        self.files['dList'].clear()        #防止多余数据
        self.files['fList'].clear()
        
        self.GetPathList(rootPath)

        count = 0 

        for fileName in self.files['fList']:
            # if fileName.endswith(".baiduyun.p.downloading"): #字符串是否以指定后缀结尾
            if rFile in fileName:
                print(f"删除文件:{fileName} ...",end=" ")
                os.remove(fileName)
                print(f"完成")
                count += 1
        
        print(f"查找文件:{rFile} 共删除了 {count} 个")


    def Finish(self):
        print("程序执行完毕, 请按任意键退出", end=" ")
        os.system("pause >nul")


    def Replace(self, file, old_content, new_content):
        """[传入文件(file),将旧内容(old_content)替换为新内容(new_content)]

        Args:
            file ([str]): [欲修改的文件]
            old_content ([str]): [旧字符串内容]
            new_content ([str]): [新字符串内容]
            # 替换操作(将test.txt文件中的'Hello World!'替换为'Hello Qt!')
            # replace(r'test.txt', 'Hello World!', 'Hello Qt!')
        """
        content = self.ReadFile(file)
        content = content.replace(old_content, new_content)
        self.RewriteFile(file, content)


    # 读文件内容
    def ReadFile(self, file):
        with open(file, encoding='UTF-8') as f:
            read_all = f.read()

        return read_all
    
    def ReadLines(self, file):
        with open(file, encoding='UTF-8') as f:
            read_all = f.readlines()
        return read_all


    # 写内容到文件
    def RewriteFile(self, file, data):
        with open(file, 'w', encoding='UTF-8') as f:
            f.write(data)

    def WriteLines(self, file, data):
        with open(file, 'w', encoding='UTF-8') as f:
            f.writelines(data)


class CZipFile:

    def __init__(self):
        self.getTime()

    def getTime(self, format="%Y%m%d%H%M%S"):
        now = datetime.now()  # current date and time
        self.now = now.strftime(format)
        return self.now

    def mkdir(self, p):
        try:
            print(f"创建文件夹: {p}")
            os.makedirs(p)
        except FileExistsError:
            print(f"文件夹{p}已存在")

    def MkDir_re(self, path):
        p = re.sub(R"(.+\\|.+/).*?\..+", R"\g<1>", path)
        if not os.path.exists(p):
            self.mkdir(p)
            
    def removedirs(self, path):
        """删除文件夹(含子文件夹)

        Args:
                path ([type]): [路径]
        """
        shutil.rmtree(path, ignore_errors=True)  # 递归删除文件夹

    def create_cmd(self, zipfile, filename):
        """ python命令行方式建立zip文件
        zip.create_cmd_python("tmp.zip", "interface wtf")

        Args:
                zipfile ([type]): [zip文件名.zip]
                filename ([type]): [文件名 多个文件用空格分隔]
        """
        print(f"\n正在创建压缩文件: {zipfile} , 请稍等...", end=' ')
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

    def callbcak(filename=""):
        return False

    def extract(self, zipfile, item_name, func= callbcak):
        """[解压压缩包内的某个文件/夹]
        extract("ElvUI年月日.zip", "Interface/AddOns/!Eva/", "../../")

        Args:
                zipfile ([string]): [压缩文件名]]
                item_name ([string]): [压缩包内的完整文件夹路径名(以/分隔路径层级)]]
                path ([string]): [压缩的目标路径]
        """

        with ZipFile(zipfile) as zf:
            for fileinfo in zf.infolist():
                # 乱码转中文
                try:
                    filename = fileinfo.filename.encode('cp437').decode('gbk')
                except UnicodeEncodeError:
                    filename = fileinfo.filename
                
                if item_name in filename or func(filename):
                    # if fileinfo.file_size >0: #判断是否文件夹(文件夹大小为0)
                    self.MkDir_re(filename)
                    try:
                        with open(filename, "wb") as outputfile:
                            print(f"从{zipfile}中 释放文件: {filename} ",
                                  end="")  # 采用复制文件的方式解压
                            shutil.copyfileobj(
                                zf.open(fileinfo.filename), outputfile)
                            print("完成.")
                    except FileNotFoundError:
                        self.mkdir(filename)
                    # except FileExistsError:
                    #     if not os.path.isdir(p):
                    #         pass
                    except OSError:
                        self.mkdir(filename)

    def extract2(self, zipfile, item_name):
        """[释放文件, 在遇到已存在的文件时跳过释放]

        Args:
                zipfile ([type]): [zip文件]
                item_name ([type]): [压缩包中的文件名]
                p ([type]): [要释放的路径]
        """

        with ZipFile(zipfile, 'r') as f:
            sign = False
            for fileName in f.namelist():
                if item_name.upper() in fileName.upper():
                    try:
                        fileName = fileName.encode('cp437').decode('gbk')
                    except UnicodeEncodeError:
                        fileName = fileName

                    try:
                        self.MkDir_re(fileName)
                        print(f"从{zipfile}中 释放 {fileName} ...", end="")
                        # extracted_path = Path(f.extract(fn, p))

                        #判断目标路径是否存在文件, 如存在则删除, 防止改名失败
                        if fileName != fileName and os.path.isfile(fileName):
                            os.remove(fileName)
                        os.renames(fileName, fileName)
                        print(f"完成")
                    except FileExistsError:
                        print(
                            f"\r文件 {fileName} 已经存在,改名失败                            ")
                    except PermissionError:
                        print(
                            f"\r文件 {fileName} 拒绝访问,改名失败                            ")
                    except FileNotFoundError:
                        self.mkdir(fileName)
                    except OSError:
                        self.mkdir(fileName)


class WOW_WA(ZFile):
    def __init__(self, account= "FAIRY011"):
        super(WOW_WA, self).__init__()
        self.account= account
        self.wa_file_path = 'WTF\\Account\\'+account+'\\SavedVariables\\WeakAuras.lua'
        self.wa_zipfile_path = 'WTF/Account/'+account+'/SavedVariables/WeakAuras.lua'
        self.tableInZip = []
        self.table = []
                

    def finish(self):
        print("\n完成, 按任意键退出.")
        os.system("pause >nul")

    def ReadWA(self, zpfile):
        with ZipFile(zpfile) as zf:
            zp = zPath(zf, self.wa_zipfile_path)
            with zp.open('r', encoding='UTF-8') as f:
                self.tableInZip = f.readlines()
            # with zf.Path.open(self.wa_zipfile_path) as f:
            #     self.tableInZip = f.readlines()

        self.table = self.ReadLines(self.wa_file_path)

    def WriteWA(self):
        self.WriteLines(self.wa_file_path, self.table)    


    def readTable(self, str, i):
        pass

    def Escape(self, str):
        #转义字符串
        esc ='\$()*+.[]?^{}|' #需要转义的字符
        l = len(esc)
        for i in range(l):
            n = str.find(esc[i])
            if n != -1:
                str = '\\'.join([str[:n],str[n:]])
           
        return str

    def modTable(self, table, key, value, begin, end):
        pattern = FR'(^\t\t\t\["{key}"\] = ).*?(,.*?)'
        repl =FR'\g<1>{value}\2'
        for i in range(begin, end):
            if re.match(pattern, table[i]):
                print(f"\t修改前: {table[i]}", end="")
                table[i] = re.sub(pattern, repl, table[i])
                print(f"\t修改后: {table[i]}", end="")
                return True

        return False

    def WriteMap(self, file, wa):
        print(f"生成备份文件: {file}", end="")
        with open(file, 'w', encoding='UTF-8') as f:
            f.writelines(wa['child'])
            f.writelines(wa['parent'])

        print(f"\r生成备份文件: {file}...完成")


    def WA_Del(self, key, begin = 0, end = 0):
        if not begin and not end :
            begin, end = self.GetTable(key, self.table)

        if not begin:
            # raise AssertionError(f"没有找到想要删除的项: {key}, 请检查你要删除的内容")
            print(f"没有找到要删除的WA项: {key}, 可能已经被删除或是填写错误请检查你要删除的内容")
        else:
            print(f"删除WA项: {key}")
            self.table[begin:end] = []
            

    def WAS_Del(self, keys):
        #批量删除WA项与子项
        for key in keys:
            wa ={
            'parent':[],
            'controlledChildren':[],
            }

            begin, end = self.fillParent(self.table, wa, key)  #填充父节点内容
            self.fillChild(wa)                #填充子节点节点名内容

            self.WA_Del(key, begin, end)      #删除父

            for v in wa['controlledChildren']:
                self.WA_Del(v)

            


    def InsertTable(self, table, wa, key):
        begin, end = self.GetTable(key, table)
        if begin: 
            print(f"导入已存在的wa:{key} 覆盖升级")
            table[begin:end] = wa   #如果存在就覆盖插入
        else:
            location, end = self.GetTable('【露露】TBC消耗品01', table)
            table[location:location] = wa   #插入

    def rec_go(self, zipfile, wa):
        self.ReadWA(zipfile)
        self.WAS_Del(wa['del'])
        self.WA_Import(wa['rec'])
        self.WriteWA()

    def WA_Import(self, parentName):
        for v in parentName:
            wa ={
            'parent':[],
            'controlledChildren':[],
            'child':[]
            }

            print(f"导入WA组项目:{v}")
            #读入备份内容
            self.fillParent(self.tableInZip, wa, v)  #填充父节点内容
            self.fillChild(wa)                #填充子节点节点名内容

            for v in wa['controlledChildren']:
                self.fillParent(self.tableInZip, wa, v, 'child')  #填充父节点内容
                self.InsertTable(self.table, wa['child'], v)

            self.InsertTable(self.table, wa['parent'], v)

        


    def WA_Export(self, parentName):
        table = self.ReadLines(self.wa_file_path)
        
        # controlledChildren
        wa ={
            'parent':[],
            'controlledChildren':[],
            'child':[]
        }

        print(f"备份WA组项目:{parentName}")

        self.fillParent(table, wa, parentName)  #填充父节点内容
        self.fillChild(wa)  #填充子节点节点名内容
        
        
        for v in wa['controlledChildren']:
            self.fillParent(table, wa, v, 'child')  #填充父节点内容

        self.WriteMap(FR"Bak\WA\{parentName}.txt", wa)
        


    def fillChild(self, wa):
        begin, end = self.GetTable('controlledChildren', wa['parent'], isChild = True)

        for i in range(begin+1, end-1): #去开头和结尾行
            #只保留关键字
            s = re.sub(FR'.*?"(.*?)".*?\n', FR'\g<1>',wa['parent'][i])
            if s[-1] == '\\': s = s.rstrip('\\')  #移除尾部
            wa['controlledChildren'].append(s)


    def fillParent(self, table, wa, parentName, node = 'parent'):
        print(f'正在填充节点:{parentName}', end='')
        begin, end = self.GetTable(parentName, table)
        if begin:
            wa[node] = table[begin:end]

        # for i in range(begin, end):
        #     wa[node].append(table[i])
        
        print(f'\r正在填充节点:{parentName} ...完成')
        return begin, end


    def GetTable(self, key, table, isChild= False, begin = 0, end = 0):
        """获取表范围"""
        l = len(table)
        tab = R"\t\t"
        beginp=R'^'+tab+'\["'+ key +'.*?"\] = {'
        endp = R'^'+tab+'\[".*?"\] = {'
        if isChild:
            tab = R"\t\t\t"
            beginp=R'^'+tab+'\["'+ key +'.*?"\] = {'
            endp = R'^'+tab+'\[".*?"\] = .*?'
        
        start = end 
        for i in range(start, l):
            if re.match(beginp, table[i]):
                # print(table[i])
                begin = i
            elif begin !=0  and re.match(endp, table[i]):
                end = i
                # print(table[i])
                break
        return begin,end
            
    def GetTableChild(self, key, table, l):
        begin=0
        end=0
        for i in range(l):
            if re.match(R'^\t\t\t\["'+ key +'.*?"\] = {', table[i]):
                # print(table[i])
                begin = i
            elif begin !=0  and re.match(R'^\t\t\[".*?"\] = {', table[i]):
                end = i
                # print(table[i])
                break
        return begin,end



class CBandizip(CZipFile):
    def __init__(self) -> None:
        super().__init__()
        self.bzpath = R"C:\Program Files\Bandizip\Bandizip.exe"
        self.bzIsExist = self.IsExistBandizip()  # 是否存在bz

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


        self.rm = [
            "Interface/AddOns/alaTradeSkill/",
            "Interface/AddOns/GogoWatch/",
            "Interface/AddOns/aux-addon/",
        ]

        self.WA = {
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
            'del':[
                '【标记】标记助手两侧',
                '【按钮】新微型菜单（露露改）',
                '【通用】点我吃面包（露露改）',
            ]
        }


    def GetAddonName(self):
        fileName = "Bak"

        if os.path.isdir(R"Interface\AddOns\NDUI"):
            fileName = 'NDUI'
        elif os.path.isdir(R"Interface\AddOns\ElvUI"):
            fileName = 'ElvUI'

        return fileName

    def GetZipFileName(self, dir='./', ext='.zip'):
        """[获取指定类型的文件名]

        Args:
                dir (str, optional): [指定目录, 默认当前]. Defaults to './'.
                ext (str, optional): [扩展名, 默认.zip]. Defaults to '.zip'.

        Returns:
                [str]: [zip文件名] 或 None 
        """
        for root, dirs, files in os.walk(dir):
            # root当前目录路径  dirs当前路径下所有子目录  files当前路径下所有非目录子文件
            file = []
            for f in files:
                if ext in f:
                    file.append(f)
            if len(file) > 1:
                file.sort(reverse=True)
            return file[0]
        return None

    def GetZipFileNameInFile(self):
        """从文件中获取最后的备份文件名,省去了在目标路径中操作的麻烦

        Returns:
            [type]: [description]
        """
        with open("LostBak.txt") as f:
            path = f.read()
        return path

    def removeAddon(self):
        for l in self.rm:
            print(f"删除插件: {l} ")
            super().removedirs(l)



    def Bak(self):
        """[备份WOW插件]
        """
        
        path = FR"Bak\{self.GetAddonName()}\{self.GetAddonName()}{self.now}.zip"
        self.MkDir_re(path)
        # os.system(FR"copy /y 恢复魔改配置.py Bak\{self.GetAddonName()}\恢复魔改配置.py")
        
        with open(f"LostBak.txt", "w") as f:
            f.write(path)

        if self.bzIsExist:
            self.create(path, "Interface WTF Fonts")
        else:
            super(CBandizip, self).create_cmd(path, "Interface WTF Fonts")
        

    def Restore(self, account):
        """[更新插件后的插件和配置恢复]
        """

        zipfile = self.GetZipFileNameInFile()

        # waObj = WOW_WA(account)
        # waObj.rec_go(zipfile, self.WA)
        # exit()
        for a in self.addon:
            self.extract(zipfile, a)

        for w in self.wtf:
            self.extract2(zipfile, w)

        self.extract(zipfile, "Fonts", IsFont_Texture)

        self.removeAddon()

        waObj = WOW_WA(account)
        waObj.rec_go(zipfile, self.WA)

        print(f"从 {zipfile} 中操作完毕")
        
