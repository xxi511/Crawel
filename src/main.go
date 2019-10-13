package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/chromedp/chromedp"
)

var browser context.Context
var domain = "https://czbooks.net/c/xuanhuan"
var forumDomain = ""
var fid = ""
var account = ""
var password = ""

var postRecord = []string{}
var recordFile *os.File

func main() {
	initPostRecord()
	login()
}

func initPostRecord() {
	file, err := os.Open("record.txt")
	if err != nil {
		log.Fatal("Load record.txt failed")
	}
	defer file.Close()

	binary, err := ioutil.ReadAll(file)
	if err != nil {
		log.Fatal("Read record.txt failed")
	}

	data := string(binary)
	split := strings.Split(data, "\n")
	postRecord = append(postRecord, split[:len(split)-1]...)
	fmt.Println(split)
}

func login() {
	ctx := context.Background()
	options := []chromedp.ExecAllocatorOption{
		chromedp.Flag("headless", false),
		chromedp.Flag("hide-scrollbars", false),
		chromedp.Flag("mute-audio", false),
		chromedp.UserAgent(`Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36`),
	}

	options = append(chromedp.DefaultExecAllocatorOptions[:], options...)

	c, cc := chromedp.NewExecAllocator(ctx, options...)
	defer cc()

	ctx, cancel := chromedp.NewContext(c)
	defer cancel()

	err := chromedp.Run(ctx,
		chromedp.Navigate(forumDomain),
		chromedp.WaitVisible(`#lsform`),
		chromedp.SendKeys("#ls_username", account),
		chromedp.SendKeys("#ls_password", password),
		chromedp.Click("#lsform td.fastlg_l button", chromedp.NodeVisible),
		chromedp.WaitVisible("div.avt.y"),
	)

	if err != nil {
		log.Fatal(err)
	}
	browser = ctx

	startCrawel(1)
}

func startCrawel(page int) {
	fmt.Println("Crawel page: " + strconv.Itoa(page))
	novels, nextCheck := getList(domain, page)
	crawelNovel(novels)

	if nextCheck == 2 && page < 1500 {
		startCrawel(page + 1)
	}
}

func crawelNovel(novels []Novel_meta) {
	for _, novel := range novels {
		getNovelContent(novel)
	}
}

// GetList return novels meta data and next page check
func getList(domain string, page int) (novels []Novel_meta, nextCheck int) {
	resp, err := http.Get(domain + "/" + strconv.Itoa(page))
	if err != nil {
		log.Fatal(err)
		return
	}
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatal(err)
		return
	}

	novels = []Novel_meta{}
	selector := "ul.nav.novel-list.style-default li div.novel-item"
	doc.Find(selector).Each(func(i int, s *goquery.Selection) {

		cover_div := s.Find("div.novel-item-cover-wrapper")
		link, _ := cover_div.Find("a").Attr("href")
		link = "https:" + link
		banner, _ := cover_div.Find("img").Attr("src")
		title := strings.TrimSpace(s.Find("div.novel-item-title").Text())
		author := strings.TrimSpace(s.Find("div.novel-item-author").Text())
		author = strings.Split(author, " ")[1]

		meta := Novel_meta{title, author, link, banner}

		novels = append(novels, meta)
	})

	// 0: initialize status
	// 1: get activate li
	// 2: has next page
	nextCheck = 0
	doc.Find("ul.nav.paginate li").Each(func(i int, s *goquery.Selection) {
		if s.HasClass("active") {
			nextCheck = 1
		} else if nextCheck == 1 {
			nextCheck = 2
		}
	})
	return
}

func getNovelContent(meta Novel_meta) {
	if isPostBefore(meta.name) {
		return
	}
	fmt.Println("Crawel novel: " + meta.name)
	resp, err := http.Get(meta.link)
	if err != nil {
		log.Fatal(err)
		return
	}
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatal(err)
		return
	}
	postNovelDescription(doc, meta)
}

func isPostBefore(name string) bool {
	if Contains(name, postRecord) {
		return true
	} else {
		appendToFile(name)
		return false
	}
}

func appendToFile(name string) {
	if recordFile == nil {
		file, _ := os.OpenFile("record.txt", os.O_APPEND|os.O_RDWR, os.ModeAppend)
		recordFile = file
	}

	_, err := recordFile.WriteString(name + "\n")
	if err != nil {
		log.Fatal("write failed ", err)
	}
	recordFile.Sync()
}

func postNovelDescription(doc *goquery.Document, meta Novel_meta) {

	state := "(連載中)"
	stateText := doc.Find("div.novel-detail div.state table tbody tr td").Text()
	if strings.Contains(stateText, "已完結") {
		state = "(已完結)"
	}
	title := meta.name + " 作者：" + meta.author + state

	descText := doc.Find("div.novel-detail div.description").Text()
	trimed := Formate(descText)
	trimed = "[img]" + meta.banner + "[/img]\n" + trimed

	postLink := forumDomain + "forum.php?mod=post&action=newthread&fid=" + fid
	var res string
	err := chromedp.Run(browser,
		chromedp.Navigate(postLink),
		chromedp.WaitVisible(`#subject`),
		chromedp.Click("#e_simple", chromedp.NodeVisible),
		chromedp.Click("#e_switchercheck", chromedp.NodeVisible),
		chromedp.SendKeys("#subject", title),
		chromedp.SetValue("#e_textarea", trimed),
		chromedp.Click("#postsubmit", chromedp.NodeVisible),
		chromedp.WaitVisible("#postlist"),
		chromedp.Evaluate(`window.location.href;`, &res),
	)
	if err != nil {
		log.Fatal("post novel failed", err)
	}

	r, _ := regexp.Compile("tid=[0-9]+")
	tid := strings.Split(r.FindString(res), "=")[1]
	GetChapterList(doc, tid)
}

func GetChapterList(root *goquery.Document, tid string) {
	root.Find("ul.nav.chapter-list li a").Each(func(i int, s *goquery.Selection) {
		postChapter(s, tid)
	})
}

func postChapter(s *goquery.Selection, tid string) {
	time.Sleep(1 * time.Second)
	href, _ := s.Attr("href")
	name := s.Text()
	content := getChapter(href)
	val := name + "\n\n" + content

	postLink := forumDomain + "forum.php?mod=post&action=reply&fid=" + fid + "&extra=&tid=" + tid
	err := chromedp.Run(browser,
		chromedp.Navigate(postLink),
		chromedp.WaitVisible("#e_switchercheck"),
		// chromedp.Click("#e_simple", chromedp.NodeVisible),
		chromedp.Click("#e_switchercheck", chromedp.NodeVisible),
		chromedp.SetValue("e_textarea", val),
		chromedp.Click("#postsubmit", chromedp.NodeVisible),
		chromedp.WaitVisible("#postlist"),
	)
	if err != nil {
		log.Fatal("post novel failed", err)
	}
}

func getChapter(link string) string {
	resp, err := http.Get("https:" + link)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	div := doc.Find("div.content").First()
	text := div.Text()
	content := Formate(text)
	return content
}
