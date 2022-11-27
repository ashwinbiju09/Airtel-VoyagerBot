import http
from flask import Flask, request
import requests
import json
import time
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from collections import defaultdict
from googleplaces import GooglePlaces, types, lang
from geopy.geocoders import Nominatim

chats = defaultdict(list)

app = Flask(__name__)

error = f'Oops ! I guess I\'m mystified right now 😵‍💫 \n\nPlease enter *Menu* or *hi* so I\'ll assist you in advancing 😬'

cont = f'\n\n -- To continue enter *Menu* or *Hi* 😁 \n Or enter *End* to end conversation ! 🥺 '


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/bot', methods=['GET','POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    print(chats)

    # Option A
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'A':
            loc = Nominatim(user_agent="GetLoc")
            # entering the location name
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 1000,types =[types.TYPE_LODGING])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    #option B

    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'B':
            msg.body('Enter your destination 📍')
            responded = True

    if len(chats[request.values["WaId"]]) >= 2:
        if chats[request.values["WaId"]][-2] == 'B':
            msg.body('Enter date of travel in given format *YYYY-MM-DD*')
            responded = True

    if len(chats[request.values["WaId"]]) > 2:
        if chats[request.values["WaId"]][-3] == 'B':
            try :
                date = incoming_msg
                source = chats[request.values["WaId"]][-2].capitalize()
                destination = chats[request.values["WaId"]][-1].capitalize()

                file = open("E:/IQ/dataset.txt", encoding="utf8")
                data = file.read()
                dataArr = data.split(":")
                sourceiata = dataArr[dataArr.index(source) + 1]
                destinationiata = dataArr[dataArr.index(destination) + 1]

                url = f'https://app.goflightlabs.com/search-all-flights?access_key=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYjcxOGQ2NDBhMzI1OWM1NTJkZDRhMmYzZjhjYTI2NDJhZWQzZmU1OWQ3OTY1MDAwMWRmMjc4OTYyNjhmNzg3ZDdjMTNmYjZlMDlmZmEyN2IiLCJpYXQiOjE2Njk0ODQ3OTMsIm5iZiI6MTY2OTQ4NDc5MywiZXhwIjoxNzAxMDIwNzkzLCJzdWIiOiIxOTAwOCIsInNjb3BlcyI6W119.gBrmXIE7mUoDAWDv2VevfDBsiTcdA3FDKitfQ_85jIZ7KJHoZVEE3qGZBwwfD_gbBMSu4f0-NuyISAC2LJVIHw&adults=1&origin={sourceiata}&destination={destinationiata}&departureDate={date}&limit=3'
                r = requests.request("GET", url)
                value = r.json()
                print(value)
                data = value["data"]["results"]
                values = ""
                for i in range(3):
                    item = data[i]
                    fromCity = item["legs"][0]["origin"]["name"]
                    toCity = item["legs"][0]["destination"]["name"]
                    arrival = item["legs"][0]["arrival"]
                    departure = item["legs"][0]["departure"]
                    flight = item["legs"][0]["carriers"]["marketing"][0]["name"]
                    flightnum = item["legs"][0]["segments"][0]["flightNumber"]
                    duration = item["legs"][0]["segments"][0]["durationInMinutes"]
                    text = f'From : *{fromCity}* \nTo : *{toCity}* \nFlight : *{flight}* \nFlight number : *{flightnum}* \nArrival : *{arrival}* \nDeparture : *{departure}* \nDuration : *{duration}* \n '
                    values += text
                    values += "\n"
                msg.body(f' {values} \n{cont} ')
                print(values)
                responded = True
            except :
                msg.body(error)
                responded = True

    # option E
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'E':

            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 3000,types =[types.TYPE_HOSPITAL])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    # option F
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'F':

            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_POLICE])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    # option G 
    if chats[request.values["WaId"]] :
        if chats[request.values["WaId"]][-1] == 'G':
                msg.body('Enter currency to be converted 💲')
                responded = True

    if len(chats[request.values["WaId"]]) >= 2:
         if chats[request.values["WaId"]][-2] == 'G':
                msg.body('Enter amount💲')
                responded = True
        
    if len(chats[request.values["WaId"]]) > 2:
         if chats[request.values["WaId"]][-3] == 'G':
                amnt = incoming_msg
                current = chats[request.values["WaId"]][-2].upper()
                convert = chats[request.values["WaId"]][-1].upper()

                url = "https://currency-converter-by-api-ninjas.p.rapidapi.com/v1/convertcurrency"
                querystring = {"have":{current},"want":{convert},"amount":{amnt}}
                headers = {
                    "X-RapidAPI-Key": "0f37a329dbmsh3596deb565d11ddp13d08ejsn4ca2bedf2c96",
                    "X-RapidAPI-Host": "currency-converter-by-api-ninjas.p.rapidapi.com"
                }

                r = requests.request("GET", url, headers=headers, params=querystring)
                value = r.json()
                text = f' *Conversion Details* \n{value["old_currency"]} : {value["old_amount"]} Converted to {value["new_currency"]} : {value["new_amount"]} \n{cont}  '
                msg.body(text)
                msg.media('https://user-images.githubusercontent.com/118819185/204077246-1421948e-a188-48c7-a8a4-a59ad46179af.jpeg')
                responded = True

    # ATM
    if chats[request.values["WaId"]]:
        if chats[request.values["WaId"]][-1] == 'O':
            msg.body('Enter your location 📍')
            responded = True
    
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '1') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_ATM])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    # Bus Station
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '2') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_BUS_STATION])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    # Railway Station
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '3') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_TRAIN_STATION])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    # Pharmacy
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '4') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_PHARMACY])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 
        
    # Restraunt
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'O') and (chats[request.values["WaId"]][-1] == '5') :
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(f'{incoming_msg}')
            API_KEY = 'AIzaSyDbs5dkx8XyPrT_XwynbaLhz-hX1jr50Ak'
            google_places = GooglePlaces(API_KEY)

            query_result = google_places.nearby_search(
                lat_lng ={'lat': getLoc.latitude, 'lng': getLoc.longitude},radius = 5000,types =[types.TYPE_RESTAURANT])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            msg.body('\n'.join(f"{place.name}\nhttp://maps.google.com/maps?q={place.geo_location['lat']},{place.geo_location['lng']}\n" for place in query_result.places))
            t=f'\n\n{cont}'
            msg.body(t)
            responded = True 

    # Train Status
    if chats[request.values["WaId"]]:
        if (chats[request.values["WaId"]][-1] == 'C') :
            msg.body('Enter your train number / Enter your PNR number to check train status  ')
            responded = True


    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'C') and (chats[request.values["WaId"]][-1] == '1') :
            try :
                url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
                querystring = {"trainNo":{incoming_msg}}
                headers = {
                    "X-RapidAPI-Key": "0f37a329dbmsh3596deb565d11ddp13d08ejsn4ca2bedf2c96",
                    "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
                }
                r = requests.request("GET", url, headers=headers, params=querystring)
                value = r.json()
                value1 = value["data"]["train_number"]
                value2 = value["data"]["train_name"]
                value3 = value["data"]["source"]
                value4 = value["data"]["destination"]
                value5 = value["data"]["new_message"]
                text = f'*Train Details* \n\n 1. Train number : *{value1}* \n 2. Train name : *{value2}* \n 3. Source : *{value3}* \n 4. Destination : *{value4}* \n 5. Addtional Information : *{value5}* \n{cont} '
                msg.body(text)
                msg.media('https://user-images.githubusercontent.com/118819185/204075125-5a7aef3c-f4d8-4c1a-9b23-ceba67e81334.jpg')
                responded = True
            
            except :
                msg.body(error)
                responded = True

    # Train Schedule
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'C') and (chats[request.values["WaId"]][-1] == '2') :

            try : 

                url = "https://irctc1.p.rapidapi.com/api/v1/getTrainSchedule"
                querystring = {"trainNo":{incoming_msg}}
                headers = {
                    "X-RapidAPI-Key": "0f37a329dbmsh3596deb565d11ddp13d08ejsn4ca2bedf2c96",
                    "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
                }
                r = requests.request("GET", url, headers=headers, params=querystring)
                value = r.json()
                x = value["data"]["route"]
                values = ""
                for i in range (len(x)):
                    name = x[i]["station_name"]
                    platform = x[i]["platform_number"]
                    if platform !=0 :
                        values += "📍"+ name + " - Platform number : " +  str(platform)
                        values += "\n"
                msg.body(f'{values} \n{cont} ')
                msg.media('https://user-images.githubusercontent.com/118819185/204075125-5a7aef3c-f4d8-4c1a-9b23-ceba67e81334.jpg')
                responded = True
            
            except :
                msg.body(error)
                responded = True

    # PNR Status
    if len(chats[request.values["WaId"]]) >= 2:
        if (chats[request.values["WaId"]][-2] == 'C') and (chats[request.values["WaId"]][-1] == '3') :

            url = f"https://pnr-status-indian-railway.p.rapidapi.com/pnr-check/{incoming_msg}"
            print(incoming_msg)
            headers = {
                "X-RapidAPI-Key": "0f37a329dbmsh3596deb565d11ddp13d08ejsn4ca2bedf2c96",
                "X-RapidAPI-Host": "pnr-status-indian-railway.p.rapidapi.com"
            }
            r = requests.request("GET", url, headers=headers)
            value = r.json()
            print(value)
            try :
                if value['code'] == 200 : 
                    text = f' *Seat Info* \nCoach : *{value["data"]["seatInfo"]["coach"]}* \nBerth : *{value["data"]["seatInfo"]["berth"]}* \nNo.of Seats : *{value["data"]["seatInfo"]["noOfSeats"]}* \n\n*Train Info* \nTrain number : *{value["data"]["trainInfo"]["trainNo"]}* \nTrain name : *{value["data"]["trainInfo"]["name"]}* '
                    msg.body(f' {text} \n{cont} ')
                    msg.media('https://user-images.githubusercontent.com/118819185/204075125-5a7aef3c-f4d8-4c1a-9b23-ceba67e81334.jpg')
                    responded = True
                else :
                    text = f" {value['error']} \nRecheck PNR or try again please ! \n {cont}"
                    msg.body(text)
                    responded = True
            except :
                msg.body(error)
                responded = True



    # Main message body       
    if not responded and 'Hi' == incoming_msg or 'Hey' == incoming_msg or 'hi' == incoming_msg or 'Menu' == incoming_msg:
        text = f'Do you enjoy travelling ? I like assisting travellers like you ! 🤜🤛 \n\n 👋 Hey there I\'m Voyager , your pocket friendly and personalized travel assistant 🧳 \n\n Please select one of the following option 👇 \n *A* -> Check the availability of hotels 🛌 \n *B* -> Check availability of flight tickets 🛫 \n *C* -> Avail Train Services 🚃 \n *D* -> Itinerary planner 🗓️ \n *E* -> Nearest Hospitals 🏥 \n *F* -> Nearest Police Station 🚨 \n *G* -> Currency conversion 💰 \n *O* -> Avail Other Services 📱 \n\n *_“The journey of a thousand miles begins with a single step.”_* '
        msg.media('https://user-images.githubusercontent.com/118819185/203973014-77eaee6b-b2ae-4ce4-86f6-dc6a7c895f88.jpg')
        msg.body(text)
        responded = True


    elif 'A' == incoming_msg:
        msg.body('Enter your location 📍')
        responded = True


    elif 'B' == incoming_msg:
        text = f'Enter your source location 📍'
        msg.body(text)
        responded = True


    elif 'C'  == incoming_msg:
        text = f' Select the Railway service you would like to avail from below 👇 \n\n *1* -> Live Train Status \n *2* -> Train Schedule \n *3* -> Check PNR Status  \n\n 🚂🚂🚂'
        msg.media('https://user-images.githubusercontent.com/118819185/204074983-8471acf4-f6d5-4988-8631-8e90fdce75e1.jpg')
        msg.body(text)
        responded = True


    elif 'D' == incoming_msg :
        text = f'To get the best plan, click here 👇 \nhttps://touristbot-jd.herokuapp.com/ \n{cont}'
        msg.body(text)
        responded = True

    elif 'E' == incoming_msg :
        text = f'Enter your location 📍'
        msg.body(text)
        responded = True

    elif 'F' == incoming_msg:
        text = f'Enter your location 📍'
        msg.body(text)
        responded = True

    elif 'G' == incoming_msg:
        text = f'*Use currency code*  \nEnter current currency used 💲'
        msg.body(text)
        responded = True

    elif 'O' == incoming_msg:
        text = f' Select the nearest service you would like to avail from below 👇 \n\n *1* -> ATM 🏧 \n *2* -> Bus Station 🚍 \n *3* -> Railway Station 🚟 \n *4* -> Pharmacy 💊 \n *5* -> Restraunt 🍱\n\n *_"A smile is a curve that sets things straight."_* 😉 '
        msg.media('https://user-images.githubusercontent.com/118819185/204011481-1c5d431b-2eda-435e-9e7f-95379391dc2b.jpg')
        msg.body(text)
        responded = True

    elif 'END'== incoming_msg or 'end' == incoming_msg or 'End' == incoming_msg:
        text = 'Thanks for using Voyager ❤️ Until next time 😉'
        msg.body(text)
        msg.media('https://user-images.githubusercontent.com/118819185/204124211-5a3854ff-fe11-4d4b-9e58-04fa61c7c294.png')
        responded = True


    if responded == False:
        msg.body(error)
        msg.media('https://user-images.githubusercontent.com/118819185/204075533-f349eb6b-2a76-45d1-a537-4c2d886658af.jpg')

    chats[request.values["WaId"]].append(incoming_msg)
    print("end",incoming_msg)
    return str(resp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)