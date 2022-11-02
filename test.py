import requests
from datetime import datetime

# dentists = []
# response = requests.get("http://localhost:8080/api/service-chatbot")
# data = response.json()
# for x in data['data']:
#     dentists.append(x['name'])
#
# print(dentists)


# Get all services

# services = []
# response = requests.get("http://localhost:8080/api/service-chatbot")
# data = response.json()
# for x in data['data']:
#     services.append(x['ServiceData']['valueVi'])
# print(services)


#Get service description

# response = requests.get("http://localhost:8080/api/service-chatbot")
# data = response.json()
# service = 'Trám răng'
# arr = {}
# for x in data['data']:
#     arr[x['ServiceData']['valueVi']] = x['description']
# print(arr)


#Get service price

# response = requests.get("http://localhost:8080/api/service-chatbot")
# data = response.json()
# price = 'Trám răng'
# arr = []
# for x in data['data']:
#     if (x['ServiceData']['valueVi']) == price :
#         arr.append(x['PriceData']['valueVi'])
# print(arr)


#Get time to do service

# response = requests.get("http://localhost:8080/api/service-chatbot")
# data = response.json()
# timetodo = 'Trám răng'
# arr = {}
# for x in data['data']:
#     arr[x['ServiceData']['valueVi']] = x['timetodo']
# print(arr[timetodo])


# Get doctor by id

# doctor = 'Đoàn Huy'
# response = requests.get("http://localhost:8080/api/get-all-doctors")
# data = response.json()
# id = ''
# for x in data['data']:
#     if (x['firstName'] == doctor):
#         id += str(x['id'])
#
# api = 'http://localhost:8080/api/get-detail-doctor-by-id?id=' + id;
# response2 = requests.get(api)
# data2 = response2.json()
# print(data2['data']['Markdown']['description'])


#Get doctor list

# dentists = []
# response = requests.get("http://localhost:8080/api/get-all-doctors")
# data = response.json()
# for x in data['data']:
#     dentists.append(x['firstName'])
# print(dentists)


# Bien doi tu ten dich vu sang id dich vu de POST api

# response = requests.get("http://localhost:8080/api/service-chatbot")
# data = response.json()
# service = 'Trám răng'
# for x in data['data']:
#     if (x['ServiceData']['valueVi'] == service):
#         id = x['serviceId']
# print(id)


#  Lấy khung giờ trống trong 1 ngày của thằng bác sĩ
# 1 Đầu tiên lấy id nha sĩ từ tên của nha sĩ:
# 2 Kế tiếp chuyển từ ngày đã chọn qua timestamp:
#   2.1 Chuyển từ string sang datetime
#   2.2 Chuyển datetime thành timestamp
# 3 Lấy khung giờ với tham số doctorId và date dưới dạng timestamp

doctor = 'Đoàn Huy'
response = requests.get("http://localhost:8080/api/get-all-doctors")
data = response.json()
for x in data['data']:
    if (x['firstName'] == doctor):
        id = x['id']
print(id)

date_string = "25/08/2021"
date_object = datetime.strptime(date_string, "%d/%m/%Y")
print("date_object =", date_object)

timestamp = datetime.timestamp(date_object)
time = str(timestamp).replace(".0", "") + '000'
print(time)

api = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(id) + '&date=' + time;
response2 = requests.get(api)
data2 = response2.json()
arr = []
for x in data2['data']:
    if (x['currentNumber'] != 1):
        arr.append(x['timeTypeData']['valueVi'])
print(arr)


#Chuyển từ khung giờ ở chatbot sang timeType (T1, T2, T3) trong DB

# time = '9:00 - 10:00'
# if(time == '7:00 - 8:00'):
#     timeChanged = 'T1'
# elif(time == '8:00 - 9:00'):
#     timeChanged = 'T2'
# elif(time == '9:00 - 10:00'):
#     timeChanged = 'T3'
# elif(time == '10:00 - 11:00'):
#     timeChanged = 'T4'
# elif(time == '11:00 - 12:00'):
#     timeChanged = 'T5'
# elif(time == '13:00 - 14:00'):
#     timeChanged = 'T6'
# elif(time == '15:00 - 16:00'):
#     timeChanged = 'T7'
# elif(time == '16:00 - 17:00'):
#     timeChanged = 'T8'
# print(timeChanged)


# Lấy entity là ngày, nhưng post api là timeStamp.

# date_string = "25/08/2021"
# date_object = datetime.strptime(date_string, "%d/%m/%Y")
# print("date_object =", date_object)
#
# timestamp = datetime.timestamp(date_object)
# time = str(timestamp).replace(".0", "") + '000'
# print(time)


# Lấy entity là giới tính (Nam, Nữ), còn post là M hoặ F (Male, Female)

# sex = 'Nữ'
# if(sex == 'Nam'):
#     sexChanged = 'M'
# elif(sex == 'Nữ'):
#     sexChanged = 'F'
# print(sexChanged)