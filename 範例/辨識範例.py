import os
from 臺灣言語工具.語音辨識.模型訓練 import 模型訓練
from 臺灣言語工具.語音辨識.辨識模型 import 辨識模型

if __name__ == '__main__':
	訓練 = 模型訓練()
	這馬目錄 = os.path.dirname(os.path.abspath(__file__))
	資料目錄 = os.path.join(這馬目錄, 'data')
	音檔目錄 = os.path.join(這馬目錄, 'wav')
	標仔目錄 = os.path.join(這馬目錄, 'labels')
	音節聲韻對照檔 = os.path.join(這馬目錄, 'Syl2Monophone.dic.ok')
	執行檔路徑 = ''
	(原本聲韻類檔, 原本模型檔),\
	(加短恬聲韻類檔, 加短恬模型檔),\
	(三連音聲韻類檔, 三連音模型檔),\
	(全部特徵檔, 原來聲韻檔, 新拄好短恬聲韻檔) = 訓練.訓練(
		音檔目錄, 標仔目錄, 音節聲韻對照檔, 資料目錄,
		執行檔路徑=執行檔路徑)
	
	模型 = 辨識模型()
	
	原本目錄 = os.path.join(資料目錄, '原本')
	os.makedirs(原本目錄, exist_ok=True)
	對齊聲韻結果檔 = 模型.對齊聲韻(原本聲韻類檔, 原本模型檔, 原來聲韻檔, 全部特徵檔, 原本目錄, 執行檔路徑=執行檔路徑)
	
	加短恬目錄 = os.path.join(資料目錄, '加短恬')
	os.makedirs(加短恬目錄, exist_ok=True)
	對齊聲韻結果檔 = 模型.對齊聲韻(加短恬聲韻類檔, 加短恬模型檔, 新拄好短恬聲韻檔, 全部特徵檔, 加短恬目錄, 執行檔路徑=執行檔路徑)
