import os
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.語音合成.句物件轉合成標仔 import 句物件轉合成標仔
from 臺灣言語工具.語音辨識.腳本程式 import 腳本程式
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私

class 拼音句轉標仔檔(腳本程式):
	隔開符號 = '///'
	_粗胚 = 文章粗胚()
	_分析器 = 拆文分析器()
	_家私 = 轉物件音家私()
	_轉合成標仔 = 句物件轉合成標仔()
	def 轉(self, 拼音, 拼音句檔名, 標仔資料夾):
		os.makedirs(標仔資料夾, exist_ok=True)
		完整標仔夾 = self.細項目錄(標仔資料夾, '完整標仔')
		主要標仔夾 = self.細項目錄(標仔資料夾, '主要標仔')
		for 一句 in self.讀檔案(拼音句檔名):
			try:
				音檔名, 拼音句 = 一句.rstrip().split(self.隔開符號)
			except:
				raise RuntimeError('格式愛：音檔名///拼音句')
			if 音檔名.endswith('.wav'):
				音檔名 = 音檔名[:-4]
			處理減號 = self._粗胚.建立物件語句前減號變標點符號(拼音, 拼音句)
			try:
				句物件 = self._分析器.產生對齊句(處理減號, 處理減號)
			except:
				raise RuntimeError('語句分析器有問題，請共問題回報到：\
https://github.com/sih4sing5hong5/tai5_uan5_gian5_gi2_kang1_ku7/issues')
			try:
				標準句物件 = self._家私.轉音(拼音, 句物件)
			except:
				raise RuntimeError('有拼音無合法')
			完整標仔 = self._轉合成標仔.句物件轉標仔(標準句物件, 加短恬=False)
			完整標仔檔名 = os.path.join(完整標仔夾, 音檔名 + '.lab')
			self.陣列寫入檔案(完整標仔檔名, 完整標仔)
			主要標仔 = self._轉合成標仔.提出標仔主要音值(完整標仔)
			主要標仔檔名 = os.path.join(主要標仔夾, 音檔名 + '.lab')
			self.陣列寫入檔案(主要標仔檔名, 主要標仔)
		return 完整標仔夾, 主要標仔夾
