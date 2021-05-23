import  time
from werkzeug.security import check_password_hash, generate_password_hash
from healingpaws import db
from healingpaws.models import House
from sqlalchemy import or_,and_
import os
from healingpaws.tools import read_pkl
import datetime

def update_data():
    path = r"D:\Programmer\Py3\私人项目\33_splider_house\splider\pkl"
    house_lists = []

    # House.query.delete()
    # db.session.commit()
    # exit()
    key_lists = [
         "id","beds","baths","area",
         "price","position","img",
         "latitude","longitude","status","broker_name",
         "pub_time",
                 ]

    def get_datetime(msg):
        try:
            pub_time = int(msg.get("hdpData",{}).get("homeInfo",{}).get("timeOnZillow",0) / 1000)
            pub_time = datetime.datetime.fromtimestamp(pub_time)
        except Exception as e:
            pub_time = datetime.datetime.now()
        return pub_time

    for pkl in os.listdir(path):
        # pkl_path = os.path.join(path,pkl)
        msg = read_pkl(path,pkl)
        # print("pub_time: ",get_datetime(msg))
        # exit()
        zpid = msg.get("zpid")
        beds = msg.get("beds")
        baths = msg.get("baths")
        area = msg.get("area")
        unformattedPrice = msg.get("unformattedPrice")
        address = msg.get("address")
        latitude = msg.get("latLong",{}).get("latitude")
        longitude = msg.get("latLong", {}).get("longitude")
        status = msg.get("statusText")
        broker_name = msg.get("brokerName")
        pub_time = get_datetime(msg)
        cur_value = [zpid, beds, baths, area,
                     unformattedPrice,address,
                     f"{zpid}.jpg",latitude, longitude,
                     status,broker_name,
                     pub_time,
                    ]
        if not all(cur_value):
            continue
        house_lists.append({key_lists[index]:value for index,value in enumerate(cur_value)})
        #house = House(id=2,beds=1,baths=2,area=3,price=4,position="5",img="6",latitude=7,longitude=8,status='Condo for sale')
    # db.session.add(house)
    # db.session.commit()
    db.session.bulk_insert_mappings(House,house_lists)
    db.session.commit()

if __name__ == "__main__":
    update_data()