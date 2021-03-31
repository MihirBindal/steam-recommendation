import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from textblob import TextBlob
import json


def get_description(game_id):
    link = "https://store.steampowered.com/app/" + str(game_id)
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    divisions = soup.body.div.div.find_next_siblings("div")[5]
    body = divisions.div.find_next_siblings("div")[2].div.div.find_next_siblings("div")[1]
    name = body.div.find_next_sibling("div").div.find_next_sibling("div").div.div.find_next_siblings("div")[1].getText()
    left_body = body.div.find_next_siblings("div")[2].div.div.div
    right_body = body.div.find_next_siblings("div")[2].div.div.find_all("div", {"class": "leftcol"})[0]
    video_block = right_body.div.div.div

    try:
        image_link = video_block.find_all("div", {"class": "highlight_player_item highlight_screenshot"})[0].div.a[
            'href']
        image_link = "<img src=\""+image_link+"\" width=\"460\" height=\"345\"/>"
        print(image_link)
        video_link = image_link
    except:
        video_link = video_block.find_all("div", {"class": "highlight_player_item highlight_movie"})[0][
            'data-mp4-source']
        print(video_link)
    image = left_body.img
    image = image['src']
    image = "<img src=\"" + image + "\" width=\"460\" height=\"345\"/>"
    desc = left_body.div.find("div", {"class": "game_description_snippet"}).getText().strip()
    review_block = left_body.div.div.find_next_siblings("div")[1]
    review = review_block.div.find("div", {"class": "summary column"}).span.getText()
    release_date = review_block.div.find("div", {"class": "release_date"}).getText()
    release_date = release_date.replace("Release Date:", "").strip()
    developer = review_block.div.div.find_next_siblings("div")[2].getText()
    developer = developer.replace("Developer:", "").replace("Publisher:", "").strip()
    # publisher = review_block.div.div.find_next_siblings("div")[2].getText()
    # print(publisher.replace("Developer:", "").replace("Publisher:", "").strip())
    tag_list = []
    tags = left_body.div.div.find_next_siblings("div")[2].find_all("a")
    num = 0
    for (tag, num) in zip(tags, range(0, 5)):
        tag_list.append(tag.getText().strip())
    description = body.div.find_next_siblings("div")[3].div.find_next_sibling("div") \
        .find_all("div", {"class": "game_page_autocollapse"})
    # print(len(description))
    if len(description) > 4:
        description = body.div.find_next_siblings("div")[3].div.find_next_sibling("div") \
            .find_all("div", {"class": "game_page_autocollapse"})[len(description) - 4].div.prettify()
    elif len(description) <= 2:
        description = body.div.find_next_siblings("div")[3].div.find_next_sibling("div") \
            .find_all("div", {"class": "game_page_autocollapse"})[0].div.prettify()
    else:
        description = body.div.find_next_siblings("div")[3].div.find_next_sibling("div") \
            .find_all("div", {"class": "game_page_autocollapse"})[len(description) - 3].div.prettify()
    print(description)
    return name, image, desc, review, release_date, tag_list, description, video_link


def get_reviews(game_id):
    link = "https://steamcommunity.com/app/" + str(
        game_id) + "/reviews/?browsefilter=toprated&snr=1_5_100010_#scrollTop=0"
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    review_page = soup.body.div.find("div", {"class": "responsive_page_content"}) \
        .find("div", {"class": "responsive_page_template_content"}).div.div.div.find_next_sibling("div").div
    divisions = review_page.find_all("div", {"class": "apphub_Card modalContentLink interactable"})
    num = 0
    review_list = []
    sentiment_list = []
    for (division, num) in zip(divisions, range(0, 10)):
        mini_div = division.div.find("div", {"class": "apphub_CardTextContent"}).getText()
        article = re.sub(r'\w+:\s\d+\s\w+\s+', '', mini_div)
        review = article.split('\n')[-1].strip()
        review_list.append(review)
        sentiment = TextBlob(review).sentiment.polarity
        if sentiment > 0:
            sentiment = "positive"
        elif sentiment == 0:
            sentiment = "neutral"
        else:
            sentiment = "negative"
        sentiment_list.append(sentiment)
    res_dict = dict(zip(review_list, sentiment_list))
    return res_dict


def get_json_data(game_id):
    name, image, desc, review, release_date, tag_list, description, video_link = get_description(game_id)
    review_dict = get_reviews(game_id)
    final_dict = {'name': name, 'image_url': image, 'video_link': video_link, 'short_description': desc,
                  "overall_review": review,
                  "release_date": release_date, "tags": tag_list, "game_description": description,
                  "reviews": review_dict}
    return final_dict


json_dict = get_json_data(703080)
#print(json_dict)
