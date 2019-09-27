import re as standardre
import time
from datetime import datetime

import requests, bs4
import csv

import requests as requests
from geopy.geocoders import Nominatim
geolocator = Nominatim()

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

urls = ["https://www.simplyhired.de/search?q=android&l=berlin&jt=internship&job=toouc-wnNEPH1BgO9HWbJ3HkvCjsJemdpWImTtm8dnB1MY5MLz_6MA"]


# Write to CSV file
outfile = open('jobs.csv','a', encoding="utf-8", newline='')
writer = csv.writer(outfile, delimiter=",")
writer.writerow(["Title", "Company"])


#Scrape all URLs
for url in urls:
    urlClean = url.replace("\n", "")
    html = requests.get(urlClean, headers=headers).content.decode('utf-8')
    #time.sleep(1)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    url_split = url.split('&')
    del url_split[-1]

    seperator = ','
    url = seperator.join(url_split).replace(",", "&")

    # Page Counter
    page_counter = 0
    while True:

        my_url = url + "&pn=" + str(page_counter)
        page_html = requests.get(my_url).text

        if "fa fa-angle-right" in page_html:
            page_counter += 1
        else:
            break

    # Max Pages = 100
    pages = list(range(1, int(page_counter) + 1))


    # Pagination
    start_page = 1
    last_page = len(pages)

    # Scrape per page
    for page in pages:
        page_url = url + "&pn=" + str(page)
        html = requests.get(page_url, headers=headers).content.decode('utf-8')
        #time.sleep(1)

        soup = bs4.BeautifulSoup(html, 'html.parser')

        print("=======================================================")
        print("                      SIMPLY HIRED                     ")
        print("                                                       ")
        print('Processing ...   Index: urls[' + str(str(urls.index(urlClean))) + ']  ' + ' Page: ' + str(page) + ' of ' + str(len(pages)))
        print("                                                       ")
        print("=======================================================")


        job_list = soup.findAll("div",{"class":"card js-job"})
        for job in job_list:

            link_job_page = 'https://simplyhired.com' + job.find('a').attrs['href']
            html = requests.get(link_job_page, headers=headers).content.decode('utf-8')
            #time.sleep(1)
            soup = bs4.BeautifulSoup(html, 'html.parser')

            title = soup.find('h1')
            titleStr = title.text.strip()

            company = soup.find('h2').find('span').text.strip()

            city = soup.find('span', {"class":{"location"}}).text.strip()

            try:
                country = geolocator.geocode(city, language='en')._address.split()[-1]
            except:
                country = ''

            try:
                type = soup.find('i', {"class": {"fa fa-briefcase"}}).next
                typeStr = type.text.split("|")
            except:
                typeStr = ''

            try:
                summary = soup.find('div' , {"class":{"viewjob-description"}}).text.replace('\t',' ').replace('\n',' ').replace('"',"").strip('\n').strip('\t')
            except:
                summary = ''

            try:
                email = standardre.findall(r'[\w\.-]+@[\w\.-]+\.\w+', summary)
                emailStr = str(email)
                containsAt = standardre.search('@', emailStr)
                if containsAt == None:
                    emailStr = ''

            except:
                emailStr = ''

            website = 'https://simplyhired.com' + job.find('a').attrs['href']
            websiteStr = str(website)

            try:
               postedDate = soup.find('i', {"class": {"fa fa-clock-o"}}).next
               postedDateStr = postedDate.text
            except:
               postedDateStr = ''


            source = 'Simply Hired'


            # scrapeDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            writer.writerow(
                [titleStr, company, city, country, typeStr, summary, emailStr, websiteStr, source, postedDateStr])

            print("_________________________________________________________________________________")
            print('Title: ' + titleStr)
            print('Company: ' + company)
            print('City: ' + city)
            seperator = ','
            print('Type: ' + seperator.join(typeStr))

