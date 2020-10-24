# pip install bs4
# pip install requests

import csv
import requests
from bs4 import BeautifulSoup

has_args = False
while not has_args:
    job = input("Job Title: ")
    location = input("Job Location: ")
    if ((job != None) and (location != None)):
        has_args = True

URL = "https://www.monster.com/jobs/search/?q={}&where={}".format(job,location)
page = requests.get(URL)

outfile = open("my_results.csv","w",newline="")
writer = csv.writer(outfile)
writer.writerow(["job_title","company","location","age","listing_url"])

soup = BeautifulSoup(page.content, "html.parser")
table_data = soup.findAll("div", {"class": "flex-row"})
for row in table_data:
    job_object = row.find("header", {"class": "card-header"}).find("h2", {"class": "title"})
    job_link = job_object.find('a', href=True)['href']
    job_title = job_object.get_text().replace('\n','').replace('\r','')
    company = row.find("div", {"class": "company"}).find("span", {"class": "name"}).get_text().replace('\n','').replace('\r','')
    location = row.find("div", {"class": "location"}).find("span", {"class": "name"}).get_text().replace('\n','').replace('\r','')
    age = row.find("time").get_text()
    writer.writerow([job_title,company,location,age,job_link])

outfile.close()

print("Search complete. See my_results.csv for output!")
