import pytesseract
import os

from PIL import Image 
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pdf2image import convert_from_path
from dotenv import load_dotenv
load_dotenv()

def connect_mongodb():
    mongo_url = os.environ.get('MONGODB_URL')
    client = MongoClient(mongo_url, server_api=ServerApi('1'))
    mydatabase = client['elecvotes']
    mycollection=mydatabase['user']

    return mycollection

def get_name_relation  ( all_data : list ):
        try:
            sub = '\'s Name'
            particular_username = [s for s in all_data if sub.lower() in s.lower()][0].split()
            # print ( particular_username )
            to_search_father = "Father\'s"
            to_search_husband = "Husband\'s"
            to_search_mother = "Mother\'s"
            relation = "----"
            user_name = "----"

            for i in range (1, len(particular_username)):
                if to_search_father in particular_username[i]:
                    user_name = particular_username[i-1]
                    relation = "father"
                if to_search_husband in particular_username[i]:
                    user_name = particular_username[i-1]
                    relation = "husband"
                if to_search_mother in particular_username[i]:
                    user_name = particular_username[i-1]
                    relation = "mother"

            return (user_name.strip(), relation)
        except:
            print ("Sorry, for the Get_Name_Relation Function")
            return ("----", "----")

def get_relation_name ( all_data : list ):
        to_search = "House Number"
        relation = "undefined"
        for element in all_data :
            if to_search in element :
                relation = (element.split(to_search)[0])
        
        return relation.strip()

def get_house_number ( all_data : list ):
    try :
        house_number = (all_data[-3].strip().split()[0])

        if not house_number.isnumeric():
            return -1
        
        return int(house_number)
    except :
        print ("Continue")
        pass

def extract_all_data_from_image ():
    image_1 = 'page1.jpg'

    img_obj_1 = Image.open(image_1)

    top_left_x = 72 
    top_left_y = 135
    bottom_right_x = 414
    bottom_right_y = 325

    collection_data = connect_mongodb()

    for j in range ( 10 ):
        for i in range ( 3 ):
            sample_obj = img_obj_1.crop((top_left_x,top_left_y, bottom_right_x, bottom_right_y))
            all_data = pytesseract.image_to_string(sample_obj)
            all_data = all_data.replace("\n", " ").strip().split(':')
            house_number = get_house_number(all_data)
            name, relation = get_name_relation (all_data)
            relation_person_name = get_relation_name ( all_data )
            gender = all_data[-1].strip()

            print ( "Name ", name, " Relation ", relation, " name ", relation_person_name, " gender ", gender, " house number ", house_number )
            
            if ( name != "----"):
                record_for_database = {
                    "Name": name,
                    "Relation": relation,
                    "Relative Name": relation_person_name,
                    "Gender": gender,
                    "House Number": house_number
                }

                collection_data.insert_one(record_for_database)

            top_left_x += 501
            bottom_right_x += 513
        
        top_left_y += 198 
        bottom_right_y += 200
        top_left_x = 72
        bottom_right_x = 414

if __name__ == "__main__":
    pages = convert_from_path('/home/nopc/Github-Clones/Image-to-text/Mizoram Electoral Votes.pdf')

    for i in range (3,len(pages)-1):
        print(i)
        pages[i].save('page1.jpg', 'JPEG')
        extract_all_data_from_image()