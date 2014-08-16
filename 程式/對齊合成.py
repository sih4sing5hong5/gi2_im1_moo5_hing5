import os
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 程式.對齊音檔時間 import 對齊音檔時間
from 程式.拼音句轉標仔檔 import 拼音句轉標仔檔
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.閩南語.通用拼音音標 import 通用拼音音標
from 臺灣言語工具.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標
from 臺灣言語工具.音標系統.閩南語.臺灣語言音標 import 臺灣語言音標
from 臺灣言語工具.語音辨識.腳本程式 import 腳本程式
from 臺灣言語工具.語音辨識.文本音值對照表.閩南語文本音值表 import 閩南語文本音值表
from 臺灣言語工具.語音辨識.文本音值對照表.客家話文本音值表 import 客家話文本音值表
import shutil
from 臺灣言語工具.語音合成.決策樹仔問題.閩南語決策樹仔 import 閩南語決策樹仔
from 臺灣言語工具.語音合成.決策樹仔問題.客家話決策樹仔 import 客家話決策樹仔
import wave
from 臺灣言語工具.語音合成.音檔頭前表 import 音檔頭前表
from 臺灣言語工具.音標系統.官話.官話注音符號 import 官話注音符號
from 臺灣言語工具.語音辨識.文本音值對照表.官話文本音值表 import 官話文本音值表
from 臺灣言語工具.語音合成.決策樹仔問題.官話決策樹仔 import 官話決策樹仔

class 對齊合成(腳本程式):
	def 訓練合成模型(self, 音檔目錄, 拼音句檔名, 標仔拼音,
			HTK執行檔路徑, SPTK執行檔路徑, HTS執行檔路徑, HTS_ENGINE執行檔路徑):
		專案目錄 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		print('判斷用的語言')
		if 標仔拼音 in [臺灣閩南語羅馬字拼音, 通用拼音音標, 教會羅馬字音標, 臺灣語言音標]:
			語言拼音 = 臺灣閩南語羅馬字拼音
			文本音值表 = 閩南語文本音值表()
			決策樹仔 = 閩南語決策樹仔()
		elif 標仔拼音 in [臺灣客家話拼音]:
			語言拼音 = 臺灣客家話拼音
			文本音值表 = 客家話文本音值表()
			決策樹仔 = 客家話決策樹仔()
		elif 標仔拼音 in [官話注音符號]:
			語言拼音 = 官話注音符號
			文本音值表 = 官話文本音值表()
			決策樹仔 = 官話決策樹仔()
		else:
			raise RuntimeError('拼音無佇工具內底')
		
		print('共拼音句轉做HTK愛的樣')
		_拼音句轉標仔檔 = 拼音句轉標仔檔()
		原始標仔資料夾 = self.細項目錄(專案目錄, '原始標仔')
		完整標仔夾, 主要標仔夾 = _拼音句轉標仔檔.轉(標仔拼音, 語言拼音, 拼音句檔名, 原始標仔資料夾)
		
		print('用HTK標語料的時間')
		_對齊音檔時間 = 對齊音檔時間()
		辨識資料 = self.細項目錄(專案目錄, '辨識資料')
		音節聲韻對照檔 = os.path.join(專案目錄, '聲韻對照檔.dict')
		self.陣列寫入檔案(音節聲韻對照檔, 文本音值表.聲韻表())
		對齊的主要音值資料夾 = _對齊音檔時間.對齊(辨識資料, 音檔目錄, 主要標仔夾, 音節聲韻對照檔, HTK執行檔路徑)
		
		print('準備HTS需要的物件')
		HTS資料目錄 = self.細項目錄(專案目錄, 'data')
		print('	1.HTS愛標仔')
		HTS標仔目錄 = self.細項目錄(HTS資料目錄, 'labels')
		HTS音值標仔目錄 = os.path.join(HTS標仔目錄, 'mono')
		HTS完整標仔目錄 = os.path.join(HTS標仔目錄, 'full')
		for 來源, 目標 in [(對齊的主要音值資料夾, HTS音值標仔目錄), (完整標仔夾, HTS完整標仔目錄)]:
			if os.path.exists(目標):
				shutil.rmtree(目標)
			shutil.copytree(來源, 目標)
		HTS試驗標仔目錄 = self.細項目錄(HTS標仔目錄, 'gen')
		for 檔名 in os.listdir(HTS完整標仔目錄)[:10]:
			來源完整標仔 = os.path.join(HTS完整標仔目錄, 檔名)
			目標完整標仔 = os.path.join(HTS試驗標仔目錄, 檔名)
			shutil.copy(來源完整標仔, 目標完整標仔)
		print('	2.HTS愛分類標仔，所以愛決策樹仔的問題')
		問題 = 決策樹仔.生()
		HTS問題目錄 = self.細項目錄(HTS資料目錄, 'questions')
		HTS問題檔案 = os.path.join(HTS問題目錄, 'questions_qst001.hed')
		self.陣列寫入檔案(HTS問題檔案, 問題)
		print('	3.HTS愛無檔頭的音標，所以愛提掉檔頭')
		檔頭前表 = 音檔頭前表()
		HTS原始檔目錄 = self.細項目錄(HTS資料目錄, 'raw')
		頻率 = None
		for 檔名 in os.listdir(音檔目錄):
			if 檔名.endswith('wav'):
				音檔檔名 = os.path.join(音檔目錄, 檔名)
				音檔 = open(音檔檔名, 'rb')
				原始檔 = open(os.path.join(HTS原始檔目錄, 檔名[:-4] + '.raw'), 'wb')
				原始檔.write(檔頭前表.提掉(音檔.read()))
				音檔.close()
				原始檔.close()
				with wave.open(音檔檔名, mode='rb') as 音物件:
					if 音物件.getnchannels() != 1 or 音物件.getsampwidth() != 2:
						raise RuntimeError('音標愛單聲道，逐的點愛兩位元組的整數')
					if 頻率 == None:
						頻率 = 音物件.getframerate()
					elif 頻率 != 音物件.getframerate():
						raise('音檔的取樣頻率愛仝款！！有{0}佮{1}Hz'.format(
							頻率, 音物件.getframerate()))
		
		'走HTS'
		音框長度 = 頻率 // 40
		音框移動 = 音框長度 // 5
		if 頻率 < 20000:
			參數量 = 24
		else:
			參數量 = 40
		HTS設定指令 = '''LANG=c ./configure --with-sptk-search-path={0} \
--with-hts-search-path={1} \
--with-hts-engine-search-path={2} \
LOWERF0=60 UPPERF0=500 SAMPFREQ={3} FRAMELEN={4} FRAMESHIFT={5} \
GAMMA=3 LNGAIN=1 MGCORDER={6} USEGV=0'''\
			.format(SPTK執行檔路徑, HTS執行檔路徑, HTS_ENGINE執行檔路徑,
				頻率, 音框長度, 音框移動, 參數量)
		self.走指令(HTS設定指令)
		HTS走指令 = 'LANG=c make all'
		self.走指令(HTS走指令)
