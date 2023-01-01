from bs4 import BeautifulSoup
import requests
import csv

file = open("user-details.csv","w",encoding='UTF-8')
csvwriter = csv.writer(file,dialect="excel")
csvwriter.writerow(['location','topics'])

for page in range(1,91):
    site = requests.get(f'https://stackoverflow.com/users?page={page}&tab=reputation&filter=all')

    soup = BeautifulSoup(site.content, "lxml")

    locations = soup.find_all('span', 'user-location')
    tags = soup.find_all('div','user-details')
    
    for tag,location in zip(tags,locations):
        link = tag.a['href']
        web = f"https://stackoverflow.com{link}"
        
        content = requests.get(web).text
        soup = BeautifulSoup(content,"lxml")

        tags = soup.find_all('a','s-tag js-gps-track')
        
        topic_list =[]
        for tag in tags:
            topic_list.append(tag.text)
        
        csvwriter.writerow([location.text, topic_list])