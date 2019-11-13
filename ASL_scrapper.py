from bs4 import BeautifulSoup
import requests
import re
import os

base_url = "https://www.handspeak.com/word/search/index.php"

#os.environ.get('GDRIVE_KEY')
max_id = 6547

for asl_id in range(max_id):
  page = base_url+"?id={}".format(asl_id)
  html = requests.get(page)
  soup = BeautifulSoup(html, 'html.parser')
  header2 = soup.h2 
  re.search("ASL sign for: (.*)", header2)
