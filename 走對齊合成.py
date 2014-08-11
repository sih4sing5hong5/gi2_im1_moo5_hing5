import os
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 程式.對齊合成 import 對齊合成

if __name__ == '__main__':
	這馬目錄 = os.path.dirname(os.path.abspath(__file__))
	音檔目錄 = os.path.join(這馬目錄, 'wav')  # 音檔下的所在，先轉做wav檔
	拼音句檔名 = os.path.join(這馬目錄, 'label')  # 全部音檔的語句
	標仔拼音 = 臺灣客家話拼音  # 選「臺灣言語工具.音標系統」內的拼音
	HTK執行檔路徑 = 'HTK-3.4.1/bin'
	SPTK執行檔路徑 = 'SPTK-3.7/bin'
	HTS執行檔路徑 = 'HTS-2.3alpha/bin'
	HTS_ENGINE執行檔路徑 = 'hts_engine/bin'
	_對齊合成 = 對齊合成()
	_對齊合成.訓練合成模型(音檔目錄, 拼音句檔名, 標仔拼音,
		HTK執行檔路徑, SPTK執行檔路徑, HTS執行檔路徑, HTS_ENGINE執行檔路徑)
