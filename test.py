import requests

url = "https://de.indeed.com/Jobs?q=Data+Scientist&jt=contract"


page_counter = 0
while True:
    my_url = url + "&start=" + str(page_counter)
    page_html = requests.get(my_url).text
    if "Weiter&nbsp;&raquo;" in page_html:
        page_counter += 10
    else:
        break

print(page_counter+10)