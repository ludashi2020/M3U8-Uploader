import os
import random
import time
import re
import json
import shutil
import requests
import threading

from loguru import logger
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode, b64encode
from urllib.parse import urljoin, unquote
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()
prefix = b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7".encode())
prefixsize = len(prefix)
lock = threading.Lock()


def request_get(url, headers, session=requests):
    for i in range(3):
        try:
            with session.get(url=url, headers=headers) as resp:
                resp.raise_for_status()
                content = resp.content
                return content
        except Exception as e:
            logger.warning(f"Get出错 {url} 报错内容 {e}")
            time.sleep(2)

    raise Exception(f"{url} 请求失败")


def upload1(filename, fdata):
    file = prefix + fdata
    url = "https://pic.2xb.cn/uppic.php?type=qq"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    data = {"file": (f"{int(time.time())}.gif", file, "image/gif")}
    for i in range(3):
        try:
            with requests.post(url=url, headers=headers, files=data) as resp:
                data = resp.json()
            return data["url"]
        except Exception as e:
            logger.warning(f"上传TS请求出错 {e}")
            time.sleep(2)

    raise Exception(f"{filename} TS 上传失败")


def upload2(filename, fdata):
    url = "https://api.vviptuangou.com/api/upload"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Sign': 'e346dedcb06bace9cd7ccc6688dd7ca1',
        'Token': 'b3bc3a220db6317d4a08284c6119d136',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    file = prefix + fdata  # size < 50MB
    data = {"file": (f"{int(time.time())}.gif", file, "image/gif")}
    for i in range(3):
        try:
            with requests.post(url=url, headers=headers, files=data) as resp:
                data = resp.json()
            return f"https://assets.vviptuangou.com/{data['imgurl']}"
        except Exception as e:
            logger.warning(f"上传TS请求出错 {e}")
            time.sleep(2)
    raise Exception(f"{filename} TS 上传失败")

def upload3(filename, fdata):
    url = "https://api.da8m.cn/api/upload"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Sign': 'e346dedcb06bace9cd7ccc6688dd7ca1',
        'Token': '4ca04a3ff8ca3b8f0f8cfa01899ddf8e',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    file = prefix + fdata  # size < 50MB
    data = {"file": (f"{int(time.time())}.gif", file, "image/gif")}
    for i in range(3):
        try:
            with requests.post(url=url, headers=headers, files=data) as resp:
                data = resp.json()
            return f"https://assets.da8m.cn/{data['imgurl']}"
        except Exception as e:
            logger.warning(f"上传TS请求出错 {e}")
            time.sleep(2)
    raise Exception(f"{filename} TS 上传失败")


def upload4(filename, fdata):
    url = "https://api.qst8.cn/api/front/upload/img"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Branchid': '1002',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sign': 'e346dedcb06bace9cd7ccc6688dd7ca1',
        'Source': 'h5',
        'Tenantid': '3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    file = prefix + fdata  # size < 5MB
    data = {"file": (f"{int(time.time())}.gif", file, "image/gif")}
    for i in range(3):
        try:
            with requests.post(url=url, headers=headers, files=data) as resp:
                return resp.json()['data']
        except Exception as e:
            logger.warning(f"上传TS请求出错 {e}")
            time.sleep(2)
    raise Exception(f"{filename} TS 上传失败")

def upload5(filename, fdata):
    file = prefix + fdata
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
    }
    data = {
        'reqtype': 'fileupload',
        'userhash': '',
        'fileToUpload': (filename, file, "image/gif")
    }
    for i in range(3):
        try:
            with requests.post(f'https://catbox.moe/user/api.php?request_type=upload', headers=headers, data=data) as resp:
                return resp.text
        except Exception as e:
            logger.warning(f"上传TS请求出错 {e}")
            time.sleep(2)
    raise Exception(f"{filename} TS 上传失败")


def upload6(filename, fdata):
    file = prefix + fdata
    data = {
        'file': (filename, file, "image/gif")
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
    }
    for i in range(3):
        try:
            with requests.post(f'https://icfruit.cn/api/fileupload', headers=headers, data=data) as resp:
                return resp.json()["data"]
        except Exception as e:
            logger.warning(f"上传TS请求出错 {e}")
            time.sleep(2)
    raise Exception(f"{filename} TS 上传失败")


class Down:
    def __init__(self, filename=None, m3u8link=None):
        self.session = requests.session()
        self.vinfo = {
            "filename": filename,
            "m3u8link": m3u8link,
            "key": b"",
            "iv": b"",
            "ts": [],
        }
        self.upload_s3 = [upload1, upload2, upload3, upload4, upload5, upload6]

    def load_m3u8(self, url=None):
        m3u8link = url or self.vinfo["m3u8link"]
        self.vinfo["m3u8link"] = m3u8link
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
        }
        logger.info(f'M3U8 Downloading {m3u8link}')
        self.vinfo["filename"] = os.path.basename(m3u8link).split("?")[0].split(".m3u8")[0]
        content = request_get(m3u8link, headers, self.session).decode()
        _content = content.split("\n").__iter__()
        while True:
            try:
                _ = _content.__next__()
                if "#EXTINF" in _:
                    while True:
                        _2 = _content.__next__()
                        if not _2 or _2.startswith("#"):
                            continue
                        else:
                            self.vinfo["ts"].append(urljoin(m3u8link, _2))
                            break
            except StopIteration:
                break
        del _content
        keyurl = (re.findall(r"URI=\"(.*)\"", content) or [''])[0]
        if keyurl:
            iv = bytes.fromhex((re.findall(r"IV=(.*)", content) or ['12'])[0][2:])
            self.vinfo["iv"] = iv or b'\x00' * 16
            logger.info(f'IV {iv}')
            keyurl = keyurl if keyurl.startswith("http") else urljoin(m3u8link, keyurl)
            logger.info(f'KEY Downloading {keyurl}')
            self.vinfo["key"] = request_get(keyurl, dict(headers, **{"Host": keyurl.split("/")[2]}), self.session)
        if not os.path.exists(self.vinfo['filename']):
            os.makedirs(self.vinfo['filename'], exist_ok=True)
        logger.info("保存raw.m3u8到本地")
        with open(f'{self.vinfo["filename"]}/raw.m3u8', "w") as fp:
            fp.write(content)
        logger.info("保存meta.json到本地")
        with open(f'{self.vinfo["filename"]}/meta.json', "w") as fp:
            fp.write(json.dumps(dict(self.vinfo, **{
                "key": self.vinfo["key"].hex(),
                "iv": self.vinfo["iv"].hex()
            })))

    def load_ts(self, index, handle):
        ts_url = self.vinfo["ts"][int(index)]
        if not ts_url.startswith('http'):
            ts_url = urljoin(self.vinfo["m3u8link"], ts_url)
        headers = {
            "Host": ts_url.split("/")[2],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        }
        logger.info(f'TS{index} Downloading')
        content = request_get(ts_url, headers, self.session)  # 下载ts
        decrypted_ts = self.decrypt_ts(content)  # 解密
        filesize = len(decrypted_ts)
        logger.info(f'TS{index} Saving to URL')
        s3_ts_url = random.choice(self.upload_s3)(f"{index}.ts", decrypted_ts)  # 上传 + 负载均衡
        with lock:
            handle.write(f"{index}@@{filesize}@@{s3_ts_url}\n")  # 写入记录
        return index

    def decrypt_ts(self, ts_data):
        if not self.vinfo["key"]:
            return ts_data

        cipher = AES.new(self.vinfo["key"], AES.MODE_CBC, iv=self.vinfo["iv"])
        decrypted_data = unpad(cipher.decrypt(ts_data), AES.block_size)
        return decrypted_data

    def save_m3u8(self):
        with open(f'{self.vinfo["filename"]}/raw.m3u8', "r") as fp:
            m3u8_text = fp.read()
        with open(f'{self.vinfo["filename"]}/temp', "r") as fp:
            data = {}
            for i in fp.read().strip("\n").split("\n"):
                index, filesize, url = i.split("@@")
                data[index] = [index, filesize, url]

        duration = (re.findall(r"EXT-X-TARGETDURATION:(\d+)", m3u8_text) or ["5"])[0]
        extinf = re.findall(r"#EXTINF:.*,", m3u8_text)

        m3u8_list = ['#EXTM3U', '#EXT-X-VERSION:4', '#EXT-X-MEDIA-SEQUENCE:0', '#EXT-X-ALLOW-CACHE:YES',
                     '#EXT-X-TARGETDURATION:%s']
        m3u8_list[4] = m3u8_list[4] % duration
        for i in range(len(data)):
            _, filesize, url = data[f"{i:04}"]
            n = int(filesize) - prefixsize
            o = prefixsize
            m3u8_list.append(extinf[i])
            m3u8_list.append(f"#EXT-X-BYTERANGE:{n}@{o}")
            m3u8_list.append(url)
        m3u8_list.append("#EXT-X-ENDLIST")
        with open(f'{self.vinfo["filename"]}/new_raw.m3u8', "wb") as fp:
            content = "\n".join(m3u8_list).encode()
            fp.write(content)


def main():
    workers = 10
    down = Down()
    logger.info("开始运行")

    m3u8_url = "https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8"
    down.load_m3u8(m3u8_url)
    if os.path.exists(f"{down.vinfo['filename']}/temp"):
        with open(f"{down.vinfo['filename']}/temp", "r") as fp:
            local_files = fp.read().strip("\n").split("\n")
            local_files = [i.split("@@")[0] for i in local_files]
    else:
        local_files = []
    local_files = [i for i in range(len(down.vinfo["ts"])) if f"{i:04}" not in local_files]  # m3u8分片
    with open(f'{down.vinfo["filename"]}/temp', "a", encoding='utf-8') as handle:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(down.load_ts, f"{index:04}", handle): index for index in local_files}
            for future in futures:
                future.result()
            handle.flush()

    logger.info(f"{down.vinfo['filename']} 下载完成")
    down.save_m3u8()
    # shutil.rmtree(down.vinfo["filename"])
    print("任务完成")


if __name__ == '__main__':
    main()
