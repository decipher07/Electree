from PIL import Image 
import pytesseract

from pymongo import MongoClient
from pdf2image import convert_from_path


def connect_mongodb():
    client = MongoClient('localhost', 27017)
    mydatabase = client['elecvotes']
    mycollection=mydatabase['user']

    rec = {
        'title': 'MongoDB and Python', 
        'description': 'MongoDB is no SQL database', 
        'tags': ['mongodb', 'database', 'NoSQL'], 
        'viewers': 104
    }
    
    # inserting the data in the database
    rec = mycollection.insert_one(rec)

    print (rec)

def get_name_relation  ( all_data : list ):
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

        return (user_name, relation)

def get_relation_name ( all_data : list ):
        to_search = "House Number"
        relation = "undefined"
        for element in all_data :
            if to_search in element :
                relation = (element.split(to_search)[0])
        
        return relation

pages = convert_from_path('/home/nopc/Github-Clones/Image-to-text/Mizoram Electoral Votes.pdf')

# for i in range (3):
#     pages[i].save('page1.jpg', 'JPEG')

image_1 = 'page1.jpg'

img_obj_1 = Image.open(image_1)

# img_obj_1.show()

top_left_x = 72 
top_left_y = 135
bottom_right_x = 414
bottom_right_y = 325

for j in range ( 10 ):
    for i in range ( 3 ):
        sample_obj = img_obj_1.crop((top_left_x,top_left_y, bottom_right_x, bottom_right_y))
        all_data = pytesseract.image_to_string(sample_obj)
        all_data = all_data.replace("\n", " ").strip().split(':')
        print(all_data)
        # print(all_data[-1], all_data[-3])
        name, relation = get_name_relation (all_data)
        relation_person_name = get_relation_name ( all_data )
        print ( "Name ", name, " Relation ", relation, " name", relation_person_name )
        
        top_left_x += 501
        bottom_right_x += 513
    
    top_left_y += 198 
    bottom_right_y += 200
    top_left_x = 72
    bottom_right_x = 414








# for i in range ( 3 ):
#     sample_obj = img_obj_1.crop((top_left_x,top_left_y, bottom_right_x, bottom_right_y))
#     print (pytesseract.image_to_string(sample_obj))
#     top_left_x += 501
#     bottom_right_x += 513





# top_left_y = 333
# bottom_right_y = 525
# top_left_x = 72 
# bottom_right_x = 414

# for i in range ( 3 ):    
#     sample_obj = img_obj_1.crop((top_left_x,top_left_y, bottom_right_x, bottom_right_y))
#     print (pytesseract.image_to_string(sample_obj))
#     top_left_x += 501
#     bottom_right_x += 513



# top_left_y = 333 - 135 = 198
# bottom_right_y = 525 - 325 = 200


# sample_obj = img_obj_1.crop((0,0, 350, 225))

# sample_obj_2 = img_obj_1.crop((585,0, 930, 225))

# print (pytesseract.image_to_string(sample_obj))
# print (pytesseract.image_to_string(sample_obj_2))

# sample_obj.show()
# sample_obj_2.show()
# img_obj_1.show()

# top_left_x = 0 
# top_left_y = 0
# bottom_right_x = 350
# bottom_right_y = 225

# for i in range ( 3 ):
#     sample_obj = img_obj_1.crop((top_left_x,top_left_y, bottom_right_x, bottom_right_y))
#     print (pytesseract.image_to_string(sample_obj))
#     top_left_x += 585
#     bottom_right_x += 580

