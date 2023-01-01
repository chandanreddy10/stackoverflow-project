from bs4 import BeautifulSoup
import requests
import re
import csv

file = open("stack_overflow_questions_data.csv","w",encoding="UTF-8")
cwriter = csv.writer(file,dialect="excel")
cwriter.writerow(['Question','Votes','Answers','Views','Tags','Date'])


for pageno in range(1,13000):  
        
    website = f"https://stackoverflow.com/questions?tab=active&page={pageno}"
        
    SITE= requests.get(website).text
    site = (SITE.replace(u"\u0131","i"))

    soup = BeautifulSoup(site, "lxml")

    questions_class = 's-post-summary js-post-summary'
    stats_class = 's-post-summary--stats js-post-summary-stats'
    tags_class = 'ml0 list-ls-none js-post-tag-list-wrapper d-inline'
    time_class = 'relativetime'

    questions = soup.find_all('div',questions_class)
    stats = soup.find_all('div', stats_class)
    tags = soup.find_all('ul',tags_class )
    dates =  soup.find_all('span',time_class)

    pattern = re.compile(r'[\d k]{1,5}')

    for question,stat,tag,date in zip(questions,stats,tags,dates):
        
        qtion = question.h3.a.text
        
        contents = stat.text
        stats = pattern.findall(contents)
        
        votes = stats[0]
        answers = stats[1]
        views = stats[2]

        question_tags = [t.text for t in tag]
        date_tag = date.text

        cwriter.writerow([qtion,votes,answers,views,question_tags,date_tag]) 

file.close()
        
