import urllib.request
from bs4 import BeautifulSoup
import pickle
import gzip
import sys
sys.setrecursionlimit(100000)


import asyncio
import aiohttp
import html5lib

# class mtest:
#     def __init__(self,code):
#         self.wws = 
#         self.loop = asyncio.get_event_loop()

#     def get_ticks(self):
#         return self.loop.run_until_complete(self.__async__get_ticks())

#     async def __async__get_ticks(self):
#         async with self.wws as echo:
#             await echo.send(json.dumps({'ticks_history': 'R_50', 'end': 'latest', 'count': 1}))
#             return await echo.receive()


async def fetch_url_aiohttp(url):
    return aiohttp.request('get', url)


class StockFinance:
    def __init__(self,code):
        self.loop = asyncio.get_event_loop()
        self.URL_PART1 = "https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode=A"
        self.Stock_CODE = code
        self.URL_PART2 = "&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
        self.URL_TPL = self.URL_PART1 + self.Stock_CODE + self.URL_PART2
        self.data = ""
        self.res = asyncio.wait(fetch_url_aiohttp(self.URL_TPL))
        print(self.data)
        self.soup = BeautifulSoup(self.data.decode('utf-8'), 'html5lib')
        self.Price = {}
        self.D_Y = {} #연간
        self.D_A = {} #분기
        self.B_Y = {}
        self.B_A = {}

    def get_ticks(self):
        return self.loop.run_until_complete(self.__async__get_ticks())


    def getPrice(self):
        self.Pricetag = self.soup.find("div", {"id": "svdMainGrid1", "class": "um_table"})

        self.Pricetag = self.Pricetag.find("tbody")
        self.Pricetag = self.Pricetag.find_all("tr")
        self.Pricetag = self.Pricetag[0].find_all("td")
        self.Pricetag = self.Pricetag[0].get_text(" ", strip=True)
        for i in enumerate(self.Pricetag):
            if(i[1] is '/'):
                self.Price["Price"] = self.Pricetag[0:i[0]]
                self.Price["Gap"] = self.Pricetag[i[0]+2:]
                #print(self.Price["Price"])
                #print(self.Price["Gap"])

    #연결
    def D_AnnualFinance(self):
        self.highlight_D_Y = self.soup.find("div", {"id": "highlight_D_Y", "class": "um_table"})
        try:
            self.period = self.highlight_D_Y.find("tr", {"class": "td_gapcolor2"})
            self.subperiod = self.period.find_all("th")
        except:
            self.Stock_CODE = self.Stock_CODE + 'N'
            print(self.Stock_CODE)
            return

        #기간설정
        for i in self.subperiod:
            if i.find("div").string:
                self.D_Y[i.find("div").string] = {}
            else:
                if i.find("span").string:
                    self.D_Y[i.find("span").string] = {}

        #print(self.D_Y)
        self.FinaceValues = self.highlight_D_Y.find("tbody")
        self.FinaceValues = self.FinaceValues.find_all("tr")

        #기간 정보 정리
        for i in range(len(self.FinaceValues)):
            self.subFinaceValues = self.FinaceValues[i].find_all("td")
            for j in range(len(self.subperiod)):
                if self.subperiod[j].find("div").string:
                        if self.FinaceValues[i].find("div").string:
                            self.text = self.FinaceValues[i].find("div").string
                            if self.text:
                                self.text = self.text.replace("\xa0","")
                            self.D_Y[self.subperiod[j].find("div").string][self.text] = self.subFinaceValues[j].string
                        else:
                            self.text = self.FinaceValues[i].find("dt").string
                            if self.text:
                                self.text = self.text.replace("\xa0", "")
                            self.D_Y[self.subperiod[j].find("div").string][self.text] = self.subFinaceValues[j].string
                else:
                    if self.subperiod[j].find("span").string:
                        if self.FinaceValues[i].find("div").string:
                            self.text = self.FinaceValues[i].find("div").string
                            if self.text:
                                self.text = self.text.replace("\xa0", "")
                            self.D_Y[self.subperiod[j].find("span").string][self.text] = self.subFinaceValues[j].string
                        else:
                            self.text = self.FinaceValues[i].find("dt").string
                            if self.text:
                                self.text = self.text.replace("\xa0", "")
                            self.D_Y[self.subperiod[j].find("span").string][self.text] = self.subFinaceValues[j].string
        #print(self.D_Y)

    def D_NetQuarterFinance(self):
        self.highlight_D_A = self.soup.find("div", {"id": "highlight_D_Q", "class": "um_table"})
        try:
            self.period = self.highlight_D_A.find("tr", {"class": "td_gapcolor2"})
            self.subperiod = self.period.find_all("th")
        except:
            self.Stock_CODE = self.Stock_CODE + 'N'
            # print(self.Stock_CODE)
            return

        # 기간설정
        for i in self.subperiod:
            if i.find("div").string:
                self.D_A[i.find("div").string] = {}
            else:
                if i.find("span").string:
                    self.D_A[i.find("span").string] = {}
        #print(self.D_A)
        self.FinaceValues = self.highlight_D_A.find("tbody")
        self.FinaceValues = self.FinaceValues.find_all("tr")

        # 기간 정보 정리
        for i in range(len(self.FinaceValues)):
            self.subFinaceValues = self.FinaceValues[i].find_all("td")
            for j in range(len(self.subperiod)):
                if self.subperiod[j].find("div").string:
                    if self.FinaceValues[i].find("div").string:
                        self.text = self.FinaceValues[i].find("div").string
                        if self.text:
                            self.text = self.text.replace("\xa0", "")
                        self.D_A[self.subperiod[j].find("div").string][self.text] = self.subFinaceValues[j].string
                    else:
                        self.text = self.FinaceValues[i].find("dt").string
                        if self.text:
                            self.text = self.text.replace("\xa0", "")
                        self.D_A[self.subperiod[j].find("div").string][self.text] = self.subFinaceValues[j].string
                else:
                    if self.subperiod[j].find("span").string:
                        if self.FinaceValues[i].find("div").string:
                            self.text = self.FinaceValues[i].find("div").string
                            if self.text:
                                self.text = self.text.replace("\xa0", "")
                            self.D_A[self.subperiod[j].find("span").string][self.text] = self.subFinaceValues[j].string
                        else:
                            self.text = self.FinaceValues[i].find("dt").string
                            if self.text:
                                self.text = self.text.replace("\xa0", "")
                            self.D_A[self.subperiod[j].find("span").string][self.text] = self.subFinaceValues[j].string
        # print(self.D_A)


    #별도
    def B_AnnualFinance(self):
        webtoon_area = self.soup.find("div", {"id": "highlight_B_Y", "class": "um_table"})
    def B_NetQuarterFinance(self):
        webtoon_area = self.soup.find("div", {"id": "highlight_B_Q", "class": "um_table"})

    def SaveFileD_A(self):
        with gzip.open("./finance/" + self.Stock_CODE, 'wb') as f:
            self.pk = pickle
            self.pk.dumps(self.D_A, f)
    def LoadFileD_A(self):
        with gzip.open("./finance/" + self.Stock_CODE, 'rb') as f:
            self.data = pickle.load(f)
            print(self.data)

            


            
if __name__ == "__main__":
    tt = ["001360","001360","001360","001360","001360","001360","001360"]
    tasks = [StockFinance(x) for x in tt]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print('done')
    # temp = StockFinance("001360")
    # temp.D_NetQuarterFinance()
    # temp.getPrice()
    # print(temp.D_A)
    #temp.SaveFileD_A()