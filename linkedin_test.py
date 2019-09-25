import bs4
import requests
import csv

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

url = "https://www.linkedin.com/jobs/search?keywords=android&location=Sch%C3%B6nefeld%2C%20BB&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=2&f_JT=I&f_C=167024%2C2567873&currentJobId=1459911512"


# Write to CSV file
outfile = open('linkedin.csv','w', encoding="utf-8", newline='')
writer = csv.writer(outfile, delimiter=",")
writer.writerow(["Title", "City"])


html = requests.get(url, headers=headers).content.decode('utf-8')
#time.sleep(1)
soup = bs4.BeautifulSoup(html, 'html.parser')

div_results = soup.find("div", {"class":{"results-context-header"}}).find("span").text
total_page = (int(div_results)/10) + 1
pages = list(range(1, int(total_page)))

for page in pages:
    r = requests.get(url + '&start=' + str(page), headers=headers).content.decode('utf-8')
    soup = bs4.BeautifulSoup(r, 'html.parser')

    job_list = soup.find_all('li', {"class":{"result-card"}})
    for job in job_list:
        titleStr = job.find('a').text
        location = job.find('div', {"class":{"result-card__meta job-result-card__meta"}}).find("span").text

        writer.writerow([titleStr, location])

        print("__________________________________________")
        print (titleStr)
        print(location)



