import threading
import requests

class Download:
    def download(self, url: str, callback_word_count):
        """
        download函数
        每次执行完都会调用 callback_word_count 回调函数
        """
        print(f"线程：{threading.get_ident()} 开始下载：{url}")
        response = requests.get(url)
        response.encoding = 'utf-8'

        callback_word_count(url, response.text) # 调用回调函数
    
    def start_download(self, url, callback_word_count):
        # self.download(url, callback_word_count) # 同步下载，仅在单线程下执行
        """
        创建一个线程对象（即新建一个线程，开始使用该线程）
        target：指定目标调用函数
        args：调用函数的参数
        """
        thread = threading.Thread(target=self.download, args=(url, callback_word_count))
        thread.start()

def word_count(url, result):
    """
    普通函数，用于回调
    """
    print(f"{url}:{len(result)}->{result[:5]}")

def main():
    download = Download()
    download.start_download('http://localhost:8000/novel1.txt', word_count)
    download.start_download('http://localhost:8000/novel2.txt', word_count)
    download.start_download('http://localhost:8000/novel3.txt', word_count)