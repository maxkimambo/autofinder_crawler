from message_queue import MessageQueue
import downloader as dwn 

queue = MessageQueue()

## Starting consumer 
queue.start_consumer(dwn.process_message) 


## Expected message format 
# {
#     "vehicle_thumbnails": [
#         "https://srv1.sbtjapan.com/photo/F0000/3000/MF3332/f.jpg?var=1507107710",
#         "https://srv1.sbtjapan.com/photo/F0000/3000/MF3332/r.jpg?var=1507107710",
#         "https://srv1.sbtjapan.com/photo/F0000/3000/MF3332/2.jpg?var=1507107710",
#         "https://srv1.sbtjapan.com/photo/F0000/3000/MF3332/3.jpg?var=1507107710"
#     ],
#     "_values": {
#         "vehicle_drive": "2WD",
#         "vehicle_body": "Hatchback",
#         "vehicle_title": "TOYOTA RAUM 2006/9 CBA-NCZ20",
#         "vehicle_price_cif": "N",
#         "vehicle_accessories": "",
#         "vehicle_engine": "1,490cc",
#         "internal_id": "SBT-MF3332",
#         "vehicle_make": "TOYOTA RAUM 2006/9 CBA-NCZ20",
#         "vehicle_mileage": "82,000",
#         "vehicle_year": "2006/9",
#         "vehicle_doors": "5",
#         "vehicle_color": "Blue(L)",
#         "vehicle_model": "\r\n                              YOKOHAMA - JAPAN                          ",
#         "vehicle_steering": "RHD",
#         "vehicle_seats": "5",
#         "vehicle_transmission": "AT",
#         "vehicle_price_fob": "",
#         "vehicle_description": "\r\n                  RHD PETROL 82,000km AT 2WD 5door 5seats PS, AC, AB, ABS, PW              ",
#         "id": "MF3332",
#         "vehicle_fuel": "PETROL"
#     }
# }
