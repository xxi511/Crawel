from urllib.parse import urlparse
import json

class Config:
    def __init__(self) -> None:
        with open('./config.json', 'r') as f:
            dict = json.load(f)
            self.account = dict['account']
            self.password = dict['password']
            self.novel_source = dict['novel_source']
            self.start_capter = dict['start_capter']
            self.fid = dict['fid']
            self.sub_category = dict['sub_category']
            self.article_link = dict['article_link']

        self.support = [
                'zwdu.com', 'book.sfacg.com', 'tw.hjwzw.com', 'hjwzw.com', 'wenku8.net',
                'hetushu.com', 'hetubook.com', 'zssq.cc', 'czbooks.net', 'quanben.io', 'dingdianorg.com',
                'uukanshu', 'wutuxs.com', '8book.com', 'bimidu.com', 'www.81book.com', 'www.81zw.com',
                '230book.net'
            ]

    def verify_configuration(self) -> bool:
        if self.check_account_config() == False:
            return False
        if self.check_source_config() == False:
            return False
        if self.check_forum_config() == False:
            return False
        return True

    def check_account_config(self) -> bool:
        account = self.account
        password = self.password
        if isinstance(account, str) == False or isinstance(password, str) == False:
            print('錯誤！ 帳號密碼是字串，範例: "account": "test"')
            return False
        if len(account) == 0 or len(password) == 0:
            print('錯誤！ 請輸入帳號密碼')
            return False
        return True

    def check_source_config(self) -> bool:
        novel_source = self.novel_source
        start_capter = self.start_capter
        if isinstance(novel_source, str) == False or isinstance(start_capter, str) == False:
            print('錯誤！ novel_source/ start_capter是字串，範例: "start_capter": "https://abc.com"')
            return False

        parsed_source = urlparse(novel_source)
        parsed_chapter = urlparse(start_capter)
        support = self.support
        if parsed_source.hostname in support and parsed_chapter.hostname in support:
            return True
        print('錯誤！ 不支援的來源網址')
        return False

    def check_forum_config(self) -> bool:
        fid = self.fid
        if isinstance(fid, int) == False:
            print('錯誤！ Fid 要是數字，範例 "fid": 3')
            return False

        sub_category = self.sub_category
        if isinstance(sub_category, int) == False:
            print('錯誤！ sub_category 要是數字，範例 "sub_category": 3')
            return False
        
        article_link = self.article_link
        if isinstance(article_link, str) == False:
            print('錯誤！ article_link 要是網址，範例 "article_link": "https://abc.com"')
            return False
        parsed_article = urlparse(article_link)
        if 'woodo.club' not in parsed_article.hostname:
            print('錯誤！ article_link 不是 woodo 的')
            return False
        return True