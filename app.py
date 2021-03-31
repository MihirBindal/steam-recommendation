from flask import Flask, render_template
import extractor
import json

app = Flask(__name__)


@app.route('/id=<int:game_id>', methods=['GET'])
def index(game_id):
    json_dict = extractor.get_json_data(game_id)
    name = json_dict['name']
    image_url = json_dict['image_url']
    video_link = json_dict['video_link']
    short_description = json_dict['short_description']
    overall_review = json_dict['overall_review']
    release_date = json_dict['release_date']
    tags = json_dict['tags']
    game_description = json_dict['game_description']
    reviews = json_dict['reviews']
    return render_template("game_page.html", name=name, image_url=image_url, video_link=video_link,
                           s_des=short_description, overall_review=overall_review, release_date=release_date, tags=tags,
                           game_description=game_description, reviews=reviews)


@app.errorhandler(404)
def not_found(e):
    return "The get request should be http://127.0.0.1:5000/id=*number*"


if __name__ == '__main__':
    app.run(debug=True)
