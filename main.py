# coding: utf-8
from zwduCrawler import crawelHome, getArticleList, crawelArticle
from web import openForum, postCover, postArticle,  getTid
from tkinter import messagebox, Tk, LEFT, X, Text, RIGHT, END, E
from tkinter.ttk import Label, Button, Entry, Progressbar, Frame, Style
import tkinter.font as tkFont


class PosterUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.forumDomain = ""
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
            messagebox.showerror('網址錯誤', '這不是八一中文的網址')
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
        return urlStr.startswith('https://www.zwdu.com')

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

        soup, banner, title, author, state, desc = crawelHome(homeLink)
        hrefs = getArticleList(soup, startChapterName)
        driver = openForum(account, password)
        if articleLink == '':
            postLink = '{}forum.php?mod=post&action=newthread&fid={}'.format(
                self.forumDomain, fid)
            tid = postCover(driver, postLink, banner, title,
                            author, state, desc, subCategoryIdx)
            self.startPostChapter(driver, tid, hrefs, fid)
        else:
            tid = getTid(articleLink)
            self.startPostChapter(driver, tid, hrefs, fid)

    def startPostChapter(self, driver, tid, sourceHrefs, fid):
        postLink = '{}forum.php?mod=post&action=reply&fid={}&extra=&tid={}'.format(
            self.forumDomain, fid, tid)
        for href in sourceHrefs:
            content = crawelArticle(href)
            postArticle(driver, postLink, content)


if __name__ == '__main__':
    root = Tk()
    root.resizable(0, 0)
    root.geometry("400x200")  # wxh
    app = PosterUI(root)
    app.mainloop()