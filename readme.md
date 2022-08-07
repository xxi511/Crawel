# 爬蟲

## How to use 
Open `config.json` 
fill in all of data
```
"account": 帳號
"password": 密碼
"novel_source": 小說首頁
"start_capter": 小說起始章節
"fid": 小說區塊 fid
"sub_category": 發文分類，新書才需要
"article_link": 論壇小說網址
```

## support sites 
Check `Novel_Crawler/helpers.py`

## pyinstaller

```
$ pyinstaller -F -n AutoPost -w main.py
```

將 `config/`, `dictionary/`, `driver/`, `data.txt` , `regex.txt`複製到 `dist/` 中

## 3-rd

`python 3`

```
$ pip install beautifulsoup4
$ pip install selenium
```

有使用 [opencc-python-reimplemented](https://pypi.org/project/opencc-python-reimplemented/)
但使用 `pyinstaller` 在檔案讀取上會失敗
所以直接將原始碼複製進來，修改檔案讀取的路徑
