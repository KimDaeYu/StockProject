import time
import asyncio
# aiohttp 설치 필요
import aiohttp
from bs4 import BeautifulSoup
import lxml
import cchardet


a = []
async def get_text_from_url(url,a):  # 코루틴 정의
    #print(f'Send request to ... {url}')

    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, headers={'user-agent': 'Mozilla/5.0'}) as res:
            text = await res.text()

    #print(f'Get response from ... {url}')
    a.append(BeautifulSoup(text, 'lxml').text)
    #print(text[:100].strip())


async def main():
    base_url = 'https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode=A{keyword}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
    #base_url = "https://finance.naver.com/item/main.nhn?code={keyword}"
    #base_url = "http://comp.fnguide.com/SVO2/asp/SVD_Finance.asp?pGB=1&gicode=A{keyword}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=103&stkGb=701"
    keywords = ["000020","000040","000050","000060","000070","000080","000100","000020","000040","000050","000060","000070","000080","000100","000020","000040","000050","000060","000070","000080","000100","000020","000040","000050","000060","000070","000080","000100"]

    # 아직 실행된 것이 아니라, 실행할 것을 계획하는 단계
    futures = [asyncio.ensure_future(get_text_from_url(
        base_url.format(keyword=keyword),a)) for keyword in keywords]

    await asyncio.gather(*futures)

if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = time.time()
    print(a)
    print(f'time taken: {end-start}')