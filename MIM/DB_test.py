import mysql.connector
import random
import datetime


connection = mysql.connector.connect(
 host="localhost",
 user="root",
 password="Debsirin_135",
 database="software_onboard"
)

db_cursor = connection.cursor()
#####################################################################
add_pre_exam_list = "INSERT INTO pre_exam_list (ID) VALUES (%(ID)s)"
# for i in range(100):
#   data_pre_exam_list = {
#     'ID': 'Presciption_ID_06' + str(i)
#   }

#   db_cursor.execute(add_pre_exam_list,data_pre_exam_list)
# connection.commit()
#####################################################################
add_medicine_info = "INSERT INTO medicine_info (MedicineName,Picture,Info) VALUES (%(MedicineName)s, %(Picture)s, %(Info)s)"
medicine_stock_list = ['Betaglucan', 'Brilinta', 'Controloc', 'Dexilant', 'Ezetrol', 'K-zuva', 'Trajenta']
path = ["Medicine_Info/Betaglucan.jpg","Medicine_Info/Brilinta.jpg","Medicine_Info/Controloc.jpg","Medicine_Info/Dexilant.jpg","Medicine_Info/Ezetrol.jpg","Medicine_Info/Kzuva.jpg","Medicine_Info/Trajenta.jpg"]
Infopath = ["Medicine_Info/Dummy.txt","Medicine_Info/Dummy.txt","Medicine_Info/Dummy.txt","Medicine_Info/Dummy.txt","Medicine_Info/Dummy.txt","Medicine_Info/Dummy.txt","Medicine_Info/Dummy.txt"]

# for i in range(len(medicine_stock_list)):
#   with open(path[i],'rb') as file:
#         binarydata = file.read()

#   with open(Infopath[i],'rt') as text_file:
#         Info_text = text_file.readline()

#   data_medicine_info = {
#     'MedicineName': medicine_stock_list[i],
#     'Picture': binarydata,
#     'Info': Info_text
#   }
#   db_cursor.execute(add_medicine_info,data_medicine_info)

# connection.commit()
################################################################################################
add_pre_exam_pres = "INSERT INTO pre_exam_prescript (Pre_exam_ID,MedicineName,SetQuentity) VALUES (%(Pre_exam_ID)s, %(MedicineName)s, %(SetQuentity)s)"
# for j in range(100):
#     row_count = random.randint(3,7)
#     Medicine_list_pres = random.sample(medicine_stock_list,row_count)
#     SetQuentity_list = random.sample(range(1,10), row_count)
#     Pre_exam_ID = 'Presciption_ID_06' + str(j)

#     for i in range(len(Medicine_list_pres)):
#       data_pre_exam_pres = {
#         'Pre_exam_ID': Pre_exam_ID,
#         'MedicineName': Medicine_list_pres[i],
#         'SetQuentity': SetQuentity_list[i],
#       }
      
#       db_cursor.execute(add_pre_exam_pres,data_pre_exam_pres)

# connection.commit()
#############################################################################################
query_medicine = "SELECT MedicineName,SetQuentity FROM pre_exam_prescript WHERE Pre_exam_ID = %(Query_index)s" 
query_setQuentity = "SELECT SetQuentity FROM pre_exam_prescript WHERE Pre_exam_ID = %(Query_index)s" 
Query_data_Pres_exam_ID = {
    'Query_index': 'A1'
  }

# db_cursor.execute(query_medicine,Query_data_Pres_exam_ID)
# Medicine_result = db_cursor.fetchall()

# db_cursor.execute(query_setQuentity,Query_data_Pres_exam_ID)
# SetQuentity_result = db_cursor.fetchall()

# print(Medicine_result[0][1])
# print(SetQuentity_result)
###############################################################################################
del_pre_exam_ID = "DELETE FROM pre_exam_list WHERE ID = %(Del_ID)s"
deldata_pre_exam_ID = {
  'Del_ID': 'A2'
}

# db_cursor.execute(del_pre_exam_ID,deldata_pre_exam_ID)
# connection.commit()
##############################################################################################
del_Medicine_Info = "DELETE FROM medicine_info WHERE MedicineName = %(Del_Medicine)s"
del_Medicine_List = ['AAA','BBB','CCC']

# for i in range(len(del_Medicine_List)):
#   deldata_Medicine_Info = {
#     'Del_Medicine': del_Medicine_List[i]
#   }
#   db_cursor.execute(del_Medicine_Info,deldata_Medicine_Info)

# connection.commit()
##############################################################################################
Update_pre_exam_ID = "UPDATE pre_exam_list SET ID = %(New_ID)s WHERE ID = %(Old_ID)s"
Updatedata_pre_exam_ID = {
  'New_ID': 'A2',
  'Old_ID': 'A1'
}

# db_cursor.execute(Update_pre_exam_ID,Updatedata_pre_exam_ID)
# connection.commit()
################################################################################################
add_exam_list = "INSERT INTO exam_list (ID,Status,DecisionDay,DecisionTime) VALUES (%(ID)s, %(Status)s, %(DecisionDay)s, %(DecisionTime)s)"

# data_exam_list = {
#     'ID': "Presciption_ID_021",
#     'Status': "Accept",
#     'DecisionDay': datetime.date.today(),
#     'DecisionTime': datetime.datetime.now().time(),
#   }
  
# db_cursor.execute(add_exam_list,data_exam_list)

# connection.commit()
#############################################################################################
timefilter_query_Examination_List = "SELECT ID,Status,DecisionDay,DecisionTime FROM exam_list WHERE DecisionDay Between %(InitDate)s AND %(FinalDate)s AND DecisionTime Between %(InitTime)s AND %(FinalTime)s" 
timefilter_query_data_Examination_List = {
    'InitDate': '2024-04-15',
    'FinalDate': '2024-04-18',
    'InitTime': '10:00:00',
    'FinalTime': '22:00:00'
  }

# db_cursor.execute(timefilter_query_Examination_List,timefilter_query_data_Examination_List)
# data = db_cursor.fetchall()
# print(data)
################################################################################################
add_Useracount = "INSERT INTO useraccount (Username,Password) VALUES (%(U)s, %(P)s)"

# data_add_Useracount = {
#     'U': "Earthy",
#     'P': "Kuay"
#   }
  
# db_cursor.execute(add_Useracount,data_add_Useracount)

# connection.commit()
