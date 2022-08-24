import gspread
import requests
from bs4 import BeautifulSoup

gc = gspread.service_account(filename="cred.json")

sh = gc.open("KMPN Pathfinder 22/23")

hello = sh.get_worksheet(2)

def extract():
    
    div_len = []
    for page in range(10):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'}
        url = f"https://id.indeed.com/jobs?q=aircraft%2Caerospace%2Caerodynamic%2Cairline%2Cdrone%2Cfem&start={page*10}&vjk=ff53be6e8c804d3d"
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.content, 'html.parser')
        divs = soup.find_all("div", class_ ="cardOutline")

        div_len.append(len(divs))
        print(len(divs))

        for item in divs: #item is not integer cant be assign as index
            title = str(item.find("span").text)
            company = str(item.find("span", class_ = "companyName").text)
            link = "https://id.indeed.com" + str(item.find("a", class_ = "jcs-JobTitle", href=True)["href"])
            hello.append_row([title, company, link])

        if (div_len[page] != div_len[page-1]):
            break

    return

#requesting higher quota first 64 then 93 google sheets api problem

extract()
    


