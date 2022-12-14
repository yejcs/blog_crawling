from konlpy.tag import Hannanum
from collections import Counter
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os

# 사용자로부터 검색어 입력받기
keyword = input("검색어를 입력하세요: ")

is_save = input("제목 파일을 저장하시려면 1, 아니라면 2를 눌러주세요: ")

print("키워드 분석 중입니다. 잠시만 기다려 주십시오.")

# 네이버 검색 -> 스크래핑
url = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" + keyword
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh;w Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}
response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, "html.parser")
title = soup.select(
    "#main_pack > section > div > div._list > panel-list > div > more-contents > div > ul > li > div > div > a"
)

# 스크랩 결과를 텍스트파일에 저장
f = open("./text/"+ keyword + " title.txt", "w", encoding="utf-8")
for titles in title:
    f.write(titles.text + "\n")

# 빈도수 분석
num = 2
f = open("./text/"+ keyword + " title.txt", "r", encoding="utf-8")
text = f.read()
f.close()

# Hannanum 객체 생성
okt = Hannanum()
word = okt.nouns(text)
count = Counter(word)

# 명사 빈도 카운트
word_list = count.most_common(15)
word_array = []
count_array = []
for word in word_list:
    word_array.append(word[0])
    count_array.append(word[1])

# 그래프 그리기
word_array.reverse()
count_array.reverse()
plt.rc('font', family='Malgun Gothic')
plt.barh(word_array, count_array, color='r')
plt.xticks(count_array)

if is_save == "1":
    pass
elif is_save == "2":
    os.remove("./text/" + keyword + " title.txt")
else:
    raise OSError("유효하지 않은 입력값입니다. 1 혹은 2를 입력해주세요.")

plt.title("'"+keyword+"' 검색 결과에 따른 상위 15개 키워드")
plt.xlabel("빈도수")
plt.show()