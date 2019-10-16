# 爬蟲

## pyinstaller

```
$ pyinstaller -F -n AutoPost -w main.py
```

將 `config/`, `dictionary/`, `driver/`, `data.txt` 複製到 `dist/` 中

## Chrome driver

目前 `mac`, `win` 是使用 `chrome 77`
`linux` 是 `chrome 74`

## 3-rd

`python 3`

```
$ pip install beautifulsoup4
$ pip install selenium
```

有使用 [opencc-python-reimplemented](https://pypi.org/project/opencc-python-reimplemented/)
但使用 `pyinstaller` 在檔案讀取上會失敗
所以直接將原始碼複製進來，修改檔案讀取的路徑
