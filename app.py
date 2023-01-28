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
one_drive_direct_link = create_onedrive_directdownload(one_drive_link)
xls = pd.ExcelFile(one_drive_direct_link)
expenses_df = pd.read_excel(xls, 'All_Expenses')
expenses_df.columns = ['Date', 'Particular', 'Category', 'Spend_Type','Total_Amount', 'Spend_Duration', 'Divide_By','Monthly_Amount']
expenses_df = expenses_df[[['Date', 'Particular', 'Category', 'Spend_Type', 'Total_Amount','Spend_Duration', 'Monthly_Amount']]]

def return_excel_data(sheet_name):
    my_dict = {}
    if sheet_name in ['Group_By_Length','Group_By_Type','Group_By_Type_Category']:
        type_df = pd.read_excel(xls, sheet_name)
        for key,value in zip(type_df['Row Labels'],type_df['Sum of Monthly Amount']):
            my_dict[key] = value
        return(my_dict)
    elif sheet_name == 'Annual_Personal_Breakdown':
        type_df = pd.read_excel(xls, sheet_name,header=3)
        for key,value in zip(type_df['Row Labels'],type_df['Sum of Monthly Amount']):
            my_dict[key] = value
        return(my_dict)
    else:        
        type_df = pd.read_excel(xls, sheet_name,header=2)
        for key,value in zip(type_df['Row Labels'],type_df['Sum of Monthly Amount']):
            my_dict[key] = value
        return(my_dict)    

@app.route('/expenses_by_length')
def group_by_length():
    try:
        excel_response = return_excel_data('Group_By_Length')
        return(excel_response)
    except Exception as e:
        return(e)

@app.route('/expenses_by_type')
def group_by_type():
    try:
        excel_response = return_excel_data('Group_By_Type')
        return(excel_response)
    except Exception as e:
        return(e) 

@app.route('/expenses_by_category')
def group_by_category():
    try:
        excel_response = return_excel_data('Group_By_Type_Category')
        return(excel_response)
    except Exception as e:
        return(e) 

@app.route('/annual_expense')
def annual_expense():
    try:
        excel_response = return_excel_data('Amortized_Annual_Expenses')
        return(excel_response)
    except Exception as e:
        return(e) 

@app.route('/monthly_expense')
def monthly_expense():
    try:
        excel_response = return_excel_data('Monthly_Repeated_Expenses')
        return(excel_response)
    except Exception as e:
        return(e) 

@app.route('/one_time_expense')
def one_time_expense():
    try:
        excel_response = return_excel_data('One_Time_Expense')
        return(excel_response)
    except Exception as e:
        return(e)  

@app.route('/personal_expense_breakdown')
def personal_expenses():
    try:
        excel_response = return_excel_data('Annual_Personal_Breakdown')
        return(excel_response)
    except Exception as e:
        return(e)  

@app.route('/pandas')
def pandas_return():
    try:
        results_df = expenses_df.groupby('Spend_Duration')['Monthly_Amount'].sum().reset_index()
        my_dict = {}
        for key,value in zip(results_df['Spend_Duration'],results_df['Monthly_Amount']):
            my_dict[key] = value
        return(my_dict)
    except Exception as e:
        return(e)