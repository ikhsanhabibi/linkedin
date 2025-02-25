import re as standardre
import time
from datetime import datetime

import requests, bs4
import csv

from geopy.geocoders import Nominatim


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

urls = open("urls_indeed.txt").readlines()


# Write to CSV file
outfile = open('jobs.csv','w', encoding="utf-8", newline='')
writer = csv.writer(outfile, delimiter=",")
#writer.writerow(["Title", "Company", "City", "Country", "Type", "Summary", "Email", "Website", "Source", "PostedDate"])


#Scrape all URLs
for url in urls:
    urlClean = url.replace("\n", "")
    html = requests.get(urlClean, headers=headers).content.decode('utf-8')
    #time.sleep(1)
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Page Counter
    page_counter = 0
    while True:
        my_url = url + "&start=" + str(page_counter)
        page_html = requests.get(my_url).text

        if "Weiter&nbsp;&raquo;" in page_html:
            page_counter += 10
        else:
            break
    page_counter+= 10;

    # Max Pages = 100
    pages = list(range(1, int(page_counter/10) + 1))


    # Pagination
    start_page = 1
    last_page = len(pages)

    # Scrape per page
    for page in pages:
        page_url = url + '&start=' + str((int(page - 1) * 10))
        html = requests.get(page_url, headers=headers).content.decode('utf-8')
        #time.sleep(1)

        soup = bs4.BeautifulSoup(html, 'html.parser')

        print("=======================================================")
        print("                      INDEED                           ")
        print("                                                       ")
        print('Processing ...   Index: urls[' + str(urls.index(url)) + ']  ' + ' Page: ' + str(page) + ' of ' + str(len(pages)))
        print("                                                       ")
        print("=======================================================")


        job_list = soup.findAll("div",{"class":"jobsearch-SerpJobCard"})
        for job in job_list:

            link_job_page = 'https://indeed.com' + job.find('a').attrs['href']
            html = requests.get(link_job_page, headers=headers).content.decode('utf-8')
            #time.sleep(1)
            soup = bs4.BeautifulSoup(html, 'html.parser')

            try:
                title = soup.find('h3')
                titleStr = title.text.strip()
            except:
                titleStr = ''

            company = job.find('span').text.strip()

            city = job.find({'span','div'}, {'class':'location'}).text.strip()

            try:
                geolocator = Nominatim()
                countryName = geolocator.geocode(city, language='en')._address.split()[-1]
                country = countryName.strip()
            except:
                country = ''

            try:
                type = soup.find('span', {'class':{'jobsearch-JobMetadataHeader-item'}})
                typeList = type.text.replace(",", " ").split()

                internship = ''
                fulltime = ''
                parttime = ''

                if 'Internship' or 'Praktikum' in typeList:
                    internship = 'Yes'
                elif 'Fulltime' or 'Full-time' or 'Vollzeit' or 'Festanstellung' or 'Permanent' in typeList:
                    fulltime = 'Yes'
                elif 'Parttime' or 'Part-time' or 'Teilzeit' or 'Contract' in typeList:
                    parttime = 'Yes'
                else:
                    internship = ''
                    fulltime = ''
                    parttime = ''

            except:
                typeList = ''
                internship = ''
                fulltime = ''
                parttime = ''

            try:
                summary = soup.find('div', {'id':{'jobDescriptionText'}}).text.replace('\t',' ').replace('\n',' ').replace('"',"").replace("'","").strip('\n').strip('\t')
            except:
                summary=''

            try:
                email = standardre.search(r'[\w\.-]+@[\w\.-]+\.\w+', summary).group()
                emailStr = str(email)
                containsAt = standardre.search('@', emailStr)
                containsAt = standardre.search('@', emailStr)
                if containsAt == None:
                    emailStr =''

            except:
                emailStr = ''

            try:
                website = soup.find('span', {'id':{'originalJobLinkContainer'}}).find('a').attrs['href']
                websiteStr = str(website)
                containsHttp = standardre.search('http', websiteStr)
                if containsHttp == None:
                    websiteStr = ''
            except:
                websiteStr = ''

            try:
                postedDate = job.find('div', {"class": {"result-link-bar"}}).find("span", {"class": {"date"}})
                postedDateStr = str(postedDate.text)
            except:
                postedDateStr = ''

            source = 'indeed'

            scrapeDate = datetime.now().strftime('%Y-%m-%d')

            writer.writerow([titleStr, company, city, country, internship, fulltime, parttime, summary, emailStr, websiteStr, source, postedDateStr, scrapeDate])

            print("_________________________________________________________________________________")
            print('Title: ' + titleStr)
            print('Company: ' + company)
            print('City: ' + city)
            seperator = ', '
            print('Type: ' + seperator.join(typeList))



outfile.close()
print ('Done')