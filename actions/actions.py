import mysql.connector as con
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction
import numpy as np
import requests
from datetime import datetime


class booking_form(Action):

    def name(self) -> Text:
        return "booking_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["service", "clinic", "customer",
                          "phone", "email", "date", "time", "note"]


class SaveInfoBook(Action):
    def name(self) -> Text:
        return "save_info_book"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict):
        service = tracker.get_slot("service")
        clinic = tracker.get_slot("clinic")
        customer = tracker.get_slot("customer")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        note = tracker.get_slot("note")
        return [SlotSet("service_booked", service),
                SlotSet("clinic_booked", clinic),
                SlotSet("customer_booked", customer),
                SlotSet("phone_booked", phone),
                SlotSet("date_booked", email),
                SlotSet("date_booked", date),
                SlotSet("time_booked", time),
                SlotSet("note_booked", note)]


class submit_form_booking(Action):
    def name(self) -> Text:
        return "action_submit_form"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            template="utter_slots_values", gender=tracker.get_slot("gender"), service_book=tracker.get_slot("service"),
            clinic_book=tracker.get_slot("clinic"), customer_book=tracker.get_slot("customer"),
            phone_book=tracker.get_slot("phone"), email_book=tracker.get_slot("email"),
            date_book=tracker.get_slot("date"), time_book=tracker.get_slot("time"), note_book=tracker.get_slot("note")
        )

        select = ["Đồng ý đặt lịch", "Bỏ đặt lịch"]
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/book_intent{\"book_check\": \"' + x + '\"}'})

        dispatcher.utter_button_message(" ", button)

        return []


class insert_form_booking(Action):
    def name(self) -> Text:
        return "action_insert_val_form"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:

        book_check = tracker.get_slot("book_check")
        print('book check: ', book_check)

        if (book_check == "Đồng ý đặt lịch"):
            service = tracker.get_slot("service")
            clinic = tracker.get_slot("clinic")
            customer = tracker.get_slot("customer")
            phone = tracker.get_slot("phone")
            email = tracker.get_slot("email")
            note = tracker.get_slot("note")
            gender = tracker.get_slot("gender")

            if (gender == 'Anh'):
                genderChanged = 'Nam'
            elif (gender == 'Chị'):
                genderChanged = 'Nữ'
            print(genderChanged)
            #################################################
            # lay id dich vu
            # response = requests.get(
            #     "http://localhost:5000/service-chatbot")
            # data = response.json()
            # for x in data:
            #     if (x['ServiceData']['valueVi'] == service):
            #         idService = x['serviceId']
            # print(idService)

            # convert ngay
            date = tracker.get_slot("date")
            dateChanged = str(datetime.strptime(date, "%d/%m/%Y"))

            # layID phòng khám
            response = requests.get(
                "http://localhost:5000/clinics")
            data = response.json()
            for x in data:
                if (x['CLINIC_NAME'] == clinic):
                    idClinic = x['CLINIC_ID']
            print(idClinic)

            # lay Tên phòng khám
            response = requests.get("http://localhost:5000/clinics")
            data = response.json()
            for x in data:
                if (x['CLINIC_ID'] == idClinic):
                    addressClinic = x['CLINIC_ADDRESS']
            print(addressClinic)

            # timeChanged
            time = tracker.get_slot("time")
            timeChanged = 'T1'

            if (time == '8h30-9h00'):
                timeChanged = 'T2'
            elif (time == '9h00-9h30'):
                timeChanged = 'T3'
            elif (time == '9h30-10h00'):
                timeChanged = 'T4'
            elif (time == '10h00-10h30'):
                timeChanged = 'T5'
            elif (time == '10h30-11h00'):
                timeChanged = 'T6'
            elif (time == '11h00-11h30'):
                timeChanged = 'T7'
            elif (time == '13h00-13h30'):
                timeChanged = 'T8'
            elif (time == '13h30-14h00'):
                timeChanged = 'T9'
            elif (time == '14h00-14h30'):
                timeChanged = 'T10'
            elif (time == '14h30-15h00'):
                timeChanged = 'T11'
            elif (time == '15h00-15h30'):
                timeChanged = 'T12'
            elif (time == '15h30-16h00'):
                timeChanged = 'T13'
            elif (time == '16h00-16h30'):
                timeChanged = 'T14'
            elif (time == '16h30-17h00'):
                timeChanged = 'T15'
            elif (time == '17h00-17h30'):
                timeChanged = 'T16'

            print(timeChanged)
            # apipost
            booking = {"BOOKING_CLINIC": idClinic, "BOOKING_TIMESLOT": timeChanged, "BOOKING_DATE": dateChanged, "BOOKING_EMAIL": email, "BOOKING_STATUS": 0,
                       "BOOKING_CUSTOMER_NAME": customer, "BOOKING_CUSTOMER_SEX": genderChanged, "BOOKING_SERVICE": service, "BOOKING_CONTACT_PHONE": phone, "BOOKING_NOTE": note}
            response = requests.post(
                "http://localhost:5000/bookings", data=booking)
            # print (str(response.content)) == response.text
            booking2 = {"BOOKING_DATE": date,
                        "BOOKING_NOTE": note,
                        "BOOKING_EMAIL": email,
                        "BOOKING_CUSTOMER_NAME": customer,
                        "BOOKING_CLINIC_NAME": clinic,
                        "BOOKING_TIMESLOT_NAME": time,
                        "BOOKING_CLINIC_ADDRESS": addressClinic,
                        "BOOKING_CUSTOMER_MALE": genderChanged,
                        "BOOKING_SERVICE": service}
            res = response.json()
            if (res['message'] == "Insert success!"):
                response2 = requests.post(
                    "http://localhost:5000/bookings/sendMail", data=booking2)
                dispatcher.utter_message(
                    "Đặt lịch thành công, quý khách có thể kiểm tra tin nhắn xác nhận đặt lịch trong email giúp em nhé!")
            else:
                dispatcher.utter_message(
                    "Đặt lịch không thành công, vui lòng đặt lại !")
        if (book_check == "Bỏ đặt lịch"):
            dispatcher.utter_message("Đã huỷ đặt lịch")


class AskSlotServiceAction(Action):
    def name(self) -> Text:
        return "action_ask_service"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        services = []
        response = requests.get("http://localhost:5000/services")
        data = response.json()
        for x in data:
            services.append(x['SERVICE_NAME'])
        print(services)
        button = []
        gender = tracker.get_slot('gender')
        dispatcher.utter_message(
            gender + ' vui lòng cho chọn dịch vụ muốn khám')
        dispatcher.utter_message(
            "Hoặc nếu như " + gender + " muốn thực hiện nhiều dịch vụ thì vui lòng nhập vào bên dưới giúp em nhé!")
        for x in services:
            button.append(
                {"title": x, "payload": '/give_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []


class AskSlotclinicAction(Action):
    def name(self) -> Text:
        return "action_ask_clinic"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        clinics = []
        response = requests.get("http://localhost:5000/clinics")
        data = response.json()
        for x in data:
            clinics.append(x['CLINIC_NAME'])
        print(clinics)
        button = []
        gender = tracker.get_slot('gender')
        dispatcher.utter_message(
            gender + ' vui lòng cho chọn nha khoa muốn khám')
        for x in clinics:
            button.append(
                {"title": "" + x, "payload": '/give_clinic{\"clinic\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class AskSlotTimeAction(Action):
    def name(self) -> Text:
        return "action_ask_time"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        date = tracker.get_slot("date")
        dateChanged = str(datetime.strptime(date, "%d/%m/%Y"))
        clinic = tracker.get_slot("clinic")
        # Lấy ID phòng khám
        response = requests.get("http://localhost:5000/clinics")
        data = response.json()
        for x in data:
            if (x['CLINIC_NAME'] == clinic):
                idClinic = x['CLINIC_ID']
        print(idClinic)

        # lấy danh sách giờ đã được đặt
        api = "http://localhost:5000/clinicSchedule/bookedTimeSlot/" + \
            str(idClinic) + "/" + dateChanged[0:10]
        response = requests.get(api)
        data = response.json()
        arr = []
        for x in data:
            arr.append(x['booking_timeslot'])

        bookedTimeslots = []
        for b in arr:
            if (b == 'T1'):
                bookedTimeslots.append('8h00-8h30')
            elif (b == 'T2'):
                bookedTimeslots.append('8h30-9h00')
            elif (b == 'T3'):
                bookedTimeslots.append('9h00-9h30')
            elif (b == 'T4'):
                bookedTimeslots.append('9h30-10h00')
            elif (b == 'T5'):
                bookedTimeslots.append('10h00-10h30')
            elif (b == 'T6'):
                bookedTimeslots.append('10h30-11h00')
            elif (b == 'T7'):
                bookedTimeslots.append('11h00-11h30')
            elif (b == 'T8'):
                bookedTimeslots.append('13h00-13h30')
            elif (b == 'T9'):
                bookedTimeslots.append('13h30-14h00')
            elif (b == 'T10'):
                bookedTimeslots.append('14h00-14h30')
            elif (b == 'T11'):
                bookedTimeslots.append('14h30-15h00')
            elif (b == 'T12'):
                bookedTimeslots.append('15h00-15h30')
            elif (b == 'T13'):
                bookedTimeslots.append('15h30-16h00')
            elif (b == 'T14'):
                bookedTimeslots.append('16h00-16h30')
            elif (b == 'T15'):
                bookedTimeslots.append('T16h30-17h00')
            elif (b == 'T16'):
                bookedTimeslots.append('17h00-17h30')

        timeSlots = ['8h00-8h30', '8h30-9h00',
                     '9h00-9h30', '9h30-10h00', '10h00-10h30', '10h30-11h00', '11h00-11h30', '13h00-13h30', '13h30-14h00', '14h00-14h30', '14h30-15h00',
                     '15h00-15h30', '15h30-16h00', '16h00-16h30', '16h30-17h00', '17h00-17h30']

        availableTimeslots = set(timeSlots) ^ set(bookedTimeslots)

        # # convert ngay
        # date = tracker.get_slot("date")
        # date_object = datetime.strptime(date, "%d/%m/%Y")
        # print("date_object =", date_object)
        # timestamp = datetime.timestamp(date_object)
        # dateChanged = str(timestamp).replace(".0", "") + '000'
        # print(dateChanged)

        # # lay khung gio
        # api = 'http://localhost:5000/get-schedule-doctor-by-date?doctorId=' + str(
        #     idClinic) + '&date=' + dateChanged
        # response2 = requests.get(api)
        # data2 = response2.json()
        # arr = []  # listtime
        # for x in data2['data']:
        #     if (x['currentNumber'] != 1):
        #         arr.append(x['timeTypeData']['valueVi'])
        # print(arr)

        if not availableTimeslots:
            dispatcher.utter_message('Ngày vừa chọn không có khung giờ trống')
            dispatcher.utter_message('Xin vui lòng chọn ngày khác!')
        else:
            dispatcher.utter_message(
                'Quý khách xin vui lòng chọn thời gian đến khám bệnh:')
        button = []
        for x in availableTimeslots:
            button.append(
                {"title": x, "payload": '/give_time{\"time\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []


class AskSlotNoteAction(Action):
    def name(self) -> Text:
        return "action_ask_note"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(gender + ' có lưu ý gì không ạ')
        dispatcher.utter_message("Nếu có lưu ý, vui lòng nhập phía dưới")
        select2 = ["Không"]
        button = []
        for x in select2:
            button.append(
                {"title": x, "payload": '/book_note{\"note\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class Greet(Action):

    def name(self) -> Text:
        return "rep_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'Dạ để tiện xưng hô, anh/chị vui lòng chọn giúp em danh xưng mình muốn được gọi nhé:')
        select = ['Anh', 'Chị']
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/get_gender{\"gender\": \"' + x + '\"}'})

        dispatcher.utter_button_message(" ", button)
        return []


class Gender(Action):

    def name(self) -> Text:
        return "rep_get_gender"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Xin chào ' + service + ' đã đến với Thế Giới Nha Khoa')
        return []


class Ask(Action):

    def name(self) -> Text:
        return "rep_ask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Dạ ' + gender + ' vui lòng chọn dịch vụ mình muốn được tư vấn ạ:')

        services = []
        response = requests.get("http://localhost:5000/services")
        data = response.json()
        for x in data:
            services.append(x['SERVICE_NAME'])
        button = []
        for x in services:
            button.append(
                {"title": x, "payload": '/ask_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []


class AskService(Action):

    def name(self) -> Text:
        return "rep_ask_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://localhost:5000/services")
        data = response.json()
        service = tracker.get_slot("service_ask")
        serviceChanged = service.lower()
        arr = {}
        for x in data:
            arr[x['SERVICE_NAME']] = x['SERVICE_DESCRIPTION']
        dispatcher.utter_message(arr[serviceChanged])

        return []


class AskPrice(Action):

    def name(self) -> Text:
        return "rep_ask_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://localhost:5000/services")
        data = response.json()
        price = tracker.get_slot('price')
        priceChanged = price.lower()
        arr = {}
        for x in data:
            arr[x['SERVICE_NAME']] = x['SERVICE_PRICE']
        # print(arr)
        # print(arr[tracker.get_slot('price')])
        dispatcher.utter_message(arr[priceChanged])
        return []


class AskTimeToDo(Action):

    def name(self) -> Text:
        return "rep_ask_timetodo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("http://localhost:5000/services")
        data = response.json()
        timetodo = tracker.get_slot('timetodo')
        timetodoChanged = timetodo.lower()
        arr = {}
        for x in data:
            arr[x['SERVICE_NAME']] = x['SERVICE_TIMETODO']
        dispatcher.utter_message(arr[timetodoChanged])

        return []


class AskAddress(Action):

    def name(self) -> Text:
        return "rep_ask_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("http://localhost:5000/clinics")
        data = response.json()
        address = tracker.get_slot('address')
        arr = {}
        for x in data:
            arr[x['CLINIC_NAME']] = x['CLINIC_ADDRESS']
        dispatcher.utter_message(arr[address])

        return []


class AskListClinic(Action):

    def name(self) -> Text:
        return "rep_ask_list_clinic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'Dạ đây là danh sách phòng khám có ở Thế Giới Nha Khoa ạ:')
        clinics = []
        response = requests.get("http://localhost:5000/clinics")
        data = response.json()
        for x in data:
            clinics.append(x['CLINIC_NAME'])
        button = []
        for x in clinics:
            # button.append(
            #     {"title": x, "payload": '/ask_dental{\"dental\": \"' + x + '\"}'})
            x = "Nha khoa " + x
            button.append(x)
        dispatcher.utter_button_message(" ", button)
        return []


class Goodbye(Action):
    def name(self) -> Text:
        return "rep_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Dạ xin chào tạm biệt ' + service.lower() + '. Hẹn gặp lại ' + service.lower() + ' ạ!')
        return []
