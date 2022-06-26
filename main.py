# coding: utf-8
from crawler import Crawler
from web import openForum, postCover, postArticle,  getTid
from tkinter import messagebox, Tk, E
from tkinter.ttk import Label, Button, Entry, Frame

import configruation as config
from urllib.parse import urlparse


class PosterUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.forumDomain = "https://woodo.club/"
        self.driver = None
        self.pack()
        self.parent = parent
        self.parent.title('AutoPost')

        self.urlHint = Label(self, text='Source URL:', width=10, padding=3)
        self.urlHint.grid(row=0, column=0, columnspan=2)
        self.urlEntry = Entry(self, width=40)
        self.urlEntry.grid(row=0, column=2, columnspan=8)

        self.chapterHint = Label(
            self, text='Start chapter:', width=15, padding=3)
        self.chapterHint.grid(row=1, column=0, columnspan=3)
        self.chapterEntry = Entry(self, width=35)
        self.chapterEntry.grid(row=1, column=3, columnspan=7)

        self.accountHint = Label(self, text='Account:', width=10, padding=3)
        self.accountHint.grid(row=2, column=0, columnspan=2)
        self.accountEntry = Entry(self, width=40)
        self.accountEntry.grid(row=2, column=2, columnspan=8)

        self.passwordHint = Label(self, text='Password:', width=10, padding=3)
        self.passwordHint.grid(row=3, column=0, columnspan=2)
        self.passwordEntry = Entry(self, width=40)
        self.passwordEntry.grid(row=3, column=2, columnspan=8)

        self.fidHint = Label(self, text='fid:', width=10, padding=3)
        self.fidHint.grid(row=4, column=0, columnspan=2)
        self.fidEntry = Entry(self, width=40)
        self.fidEntry.grid(row=4, column=2, columnspan=8)

        self.subHint = Label(self, text='sub category:', width=15, padding=3)
        self.subHint.grid(row=5, column=0, columnspan=3)
        self.subEntry = Entry(self, width=35)
        self.subEntry.grid(row=5, column=3, columnspan=7)

        self.articleLinkHint = Label(
            self, text='article link:', width=15, padding=3)
        self.articleLinkHint.grid(row=6, column=0, columnspan=3)
        self.articleLinkEntry = Entry(self, width=35)
        self.articleLinkEntry.grid(row=6, column=3, columnspan=7)

        self.articleLinkDesc = Label(
            self, text='Keep empty if this is a new post', width=35, padding=3)
        self.articleLinkDesc.grid(row=7, column=3, columnspan=7)

        self.btn = Button(self, text='Go', command=self.clickBtn)
        self.btn.grid(row=8, column=0, columnspan=10, stick=E)

    def clickBtn(self):
        if not self.checkurl():
            messagebox.showerror('網址錯誤', '這不是八一中文, SF, 黃金屋, 輕小說文庫的網址')
            return
        elif not self.checkAccountPassword():
            messagebox.showerror('帳密錯誤', '是空的喔')
            return
        elif not self.checkFid():
            messagebox.showerror('fid錯誤', '會是純數字喔')
            return
        elif self.checkArticleLink():
            self.setValue()
            return
        elif not self.checkSubCategory():
            messagebox.showerror('sub category錯誤', '會是純數字喔')
            return
        self.setValue()

    def checkurl(self):
        # https://www.zwdu.com/book/32934/
        urlStr = self.urlEntry.get()
        support = ['zwdu.com', 'book.sfacg.com', 'hjwzw.com', 'wenku8.net',
                   'hetushu.com', 'hetubook.com', 'zssq.cc', 'czbooks.net', 'quanben.io', 'dingdianorg.com',
                   'uukanshu', 'wutuxs.com', '8book.com', 'bimidu.com', 'www.81book.com', 'www.81zw.com',
                   '230book.net']
        for s in support:
            if s in urlStr:
                return True
        return False

    def checkAccountPassword(self):
        _account = self.accountEntry.get()
        _password = self.passwordEntry.get()
        return _account != '' and _password != ''

    def checkFid(self):
        _fid = self.fidEntry.get()
        try:
            int(_fid)
            return True
        except ValueError:
            return False

    def checkSubCategory(self):
        _sub = self.subEntry.get()
        try:
            int(_sub)
            return True
        except ValueError:
            return False

    def checkArticleLink(self):
        _link = self.articleLinkEntry.get()
        return _link != ''

    def setValue(self):
        homeLink = self.urlEntry.get()
        account = self.accountEntry.get()
        password = self.passwordEntry.get()
        try:
            fid = int(self.fidEntry.get())
            subCategoryIdx = int(self.subEntry.get())
        except ValueError:
            subCategoryIdx = 0

        # 論壇的帖子連結, 如果不是續傳就保持 ''
        articleLink = self.articleLinkEntry.get()
        # 從 {{homeLink}} 的第某某章開始貼
        # 比方說 startChapterName = '第十六章 挖墙角', 去查然後直接複製貼上
        # 沒有指定從哪開始就保持 ""
        startChapterName = self.chapterEntry.get()
        self.btn.config(state="disabled")
        self.startWork(homeLink, startChapterName, account,
                       password, articleLink, fid, subCategoryIdx)

    def startWork(self, homeLink, startChapterName, account, password, articleLink, fid, subCategoryIdx):
        crawler = Crawler()
        soup, banner, title, author, state, desc = crawler.crawelHome(homeLink)
        hrefs = crawler.getArticleList(soup, startChapterName)
        if self.driver is None:
            self.driver = openForum(self.forumDomain, account, password)
        if articleLink == '':
            postLink = '{}forum.php?mod=post&action=newthread&fid={}'.format(
                self.forumDomain, fid)
            tid = postCover(self.driver, postLink, banner, title,
                            author, state, desc, subCategoryIdx)
            if tid.startswith('failed,'):
                self.unlockButton()
                return
            self.startPostChapter(crawler, self.driver, tid, hrefs, fid)
        else:
            tid = getTid(articleLink)
            self.startPostChapter(crawler, self.driver, tid, hrefs, fid)

    def startPostChapter(self, crawler, driver, tid, sourceHrefs, fid):
        postLink = '{}forum.php?mod=post&action=reply&fid={}&extra=&tid={}'.format(
            self.forumDomain, fid, tid)
        for href in sourceHrefs:
            content = crawler.crawelArticle(href)
            if len(content) < 400:
                # 請假章節
                self.unlockButton()
                break
            res = postArticle(driver, postLink, content)
            if res.startswith('failed,'):
                self.unlockButton()
                break
        self.unlockButton()

    def unlockButton(self):
        self.btn.config(state="normal")
        messagebox.showinfo('通知', '自動刊登暫停，更新完設定後請繼續')


def start():
    if verify_configuration() == False:
        return 
    start_crawling()

def verify_configuration() -> bool:
    if check_account() == False:
        return False
    if check_source() == False:
        return False
    if check_forum() == False:
        return False
    return True

def check_account() -> bool:
    account = config.account
    password = config.password
    if isinstance(account, str) == False or isinstance(password, str) == False:
        print('錯誤！ 帳號密碼是字串，範例: account = "test"')
        return False
    if len(account) == 0 or len(password) == 0:
        print('錯誤！ 請輸入帳號密碼')
        return False
    return True

def check_source() -> bool:
    novel_source = config.novel_source
    start_capter = config.start_capter
    if isinstance(novel_source, str) == False or isinstance(start_capter, str) == False:
        print('錯誤！ novel_source/ start_capter是字串，範例: start_capter = "https://abc.com"')
        return False

    parsed_source = urlparse(novel_source)
    parsed_chapter = urlparse(start_capter)
    support = config.support
    if parsed_source.hostname in support and parsed_chapter.hostname in support:
        return True
    print('錯誤！ 不支援的來源網址')
    return False

def check_forum() -> bool:
    fid = config.fid
    if isinstance(fid, int) == False:
        print('錯誤！ Fid 要是數字，範例 fid = 3')
        return False

    sub_category = config.sub_category
    if isinstance(sub_category, int) == False:
        print('錯誤！ sub_category 要是數字，範例 sub_category = 3')
        return False
    
    article_link = config.article_link
    if isinstance(article_link, str) == False:
        print('錯誤！ article_link 要是網址，範例 article_link = "https://abc.com"')
        return False
    parsed_article = urlparse(article_link)
    if parsed_article.hostname != 'woodo.club':
        print('錯誤！ article_link 不是 woodo 的')
        return False
    return True

def start_crawling():
    print('a')

if __name__ == '__main__':
    start()
    # root = Tk()
    # root.resizable(0, 0)
    # root.geometry("500x250")  # wxh
    # app = PosterUI(root)
    # app.mainloop()
