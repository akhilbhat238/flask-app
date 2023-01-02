import pandas as pd
import base64
from openpyxl import load_workbook
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def create_onedrive_directdownload (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl

one_drive_link = "https://1drv.ms/x/s!AtIkLugUST4_gbt9Bp4t95oAEJXkbA?e=OVhXnA"

@app.route('/')
def hello_world():
    try:
        # one_drive_link = "https://1drv.ms/x/s!AtIkLugUST4_gbt9Bp4t95oAEJXkbA?e=OVhXnA"
        one_drive_direct_link = create_onedrive_directdownload(one_drive_link)
        xls = pd.ExcelFile(one_drive_direct_link)
        type_df = pd.read_excel(xls, 'Group_By_Type')
        response = type_df.set_index("Row Labels").T.to_dict('list')
        return(response)
    except Exception as e:
        # 
        return(e)