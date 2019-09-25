import requests
import json

headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://cafe.bithumb.com",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://cafe.bithumb.com/view/boards/43",
        "Accept-Encoding": "gzip, deflate, br"
    }

string = """columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&start=30&length=30&search[value]=&search[regex]=false"""


article_root = "https://cafe.bithumb.com/view/board-contents/{}"

for page in range(1,4):
    with requests.Session() as s:
        s.headers.update(headers)

        data = {"draw":page}
        data.update( { ele[:ele.find("=")]:ele[ele.find("=")+1:] for ele in string.split("&") } )
        data["start"] = 30 * (page - 1)

        r = s.post('https://cafe.bithumb.com/boards/43/contents', data = data, verify = False) # set verify = False while you are using fiddler

        json_data = json.loads(r.text).get("data") # transform string to dict then we can extract data easier
        for each in json_data:
            url = article_root.format(each[0])
            print(url)