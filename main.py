import re as standardre

import requests, bs4
import csv
import time
#from selenium import webdriver

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

urls = [ "https://de.indeed.com/Jobs?q=android+entwickler&jt=internship"]


# Write to CSV file
outfile = open('indeed.csv','a', encoding="utf-8", newline='')
writer = csv.writer(outfile, delimiter=",")
writer.writerow(["Title", "Company", "Location", "Type", "Summary", "Email", "Website"])


#scrape elements
for url in urls:
    #root_url = url
    html = requests.get(url, headers=headers)
    time.sleep(3)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')


    # Pagination
    paging = soup.find("div",{"class":"pagination"}).find_all("a")
    start_page = int(paging[0].text) - 1
    last_page = paging[len(paging)-2].text



    # Scrape per page
    pages = list(range(1,int(last_page)+1))
    for page in pages:
        page_url = url + '&start=' + str((int(page-1)*10))
        html = requests.get(page_url, headers=headers)
        time.sleep(5)

        soup = bs4.BeautifulSoup(html.text, 'html.parser')

        print ('Processing URL with index: ' + str(urls.index(url)) + ' page: ' + str(page))



        job_list = soup.findAll("div",{"class":"jobsearch-SerpJobCard"})
        for job in job_list:
            #driver = webdriver.Chrome(executable_path='/Users/Ikhsan/Downloads/chromedriver')
            #driver.get(page_url)
            #python_button = driver.find_element_by_class_name('title')
            #python_button.click()

            link_job_page = 'https://indeed.com' + job.find('a').attrs['href']
            html = requests.get(link_job_page, headers=headers)
            time.sleep(3)

            soup = bs4.BeautifulSoup(html.text, 'html.parser')

            title = soup.find('h3')
            titleStr = title.text.strip()

            company = job.find('span').text.strip()

            location = job.find({'span','div'}, {'class':'location'}).text.strip()

            type = soup.find('span', {'class':{'jobsearch-JobMetadataHeader-item'}}).text.strip()

            summary = soup.find('div', {'class':{'jobsearch-JobComponent-description'}}).text.strip().replace('\t','').replace('\n','').strip('\n').strip('\t')

            try:
                email = standardre.findall(r'[\w\.-]+@[\w\.-]+\.\w+', summary)[0]
            except:
                email = standardre.findall(r'[\w]+..\w.[\w\.-]+\.\w+', summary)

            try:
                website = soup.find('span', {'id':{'originalJobLinkContainer'}}).find('a').attrs['href']
            except:
                website = soup.find('a', {'class':{'icl-Button'}}).attrs['href']

            writer.writerow([titleStr, company, location, type, summary, email, website])



outfile.close()
print ('Done')