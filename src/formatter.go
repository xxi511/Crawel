package main

import (
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"strings"
)

var wordDic = []string{}
var redundantDic = []string{}

func Formate(content string) string {
	trimString := trimSpace(content)
	newContent := replaceWord(trimString)
	return newContent
}

func trimSpace(content string) string {
	_redundantStr := loadRedundant()
	splits := strings.Split(content, "\n")
	trimed := []string{}
	for _, sen := range splits {
		str := "　　" + strings.TrimSpace(sen)
		if !Contains(str, _redundantStr) {
			trimed = append(trimed, str)
		}
	}
	res := strings.Join(trimed[:], "\n")
	return res
}

func replaceWord(content string) string {
	newContent := content
	dicArr := loadDataDic()
	for _, dic := range dicArr {
		_str := strings.Split(dic, " ")
		re := regexp.MustCompile(_str[0])
		newContent = re.ReplaceAllString(newContent, _str[1])
	}

	return newContent
}

func loadDataDic() []string {
	if len(wordDic) > 0 {
		return wordDic
	}

	file, err := os.Open("data.txt")
	if err != nil {
		log.Fatal("Load data.txt failed")
	}
	defer file.Close()

	binary, err := ioutil.ReadAll(file)
	if err != nil {
		log.Fatal("Read data.txt failed")
	}

	data := string(binary)
	dicArr := strings.Split(data, "\n")
	wordDic = dicArr
	return dicArr
}

func loadRedundant() []string {
	if len(redundantDic) > 0 {
		return redundantDic
	}

	file, err := os.Open("redundant.txt")
	if err != nil {
		log.Fatal("Load redundant.txt failed")
	}
	defer file.Close()

	binary, err := ioutil.ReadAll(file)
	if err != nil {
		log.Fatal("Read redundant.txt failed")
	}

	data := string(binary)
	dicArr := strings.Split(data, "\n")
	redundantDic = dicArr
	return dicArr
}

func Contains(target string, sources []string) bool {
	for _, str := range sources {
		if strings.Contains(target, str) {
			return true
		}
	}
	return false
}
