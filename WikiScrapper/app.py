import requests
from bs4 import BeautifulSoup
from DatabaseHandling import MongoDBManagement
from TextHandling import TextHandler
from ReferenceLinkHandling import ReferenceHandler
from ImageHandling import ImageHandler
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin

db_name = 'WikiScrapper'

global_collection_name = ''

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    global global_collection_name
    if request.method == 'POST':
        search_string = request.form['content'].replace(" ", "_").lower()
        global_collection_name = search_string
        text = ''
        try:

            mongo_connection = MongoDBManagement()
            if mongo_connection.is_collection_present(collection_name=search_string, db_name=db_name):
                data_in_db = mongo_connection.get_record_data(query={'Title': search_string}, db_name=db_name,
                                                              collection_name=search_string)
                refer_to_store = data_in_db['References']
                image_handle = ImageHandler()
                decoded_images_list = image_handle.get_decoded_images(images=data_in_db['Images'])
                return render_template('results.html', data=data_in_db, decoded_images_list=decoded_images_list,
                                       reference_links=refer_to_store)
            else:
                url = "https://en.wikipedia.org/wiki/" + search_string
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")
                text_handle = TextHandler(soup)
                text_to_store = text_handle.get_summary()
                refer_handle = ReferenceHandler()
                refer_handle.store_links(soup)
                refer_to_store = refer_handle.get_references()
                image_handle = ImageHandler()
                image_handle.encode_images(soup)
                images_to_store = image_handle.get_images()

                record_to_store = {'Title': search_string,
                                   'Summary': text_to_store,
                                   'References': refer_to_store,
                                   'Images': images_to_store
                                   }

                mongo_connection.create_collection(collection_name=search_string, db_name=db_name)
                mongo_connection.create_document(db_name=db_name, collection_name=search_string, record=record_to_store)
                return redirect(url_for('feedback'))

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    global global_collection_name
    search_string = global_collection_name
    try:
        mongo_connection = MongoDBManagement()
        if mongo_connection.is_collection_present(collection_name=search_string, db_name=db_name):
            data_in_db = mongo_connection.get_record_data(query={'Title': search_string}, db_name=db_name,
                                                          collection_name=search_string)
            refer_to_store = data_in_db['References']
            image_handle = ImageHandler()
            decoded_images_list = image_handle.get_decoded_images(images=data_in_db['Images'])
            return render_template('results.html', data=data_in_db, decoded_images_list=decoded_images_list,
                                   reference_links=refer_to_store)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))


if __name__ == "__main__":
    app.run()
