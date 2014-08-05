import os
import itertools
import shutil
import re
from 臺灣言語工具.語音合成.句物件轉合成標仔 import 句物件轉合成標仔
from 語音辨識.腳本程式 import 腳本程式
from 語音辨識.辨識模型 import 辨識模型
from 語音辨識.語料處理 import 語料處理

class 模型訓練(腳本程式, 語料處理):
	音檔結束符號 = '.'
	_轉合成標仔 = 句物件轉合成標仔()
	恬音 = _轉合成標仔.產生主要音值標仔(_轉合成標仔.恬音)
	短恬 = _轉合成標仔.產生主要音值標仔(_轉合成標仔.短恬)
	孤音混合數 = [1, 2, 4, 8, 12, 16, 24, 32]
	三連音混合數 = [1, 2, 4, 6, 8]
	def 訓練(self, 音檔目錄, 標仔目錄, 音節聲韻對照檔, 資料目錄, 執行檔路徑='',
			算特徵=True,  # 開發用的
			):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		全部語料 = self.揣全部語料(音檔目錄, 標仔目錄)
		
		全部特徵檔 = os.path.join(資料目錄, '全部特徵檔.scp')
		全部標仔檔 = os.path.join(資料目錄, '全部標仔檔.scp')
		os.makedirs(資料目錄, exist_ok=True)
		# 開發用的
		if 算特徵:
			self.揣特徵而且算(執行檔路徑, 資料目錄, 全部語料, 全部特徵檔)
			
		原始目錄 = self.細項目錄(資料目錄, '原始標音目錄')
		原來音類檔 = os.path.join(原始目錄, '原來音類檔.list')
		原來音節檔 = os.path.join(原始目錄, '原來音節檔.mlf')
		原來聲韻類檔 = os.path.join(原始目錄, '原來聲韻類檔.list')
		原來聲韻檔 = os.path.join(原始目錄, '原來聲韻檔.mlf')
		加恬音節檔 = os.path.join(原始目錄, '加恬音節檔.mlf')
		加恬音類檔 = os.path.join(原始目錄, '加恬音類檔.list')
		加恬聲韻類檔 = os.path.join(原始目錄, '加恬聲韻類檔.list')
		加恬聲韻檔 = os.path.join(原始目錄, '加恬聲韻檔.mlf')
		
# 		if 切標仔:
		全部標仔 = []
		for 語料 in 全部語料:
			標仔所在 = 語料[2]
			全部標仔.append(標仔所在)
		self.陣列寫入檔案(全部標仔檔, 全部標仔)
		self.標仔收集起來(執行檔路徑, 全部標仔檔, 原始目錄, 原來音類檔, 原來音節檔)
		self.標仔切做聲韻(執行檔路徑, 原來音節檔, 音節聲韻對照檔, 原始目錄, 原來聲韻類檔, 原來聲韻檔)
		self.音類標仔加短恬(原來音類檔, 加恬音類檔)
		if len(self.讀檔案(原來音節檔)) > 200:
			'音節轉聲韻，漢語聲韻加起來袂超過200'
			self.音節標仔加短恬(原來音節檔, 加恬音節檔)
		else:
			'聲韻轉聲韻，漢語聲韻加起來袂超過200'
			self.音節標仔逐字中央加短恬(原來音節檔, 加恬音節檔)
		self.標仔切做聲韻(執行檔路徑, 加恬音節檔, 音節聲韻對照檔, 原始目錄, 加恬聲韻類檔, 加恬聲韻檔)
# 		if 做初步模型:
		初步模型檔 = self.建立初步模型(執行檔路徑, 原始目錄, 全部特徵檔, 原來聲韻類檔, 原來聲韻檔)
		做好的初步模型檔 = self.模型重估(執行檔路徑, 原始目錄, 全部特徵檔, 原來聲韻類檔, 原來聲韻檔, 初步模型檔, 估幾擺=60)
# 		上尾模型檔 = 做好的初步模型檔
# 		上尾聲韻類檔 = 原來聲韻類檔
# 		上尾聲韻檔 = 原來聲韻檔
		
# 		if 加切短恬:
		短恬目錄 = self.細項目錄(資料目錄, '短恬目錄')
		加短恬的模型 = os.path.join(短恬目錄, '加短恬的模型.macro')
		self.模型加短恬(做好的初步模型檔, 加短恬的模型)
		加短恬縛好模型 = os.path.join(短恬目錄, '加短恬縛好模型.macro')
		self.恬音佮短恬愛縛做伙(執行檔路徑, 短恬目錄, 加短恬的模型, 加短恬縛好模型, 加恬聲韻類檔)
		加短恬的重估模型 = self.模型重估(執行檔路徑, 短恬目錄, 全部特徵檔,
			加恬聲韻類檔, 加恬聲韻檔, 加短恬縛好模型, 估幾擺=20)
		
		_辨識模型 = 辨識模型()
		對齊聲韻結果目錄 = _辨識模型.對齊聲韻(加恬聲韻類檔, 加短恬的重估模型, 加恬聲韻檔,
			全部特徵檔, 短恬目錄, 執行檔路徑=執行檔路徑)
		新拄好短恬全部標仔檔 = os.path.join(短恬目錄, '新拄好短恬全部標仔檔.scp')
		self.陣列寫入檔案(新拄好短恬全部標仔檔, self.標仔換目錄(全部標仔檔, 對齊聲韻結果目錄))
		
		新對齊短恬聲韻檔 = os.path.join(短恬目錄, '新對齊短恬聲韻檔.mlf')
		用袂著的檔案 = os.path.join(短恬目錄, '用袂著的檔案.garbage')
		self.標仔收集起來(執行檔路徑, 新拄好短恬全部標仔檔,
			短恬目錄, 用袂著的檔案, 新對齊短恬聲韻檔)
		新拄好短恬聲韻檔 = os.path.join(短恬目錄, '新拄好短恬聲韻檔.mlf')
		self.提掉傷短的短恬(新對齊短恬聲韻檔, 新拄好短恬聲韻檔)
		拄好短恬的重估模型 = self.模型重估(執行檔路徑, 短恬目錄, 全部特徵檔,
			加恬聲韻類檔, 新拄好短恬聲韻檔, 加短恬的重估模型, 估幾擺=20)
# 		上尾模型檔 = 拄好短恬的重估模型
# 		上尾聲韻類檔 = 加恬聲韻類檔
# 		上尾聲韻檔 = 新拄好短恬聲韻檔

# 		if 三連音:
		三連音目錄 = self.細項目錄(資料目錄, '三連音目錄')
		三連音聲韻類檔 = os.path.join(三連音目錄, '三連音聲韻類檔.list')
		三連音聲韻檔 = os.path.join(三連音目錄, '三連音聲韻檔.mlf')
		self.音標換三連音(執行檔路徑, 三連音目錄, 新拄好短恬聲韻檔, 三連音聲韻類檔, 三連音聲韻檔)
		三連音模型檔 = os.path.join(三連音目錄, '三連音模型檔.macro')
		self.模型換三連音(執行檔路徑, 三連音目錄, 拄好短恬的重估模型, 加恬聲韻類檔, 三連音模型檔, 三連音聲韻類檔)
		三連音重估模型 = self.模型重估(執行檔路徑, 三連音目錄, 全部特徵檔,
			三連音聲韻類檔, 三連音聲韻檔, 三連音模型檔, 估幾擺=20)
		三連音統計檔 = 三連音重估模型[:-len('.macro')] + '.sts'
		三連音縛做伙模型 = os.path.join(三連音目錄, '三連音縛做伙模型.macro')
		三連音縛做伙聲韻類檔 = os.path.join(三連音目錄, '三連音縛做伙聲韻類檔.tied')
		三連音縛做伙樹檔 = os.path.join(三連音目錄, '三連音縛做伙樹檔.tree')
		self.模型相倚三連音縛做伙(執行檔路徑, 三連音目錄,
			三連音模型檔, 三連音聲韻類檔, 三連音統計檔, 加恬聲韻類檔,
			三連音縛做伙模型, 三連音縛做伙聲韻類檔, 三連音縛做伙樹檔)
# 		上尾模型檔 = 三連音縛做伙模型
# 		上尾聲韻類檔 = 三連音縛做伙聲韻類檔
# 		上尾聲韻檔 = 三連音聲韻檔
			
# 		if 加混合:
		原來加混合模型 = self.加混合數(執行檔路徑, 原始目錄, 全部特徵檔,
			原來聲韻類檔, 原來聲韻檔, 做好的初步模型檔,
			self.孤音混合數, 估幾擺=10, 上尾估幾擺=50)
		短恬加混合模型 = self.加混合數(執行檔路徑, 短恬目錄, 全部特徵檔,
			加恬聲韻類檔, 新拄好短恬聲韻檔, 拄好短恬的重估模型,
			self.孤音混合數, 估幾擺=10, 上尾估幾擺=50)
		三連音加混合模型 = self.加混合數(執行檔路徑, 三連音目錄, 全部特徵檔,
			三連音縛做伙聲韻類檔, 三連音聲韻檔, 三連音縛做伙模型,
			self.三連音混合數, 估幾擺=10, 上尾估幾擺=50)
		三連音全部縛做伙模型 = os.path.join(三連音目錄, '三連音全部縛做伙模型.macro')
		三連音全部縛做伙聲韻類檔 = os.path.join(三連音目錄, '三連音全部縛做伙聲韻類檔.tied')
		self.模型加全部三連音(執行檔路徑, 三連音目錄,
			音節聲韻對照檔, 三連音縛做伙樹檔,
			三連音加混合模型, 三連音聲韻類檔, 三連音縛做伙聲韻類檔,
			三連音全部縛做伙模型, 三連音全部縛做伙聲韻類檔)

		return (原來聲韻類檔, 原來加混合模型), \
			(加恬聲韻類檔, 短恬加混合模型), \
			(三連音全部縛做伙聲韻類檔, 三連音全部縛做伙模型)
	def 標仔換目錄(self, 原本全部標仔檔, 新標仔目錄):
		全部標仔 = []
		for 標仔檔名 in self.讀檔案(原本全部標仔檔):
			標仔所在 = os.path.join(新標仔目錄, os.path.basename(標仔檔名))
			if os.path.isfile(標仔所在):
				全部標仔.append(標仔所在)
		return 全部標仔
	def 建立初步模型(self, 執行檔路徑, 資料目錄, 全部特徵檔, 聲韻類檔, 聲韻檔):
		公家模型建立參數檔 = os.path.join(資料目錄, '公家模型建立參數檔.cfg')
		self.字串寫入檔案(公家模型建立參數檔,
			self.特徵參數.format('ANON', 'HTK'))
		公家模型檔 = os.path.join(資料目錄, '公家模型檔')
		模型版檔 = os.path.join(資料目錄, '模型版檔')
		self.字串寫入檔案(模型版檔, self.模型版參數)
		公家模型指令 = '{0}HCompV -A -C {1} -m -f 0.0001 -o {2} -M {3} -I {4} -S {5} {6}'\
			.format(執行檔路徑, 公家模型建立參數檔, 公家模型檔,
				資料目錄, 聲韻檔, 全部特徵檔, 模型版檔)
		self.走指令(公家模型指令)
		公家模型 = self.讀檔案(公家模型檔)
		公家變異數檔 = os.path.join(資料目錄, 'vFloors')
		公家變異數 = self.讀檔案(公家變異數檔)
		初步模型資料 = [公家模型[:3], 公家變異數]
		公家狀態 = 公家模型[4:]
		聲韻名 = '~h "{0}"'
		for 聲韻 in self.讀檔案(聲韻類檔):
			初步模型資料.append([聲韻名.format(聲韻)])
			初步模型資料.append(公家狀態)
		初步模型檔 = os.path.join(資料目錄, '初步模型檔.macro')
		self.陣列寫入檔案(初步模型檔,
			itertools.chain.from_iterable(初步模型資料))
		return 初步模型檔
	def 模型重估(self, 執行檔路徑, 資料目錄, 全部特徵檔, 聲韻類檔, 聲韻檔, 原來模型檔, 估幾擺):
		原來模型檔檔名 = os.path.basename(原來模型檔)
		這馬模型檔 = 原來模型檔
		基本路徑 = 原來模型檔.rsplit('.', 1)[0]
		資料夾 = 基本路徑 + '-重估'
		for 第幾擺 in range(估幾擺):
			這擺資料夾 = os.path.join(資料夾, '{0:02}'.format(第幾擺))
			os.makedirs(這擺資料夾, exist_ok=True)
			新統計檔 = os.path.join(這擺資料夾, '統計.sts')
			重估指令 = '{0}HERest -A -T 407 -t 450.0 150.0 1000.0 -M {1} -H {2} -s {3} -I {4} -S {5} {6}'\
				.format(執行檔路徑, 這擺資料夾, 這馬模型檔, 新統計檔,
					聲韻檔, 全部特徵檔, 聲韻類檔)
			self.走指令(重估指令)
			這馬模型檔 = os.path.join(這擺資料夾, 原來模型檔檔名)
		上尾模型檔 = '{0}-重估.macro'.format(基本路徑)
		上尾統計檔 = '{0}-重估.sts'.format(基本路徑)
		shutil.copy(這馬模型檔, 上尾模型檔)
		shutil.copy(新統計檔, 上尾統計檔)
		return 上尾模型檔
	def 音類標仔加短恬(self, 原來音類檔, 加恬音類檔):
		音類 = self.讀檔案(原來音類檔)
		音類.append(self.短恬)
		音類.sort()
		self.陣列寫入檔案(加恬音類檔, 音類)
	def 音節標仔加短恬(self, 原來音節檔, 加恬音節檔):
		頂一逝, *後壁資料 = self.讀檔案(原來音節檔)
		加短恬音節 = [頂一逝]
		for 一逝 in 後壁資料:
			if self.是有音標仔(頂一逝) and self.是有音標仔(一逝):
				加短恬音節.append(self.短恬)
			加短恬音節.append(一逝)
			頂一逝 = 一逝
		self.陣列寫入檔案(加恬音節檔, 加短恬音節)
	def 音節標仔逐字中央加短恬(self, 原來音節檔, 加恬音節檔):
		self.音節標仔加短恬(原來音節檔, 加恬音節檔)
		加短恬音節 = []
		目前短恬數量 = 0
		for 一逝 in self.讀檔案(加恬音節檔):
			if 一逝 == self.音檔結束符號:
				目前短恬數量 = 0
			這逝是有音標仔無 = (一逝 == self.短恬)
			if 這逝是有音標仔無:
				目前短恬數量 += 1
			if not 這逝是有音標仔無 or 目前短恬數量 % 2 == 0:
				加短恬音節.append(一逝)
		self.陣列寫入檔案(加恬音節檔, 加短恬音節)
	def 是有音標仔(self, 標仔):
		if 標仔 == '#!MLF!#' or 標仔 == self.音檔結束符號 or\
				標仔.startswith('"') or 標仔 == self.恬音:
			return False
		return True
	def 提掉傷短的短恬(self, 對齊加恬聲韻檔, 新拄好短恬聲韻檔):
		新聲韻 = []
		for 一逝 in self.讀檔案(對齊加恬聲韻檔):
			try:
				開始, 結束, 標仔 = 一逝.split()
				# 無到三个音框就提掉
				if int(結束) - int(開始) >= 300000 or 標仔 != self.短恬:
					新聲韻.append(標仔)
			except:
				新聲韻.append(一逝)
		self.陣列寫入檔案(新拄好短恬聲韻檔, 新聲韻)
	def 模型加短恬(self, 原本模型, 加短恬模型):
		恬中央狀態 = '~h \"{0}.*?\".*?<STATE> 3[ \n]*(.*?)[ \n]*<STATE> 4'\
			.format(self.恬音)
		原本資料 = self.讀檔案(原本模型)
		揣著的高斯狀態 = re.search(恬中央狀態,
			'\n'.join(原本資料), re.DOTALL)
		短恬高斯狀態 = self.短恬參數.format(self.短恬, 揣著的高斯狀態.group(1))
		原本資料.append(短恬高斯狀態)
		self.陣列寫入檔案(加短恬模型, 原本資料)
	def 恬音佮短恬愛縛做伙(self, 執行檔路徑, 資料目錄,
			加短恬模型, 加短恬縛好模型, 聲韻類檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		恬音佮短恬愛縛做伙 = os.path.join(資料目錄, '恬音佮短恬愛縛做伙.hed')
		指令 = '''\
AT 2 4 0.2 {{{0}.transP}}
AT 4 2 0.2 {{{0}.transP}}
TI 短恬縛恬音 {{{0}.state[3],{1}.state[2]}}\
'''	.format(self.恬音, self.短恬)
		self.字串寫入檔案(恬音佮短恬愛縛做伙, 指令)
		縛做伙指令 = self.改模型指令.format(
			執行檔路徑, 加短恬模型, 加短恬縛好模型, 恬音佮短恬愛縛做伙, 聲韻類檔)
		self.走指令(縛做伙指令)
	def 音標換三連音(self, 執行檔路徑, 資料目錄,
			孤音聲韻檔, 三連音聲韻類檔, 三連音聲韻檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = TRUE')
		換三連音 = os.path.join(資料目錄, '換三連音.led')
		指令 = [  # 'WB {0}'.format(self.恬音),
			'WB {0}'.format(self.短恬),
			'TC']
		self.陣列寫入檔案(換三連音, 指令)
		換三連音指令 = '{0}HLEd -A -C {1} -l "*" -n {2} -i {3} {4} {5}'\
			.format(執行檔路徑, 莫跳脫聲韻, 三連音聲韻類檔, 三連音聲韻檔,
				換三連音, 孤音聲韻檔)
		self.走指令(換三連音指令)
		聲韻類 = self.讀檔案(三連音聲韻類檔)
		if self.短恬 not in 聲韻類:
			聲韻類.append(self.短恬)
			self.陣列寫入檔案(三連音聲韻類檔, 聲韻類)
	def 模型換三連音(self, 執行檔路徑, 資料目錄,
			孤音模型, 孤音聲韻類檔, 三連音模型, 三連音聲韻類檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		換三連音 = os.path.join(資料目錄, '換三連音.hed')
		指令 = ['CL {0}'.format(三連音聲韻類檔)]
		for 聲韻 in self.讀檔案(孤音聲韻類檔):
			指令.append(
				'TI T_{0} {{({0},{0}+*,*-{0},*-{0}+*).transP}}'.format(聲韻))
		self.陣列寫入檔案(換三連音, 指令)
		換三連音指令 = self.改模型指令.format(
				執行檔路徑, 孤音模型, 三連音模型, 換三連音, 孤音聲韻類檔)
		self.走指令(換三連音指令)
		
	def 模型相倚三連音縛做伙(self, 執行檔路徑, 資料目錄,
			三連音模型檔, 三連音聲韻類檔, 三連音統計檔, 孤音聲韻類檔,
			三連音縛做伙模型, 三連音縛做伙聲韻類檔, 三連音縛做伙樹檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		設定 = """\
RO 100.0 {0}
TR 0
{{0}}

TR 2
{{1}}

TR 1
AU "{1}"
CO "{2}"
ST "{3}"
SH
""".format(三連音統計檔, 三連音聲韻類檔, 三連音縛做伙聲韻類檔, 三連音縛做伙樹檔)
		問題設定 = []
		縛做伙設定 = []
		for 聲韻 in self.讀檔案(孤音聲韻類檔):
			'有恬音做樹就好，因為因兩个縛做伙'
			if 聲韻 == self.短恬:
				continue
			問題設定.append(
				'QS "頭前是{0}" {{{0}-*}}'.format(聲韻))
			問題設定.append(
				'QS "後壁是{0}" {{*-{0}}}'.format(聲韻))
			for 第幾个狀態 in range(2, 5):
				縛做伙設定.append(
					'TB {2} "縛{0}的{1}" {{({0},{0}+*,*-{0},*-{0}+*).state[{1}]}}'
						.format(聲韻, 第幾个狀態, 350.0))
		三連音縛做伙設定 = os.path.join(資料目錄, '三連音縛做伙設定.hed')
		self.字串寫入檔案(三連音縛做伙設定,
			設定.format('\n'.join(問題設定), '\n'.join(縛做伙設定)))
		三連音縛做伙指令 = self.改模型指令.format(執行檔路徑,
			三連音模型檔, 三連音縛做伙模型, 三連音縛做伙設定, 三連音聲韻類檔)
		self.走指令(三連音縛做伙指令)
	def 模型加全部三連音(self, 執行檔路徑, 資料目錄,
			音節聲韻對照檔, 三連音縛做伙樹檔,
			原來模型, 原來聲韻類檔, 原來縛做伙檔,
			全部模型檔, 全部縛做伙檔):
		'其實會當佮「三連音縛做伙」當齊做，毋過分開較知影佇創啥，親像HTS仝款加無看過的模型'
		全部聲韻 = set()
		for 聲韻 in self.讀檔案(原來聲韻類檔):
			全部聲韻.add(
				self._轉合成標仔.產生主要音值標仔(聲韻))
		聲韻排法 = []
		for 音節聲韻 in self.讀檔案(音節聲韻對照檔):
			拆聲韻 = 音節聲韻.split()[1:]
			for 聲韻 in 拆聲韻:
				if 聲韻 not in 全部聲韻:
					break
			else:
				聲韻排法.append(拆聲韻)
		家己一音 = set()
		頭一音, 頭兩音 = set(), set()
		尾一音, 尾兩音 = set(), set()
		全部三連音 = set()
		for 聲韻組 in 聲韻排法:
			頭一音.add(tuple(聲韻組[:1]))
			尾一音.add(tuple(聲韻組[-1:]))
			if len(聲韻組) == 1:
				'予因莫食著邊仔的音'
				if 聲韻組[0] not in [self.恬音, self.短恬]:
					家己一音.add(tuple(聲韻組))
			else:
				頭兩音.add(tuple(聲韻組[:2]))
				尾兩音.add(tuple(聲韻組[-2:]))
		for 頭前, 中央, 後壁 in [(頭一音, [()], 尾兩音),
					(頭兩音, [()], 尾一音),
					(頭一音, 家己一音, 尾一音)]:
			for 頭 in 頭前:
				for 中 in 中央:
					for 後 in 後壁:
						全部三連音.add(
							'{0}-{1}+{2}'.format(*(頭 + 中 + 後)))
		全部三連音檔 = os.path.join(資料目錄, '全部三連音.list')
		self.陣列寫入檔案(全部三連音檔, 全部三連音)
		設定 = """\
LT "{0}"
AU "{1}"
CO "{2}"
SH
""".format(三連音縛做伙樹檔, 全部三連音檔, 全部縛做伙檔)
		全部三連音設定檔 = os.path.join(資料目錄, '全部三連音設定.hed')
		self.字串寫入檔案(全部三連音設定檔, 設定)
		這馬模型有的聲韻表檔 = os.path.join(資料目錄, '這馬模型有的聲韻表.list')
		這馬模型有的聲韻表 = []
		for 聲韻 in self.讀檔案(原來縛做伙檔):
			if ' ' not in 聲韻:
				這馬模型有的聲韻表.append(聲韻)
		self.陣列寫入檔案(這馬模型有的聲韻表檔, 這馬模型有的聲韻表)
		縛做伙指令 = self.改模型指令.format(
			執行檔路徑, 原來模型, 全部模型檔, 全部三連音設定檔, 這馬模型有的聲韻表檔)
		self.走指令(縛做伙指令)
	def 加混合數(self, 執行檔路徑, 資料目錄,
			全部特徵檔, 聲韻類檔, 聲韻檔,
			原來模型, 混合數, 估幾擺=20, 上尾估幾擺=50):
		頂一个模型 = 原來模型
		for 擺, 混合 in enumerate(混合數):
			這擺資料夾 = os.path.join(資料目錄, '加混合數', '{0:02}'.format(擺))
			os.makedirs(這擺資料夾, exist_ok=True)
			設定檔 = os.path.join(這擺資料夾, '設定檔.hed')
			加混合模型 = os.path.join(這擺資料夾, '加混合模型.macro')
			self.陣列寫入檔案(設定檔, [
		 		"MU {0} {{*.state[2-4].mix}}".format(混合),
		 		"MU {0} {{{1}.state[2-4].mix}}".format(混合 * 2, self.恬音)])
			加混合數指令 = self.改模型指令.format(
				執行檔路徑, 頂一个模型, 加混合模型, 設定檔, 聲韻類檔)
			self.走指令(加混合數指令)
			頂一个模型 = self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔,
				聲韻類檔, 聲韻檔, 加混合模型, 估幾擺=估幾擺)
		加混合了模型 = os.path.join(資料目錄, '加混合了模型.macro')
		shutil.copy(頂一个模型, 加混合了模型)
		上尾模型檔 = self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔,
			聲韻類檔, 聲韻檔, 加混合了模型, 估幾擺=上尾估幾擺)
		return 上尾模型檔
	模型版參數 = \
'''
~o <VecSize> 39 <MFCC_E_D_A_Z> <DiagC> <StreamInfo> 1 39
<BeginHMM>
<NUMSTATES> 5
<STATE> 2
<NUMMIXES> 1 
<SWeights> 1 1 
<STREAM> 1
<MIXTURE> 1 1.000000e+000
<MEAN> 39
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
<VARIANCE> 39
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 \
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0

<STATE> 3
<NUMMIXES> 1 
<SWeights> 1 1 
<STREAM> 1
<MIXTURE> 1 1.000000e+000
<MEAN> 39
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
<VARIANCE> 39
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 \
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0

<STATE> 4
<NUMMIXES> 1 
<SWeights> 1 1 
<STREAM> 1
<MIXTURE> 1 1.000000e+000
<MEAN> 39
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
<VARIANCE> 39
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 \
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0

<TRANSP> 5
0.000000e+000 1.000000e+000 0.000000e+000 0.000000e+000 0.000000e+000 
0.000000e+000 6.000000e-001 4.000000e-001 0.000000e+000 0.000000e+000 
0.000000e+000 0.000000e+000 6.000000e-001 4.000000e-001 0.000000e+000 
0.000000e+000 0.000000e+000 0.000000e+000 6.000000e-001 4.000000e-001 
0.000000e+000 0.000000e+000 0.000000e+000 0.000000e+000 0.000000e+000 
<ENDHMM>
'''
	短恬參數 = \
'''
~h "{0}"
<BEGINHMM>
<NUMSTATES> 3
<STATE> 2
{1}
<TRANSP> 3
0.000000e+00 1.000000e+00 0.000000e+00
0.000000e+00 5.000000e-01 5.000000e-01
0.000000e+00 0.000000e+00 0.000000e+00
<ENDHMM>
'''
	改模型指令 = '{0}HHEd -A -H {1} -w {2} {3} {4}'
