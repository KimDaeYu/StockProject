from bs4 import BeautifulSoup
import requests
import time
search_word = "삼성" #검색어 지정
start = 1
end = 300 #마지막 뉴스 지정
title_list = []
 
if __name__ == '__main__':
    start_time = time.time()
    while 1:
        if start > end:
            break
        print(start)
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'.format(search_word,start)
        req = requests.get(url)

        #정상적인 request 확인
        if req.ok:
            html = req.text
            soup = BeautifulSoup(html,'html.parser')
    
            #뉴스제목 뽑아오기
            titles = soup.select(
                'ul.type01 > li > dl > dt > a'
            )
            #list에 넣어준다
            for title in titles:
                title_list.append(title['title'])
        start += 10
    print(title_list)
    print("실행 시간 : %s초" % (time.time() - start_time))
