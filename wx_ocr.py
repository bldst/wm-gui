from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID
#后面改成在配置文件中读取相关路径
wechat_ocr_dir = "C:\\Users\\cc\\AppData\\Roaming\\Tencent\\WeChat\\XPlugin\\Plugins\\WeChatOCR\\7071\\extracted\\WeChatOCR.exe"
wechat_dir = "C:\\Program Files\\Tencent\\WeChat\\[3.9.9.43]"


class WxOcr:
    def __init__(self, img_path):
        self.img_path = img_path
        self.results = []

    def ocr_result_callback(self,img_path,results: dict):
        self.results = results['ocrResult']

    def main(self):
        ocr_manager = OcrManager(wechat_dir)
        # 设置WeChatOcr目录
        ocr_manager.SetExePath(wechat_ocr_dir)
        # 设置微信所在路径
        ocr_manager.SetUsrLibDir(wechat_dir)
        # 设置ocr识别结果的回调函数
        ocr_manager.SetOcrResultCallback(self.ocr_result_callback)
        # 启动ocr服务
        ocr_manager.StartWeChatOCR()
        # 开始识别图片
        ocr_manager.DoOCRTask(rf"{self.img_path}")

        #time.sleep(1)
        while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
            pass
        # 识别输出结果
        ocr_manager.KillWeChatOCR()
