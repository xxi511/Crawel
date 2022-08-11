# coding: utf-8
from crawler import Crawler
from configruation import Config
from forum import Forum

class App:
    def __init__(self) -> None:
        self.config = Config()
        self.forum = Forum()
        self.crawler = Crawler()

    def start(self):
        if self.config.verify_configuration() == False:
            return
        if self.forum.prepare_driver() == False:
            print('Chrome driver 錯誤，請檢察')
            return
        self.forum.login(self.config.account, self.config.password)
        self.start_crawling()

    def start_crawling(self):
        soup, banner, title, author, state, desc = self.crawler.crawelHome(self.config.novel_source)
        hrefs = self.crawler.getArticleList(soup, self.config.start_capter)
        if self.config.article_link == '':
            postLink = 'https://woodo.club/forum.php?mod=post&action=newthread&fid={}'.format(
                self.config.fid)
            tid = self.forum.postCover(postLink, banner, title,
                                        author, state, desc, self.config.sub_category)
            if tid.startswith('failed,'):
                return
            self.startPostChapter(tid, hrefs, self.config.fid)
        else:
            tid = self.forum.getTid(self.config.article_link)
            self.startPostChapter(tid, hrefs, self.config.fid)

    def startPostChapter(self, tid, sourceHrefs, fid):
        postLink = 'https://woodo.club/forum.php?mod=post&action=reply&fid={}&extra=&tid={}'.format(
            fid, tid)
        for href in sourceHrefs:
            content = self.crawler.crawelArticle(href)
            if len(content) < 400:
                # 請假章節
                break
            res = self.forum.postArticle(postLink, content)
            if res.startswith('failed,'):
                break

if __name__ == '__main__':
    app = App()
    app.start()
