import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

result = requests.get("https://store.steampowered.com/app/271590")
src = result.content

soup = BeautifulSoup(src, "lxml")
divisions = soup.body.div.div.find_next_siblings("div")[5]
body = divisions.div.find_next_siblings("div")[2].div.div.find_next_siblings("div")[1]
name = body.div.find_next_sibling("div").div.find_next_sibling("div").div.div.find_next_siblings("div")[1].getText()
# print(name)
left_body = body.div.find_next_siblings("div")[2].div.div.div
image = left_body.img.get('src')
# print(image)
desc = left_body.div.find("div", {"class": "game_description_snippet"}).getText()
# print(desc.strip())
review_block = left_body.div.div.find_next_siblings("div")[1]
review = review_block.div.find("div", {"class": "summary column"}).span.getText()
# print(review)
release_date = review_block.div.find("div", {"class": "release_date"}).getText()
# print(release_date.replace("Release Date:", "").strip())
developer = review_block.div.div.find_next_siblings("div")[2].getText()
# print(developer.replace("Publisher:", "").strip())
publisher = review_block.div.div.find_next_siblings("div")[2].getText()
print(publisher.replace(r"Developer:", "").strip())
tag_list = []
tags = left_body.div.div.find_next_siblings("div")[2].find_all("a")
for tag in tags:
    tag_list.append(tag.getText().strip())
# print(tag_list)
# description = body.div.find_next_siblings("div")[3].div.find_next_sibling("div")\
#     .find("div", {"class":"game_page_autocollapse"}).div.prettify()
# print(description)

# result = requests.get("https://steamcommunity.com/app/271590/reviews/?browsefilter=toprated&snr=1_5_100010_#scrollTop=0")
# src = result.content
#
# soup = BeautifulSoup(src, "lxml")
# divisions = soup.body.prettify()
# print(divisions)
