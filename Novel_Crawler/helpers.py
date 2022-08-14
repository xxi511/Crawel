from enum import Enum
import requests
from bs4 import BeautifulSoup


class Encoding(Enum):
    gbk = "gbk"
    big5 = "Big5"
    utf8 = "UTF-8"

class Support(Enum):
    unknown = 'unknown'
    sixnineshu = 'www.69shu.com'
    b520 = 'www.b520.cc'
    bimidu = 'www.bimidu.com'
    book8 = '8book.com'
    cnuu = 'cn.uukanshu.cc'
    czbook = 'czbooks.net'
    hetu = 'hetushu.com'
    hj = 'tw.hjwzw.com'
    pt = 'www.ptwxz.com'
    quanben = 'www.quanben.io'
    sf = 'book.sfacg.com'
    uu = 'tw.uukanshu.com'
    wenku = 'www.wenku8.net'
    wutuxs = 'www.wutuxs.com'
    zwdu = 'www.81book.com'

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str) == False:
            return Support.unknown

        for host in supports:
            if host.value in value:
                return host
        return Support.unknown

supports = [
                Support.sixnineshu,
                Support.b520, Support.bimidu, Support.book8, 
                Support.cnuu, Support.czbook, 
                Support.hetu, Support.hj,
                Support.pt, Support.quanben, Support.sf, Support.uu, Support.wenku, Support.wutuxs, 
                Support.zwdu
            ]

def getSoup(link: str, encoding: Encoding) -> BeautifulSoup:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    resp = requests.get(link, headers=headers, verify=False)
    resp.encoding = encoding.value
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


if __name__ == "__main__":
    a = Encoding.big5.value
    k = Support('https://tw.hjwzw.com/Book/33924')
    print(a)
