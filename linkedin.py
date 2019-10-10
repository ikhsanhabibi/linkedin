import time
import re as standardre

import bs4
import requests
import csv

from geopy.geocoders import Nominatim
geolocator = Nominatim()

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

urls = open("urls_linkedin.txt").readlines()


# Write to CSV file
outfile = open('jobs.csv','a', encoding="utf-8", newline='')
writer = csv.writer(outfile, delimiter=",")
#writer.writerow(["Title", "Company", "City", "Country", "Type", "Summary", "Email", "Website", "Source", "PostedDate"])



#Scrape all URLs
for url in urls:
    urlClean = url.replace("\n", "")
    html = requests.get(urlClean, headers=headers).content.decode('utf-8')
    #time.sleep(1)
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Find the result (Total page)
    div_results = soup.find("div", {"class":{"results-context-header"}}).find("span").text
    total_page = (int(div_results)/10) + 2
    pages = list(range(1, int(total_page)))



    for page in pages:
        page_link = requests.get(url + '&start=' + str(page), headers=headers).content.decode('utf-8')
        soup = bs4.BeautifulSoup(page_link, 'html.parser')




        print("=======================================================")
        print("                    LINKEDIN                           ")
        print("                                                       ")
        print('Processing ...   Index: urls[' + str(urls.index(url)) + ']  ' + ' Page: ' + str(page) + ' of ' +  str(len(pages)))
        print("                                                       ")
        print("=======================================================")


        job_list = soup.find_all('li', {"class":{"result-card"}})
        for job in job_list:

            link_job_page = job.find('a').attrs['href']
            html = requests.get(link_job_page, headers=headers).content.decode('utf-8')
            #time.sleep(1)
            soup = bs4.BeautifulSoup(html, 'html.parser')


            # Title, Company
            titleStr = job.find('a').text
            company = job.find('h4').text

            # City & Country
            location = job.find('div', {"class":{"result-card__meta job-result-card__meta"}}).find("span").text
            locationSplit = location.replace(",", " ").split()

            city = locationSplit[:2]
            seperator = ','
            cityStr = seperator.join(city).replace(',', " ")

            try:
                country = geolocator.geocode(cityStr, language='en')._address.split(",")[-1]
            except:
                country = ''

            type = soup.find_all('li', {"class":{"job-criteria__item"}})[1].find('span').text
            typeStr = str(type)

            internship = ''
            fulltime = ''
            parttime = ''

            if typeStr in ('Internship','Praktikum'):
                internship = 'Yes'
            elif typeStr in ('Fulltime','Full-time','Vollzeit','Festanstellung','Permanent'):
                fulltime = 'Yes'
            elif typeStr in ('Parttime','Part-time','Teilzeit', 'Contract', 'Temporary'):
                parttime = 'Yes'
            else:
                internship = ''
                fulltime = ''
                parttime = ''


            summary = soup.find('div', {"class":{"description__text description__text--rich"}}).text.replace('\t',' ').replace('\n',' ').replace('"',"").replace("'","").strip('\n').strip('\t')

            try:
                email = standardre.search(r'(?:\.?)([\w\-_+#~!$&\'\.]+(?<!\.)(@|[ ]?\(?[ ]?(at|AT)[ ]?\)?[ ]?)(?<!\.)[\w]+[\w\-\.]*\.[a-zA-Z-]{2,3})(?:[^\w])', summary).group()
                emailStr = str(email)
                containsAt = standardre.search('@', emailStr)
                containsAt = standardre.search('@', emailStr)
                if containsAt == None:
                    emailStr = ''

            except:
                emailStr = ''

            websiteStr = job.find('a').attrs['href']

            source = 'Linkedin'

            postedDate = job.find('time').text
            postedDateStr = str(postedDate)

            writer.writerow(
                [titleStr, company, cityStr, country, internship, fulltime, parttime, summary, emailStr, websiteStr, source, postedDateStr])

            print("_________________________________________________________________________________")
            print('Title: ' + titleStr)
            print('Company: ' + company)
            print('City: ' + cityStr)
            print('Type: ' + typeStr)


