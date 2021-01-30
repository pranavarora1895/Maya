""" Let's call her Maya """
import pyttsx3
import datetime, time
from datetime import date
import speech_recognition as sr
from plyer import notification
import wikipedia
import webbrowser
import os, sys
import smtplib, quickstart
import pywhatkit
import geopy
from geopy.distance import geodesic
import datadynamic as dd
import random
import requests
import platform, socket, re, uuid, json, psutil, logging

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
user_api = os.environ.get('current_weather_api')
engine = pyttsx3.init('sapi5')
mic_voices = engine.getProperty('voices')
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print(rate)
engine.setProperty('rate', 172)
browser = "C://Program Files (x86)//Google//Chrome//Application//chrome.exe %s"
# print(mic_voices[1].id)
time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
engine.setProperty('voice', mic_voices[1].id)

mydata = dd.data


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        morning_wishes = dd.wish_morning
        speak(f'{random.choice(morning_wishes)} Pranav')
    elif 12 <= hour < 16:
        afternoon_wishes = dd.wish_afternoon
        speak(f'{random.choice(afternoon_wishes)} Pranav')
    elif 16 <= hour < 20:
        evening_wishes = dd.wish_evening
        speak(f'{random.choice(evening_wishes)} Pranav')
    else:
        speak('Hope you had dinner Pranav!')

    speak('What can I do for you?')


def takeCommand():
    r = sr.Recognizer()
    # r.energy_threshold = 300
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f'You said: {query}\n')
    except Exception as e:
        # print(e)
        print('Say that again please...')
        return "None"
    return query


def sendEmail(to, content, header):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = header
        body = content

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADDRESS, to, msg)
        smtp.close()


def readEmails():
    speak('Reading first three email snippets')
    message_c = 3
    messages = quickstart.main(message_c)
    count = 0
    for message in messages:
        count += 1
        print(f'{count}. {message}')
        speak(count)
        speak(message)
        time.sleep(2)


def sendWhatsapp(to_message, message):
    time_hr = datetime.datetime.now().time().hour
    time_min = datetime.datetime.now().time().minute
    if time_min == 59:
        time_hr += 1
    next_min = time_min + 2
    if '+' in to_message:
        pywhatkit.sendwhatmsg(to_message, message, time_hr, next_min)
    else:
        pywhatkit.sendwhatmsg_to_group(to_message, message, time_hr, next_min)


def getWeather(mylocspecified='Jhansi'):
    try:
        location = mylocspecified
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + user_api
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()

        # create variables to store and display data
        temp_city = ((api_data['main']['temp']) - 273.15)
        weather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        speak(f'Current temperature for {location} is {int(temp_city)} degrees Celsius with {weather_desc}.')
        speak('Do you want full weather statistics?')
        resp = takeCommand().lower()
        if 'yes' in resp:
            speak(f'Current Humidity is {hmdt} percent with a wind speed of {wind_spd} kilometers per hour.')
        else:
            speak('On your command!')
    except Exception as e:
        print('Just say the city name! Try again!!')


def getSystemInfo():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def myAge():
    f_date = date(2021, 1, 24)
    l_date = date.today()
    delta = l_date - f_date
    year = int(delta.days // 365)
    weeks = int((delta.days % 365) // 7)
    days = (delta.days % 365) % 7
    if year == 0 and weeks == 0:
        speak(f'I am {days} days old.')
    elif year == 0 and weeks != 0:
        speak(f'I am {weeks} weeks and {days} days old.')
    elif weeks == 0 and days == 0:
        speak(f'I am {year} year old.')
    elif days == 0:
        speak(f'I am {year} year and {weeks} weeks old.')
    elif weeks == 0:
        speak(f'I am {year} year and {days} days old.')
    elif days == 0 and year == 0:
        speak(f'I am {weeks} weeks old.')
    else:
        speak(f'I am {year} year, {weeks} weeks and {days} days old.')


def getNews():
    news_api = open('newsapi.txt', 'r').read()
    r = requests.get('http://newsapi.org/v2/top-headlines?country=in&apiKey=' + news_api)
    data = json.loads(r.content)
    speak("Here's the news")
    for i in range(5):
        news1 = data['articles'][i]['title']
        print(f'{i+1}. {news1}')
        speak(i + 1)
        speak(news1)


def getDistance(dist_list):
    try:
        geolocator = geopy.Nominatim(user_agent='maya')
        distance_list = dist_list
        location1 = geolocator.geocode(distance_list[0])
        location2 = geolocator.geocode((distance_list[1]))
        loc_coord1 = (location1.latitude, location1.longitude)
        loc_coord2 = (location2.latitude, location2.longitude)
        distance_calc = round(geodesic(loc_coord1, loc_coord2).km)
        speak(f"The distance between {location1.address} and {location2.address} is {distance_calc} kilometers.")
        imp1 = location1.raw.get('importance')
        imp2 = location2.raw.get('importance')
        #print(imp1, imp2)
        if max(imp1, imp2) == imp1:
            speak(f'I feel that {distance_list[0]}is more important administrative place than {distance_list[1]} ')
        elif max(imp1, imp2) == imp2:
            speak(f'I feel {distance_list[1]} is more important administrative place than {distance_list[0]} ')
        else:
            speak(f'Both {distance_list[0]} and {distance_list[1]} must be of equal administrative importance. ')
        if distance_calc < 500:
            speak(f'You can either take a car, bus or train to travel to {distance_list[1]}')
        elif 500 <= distance_calc < 2000:
            speak(f'Either a flight or the train can be a good option to reach {distance_list[1]}')
        else:
            speak(f'Book a flight to reach {distance_list[1]}')
    except Exception:
        speak('Invalid Address')



def readDictation():
    try:
        file = open('dictation.txt', 'r').read()
        if file == "":
            speak('Dictation Section is empty')
        else:
            print(file)
            speak(file)
    except FileNotFoundError:
        speak('Dictation file not found')


def clearDictation():
    speak('Are you sure you want to clear the dictation? This step can be destructive!!!(yes or no)?')
    sure = takeCommand()
    if 'yes' in sure:
        file = open('dictation.txt', 'w')
        clear_file = ""
        file.write(clear_file)
        file.close()
        speak('The dictation has been cleared')
    else:
        speak('No changes done in the dictation')


def writeDictation():
    file = open('dictation.txt', 'r')
    read_file = file.read()
    file.close()
    if read_file != "":
        speak('The file already contains previous dictation. Do you want to continue in previous existing file, '
              'or you want to clear the previous dictation?(continue or clear or read)?')
        permission = takeCommand()
        if 'clear' in permission:
            clearDictation()
            file_write = open('dictation.txt', 'a')
            dictate_on = True
            file_write.write(time_stamp + '\n\n')
            while dictate_on:
                speak('What you want to write?')
                dictate_maya = takeCommand()
                file_write.write(dictate_maya + '\n')
                speak('Added to the dictation')
                speak('Do you want to dictate more?(yes or no) ')
                per = takeCommand()
                if 'no' in per:
                    dictate_on = False
                else:
                    dictate_on = True
            speak('Your dictation has been added.')
            file_write.close()
        elif 'continue' in permission:
            file_append = open('dictation.txt', 'a')
            file_append.write("\n\n")
            file_append.write(time_stamp + '\n\n')
            dictate_on = True
            while dictate_on:
                speak('What you want to write?')
                dictate_maya = takeCommand()
                file_append.write(dictate_maya + '\n')
                speak('Added to the dictation')
                speak('Do you want to dictate more? (yes or no) ')
                per = takeCommand()
                if 'no' in per:
                    dictate_on = False
                else:
                    dictate_on = True
            speak('Your dictation has been added.')
            file_append.close()
        else:
            readDictation()
            writeDictation()
    else:
        file_write = open('dictation.txt', 'w')
        dictate_on = True
        file_write.write(time_stamp + '\n\n')
        while dictate_on:
            speak('What you want to write?')
            dictate_maya = takeCommand()
            file_write.write(dictate_maya + '\n')
            speak('Added to the dictation')
            speak('Do you want to dictate more?(yes or no)')
            per = takeCommand()
            if 'no' in per:
                dictate_on = False
            else:
                dictate_on = True
        speak('Your dictation has been added.')
        file_write.close()


def who_are_you():
    speak(dd.who_am_i)
    speak('Do you want to know my specifications?')
    resp = takeCommand().lower()
    if 'yes' in resp:
        speak('Okay!! Taking you into some technical stuff now')
        speak(f'Born on 24 January 2021')
        myAge()
        speak(f'I was built on Python {sys.version}.')
        speak(f'I reside in: {json.loads(getSystemInfo())}, current version: 0.0.1')
    else:
        speak('Sure')


def matched_query(inp_query, matching_list):
    for word in matching_list:
        if word in inp_query:
            return word
    else:
        return "none_thing"


to_message, send_message_to, to, send_to = None, None, None, None
if __name__ == '__main__':
    notification.notify(
        title='Maya here 😊😊',
        message='Your Virtual Assistant',
        app_icon='maya.ico',
        timeout=10
    )
    time.sleep(1)
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            try:
                print('Searching.....')
                speak('Searching wikipedia')
                query = query.replace('wikipedia', "")
                results = wikipedia.summary(query, sentences=2)
                speak('According to wikipedia')
                print(results)
                speak(results)
            except Exception as e:
                speak('Sorry!! Unable to search!!')

        elif 'youtube' in query:
            if 'search on youtube' in query:
                print('Searching.....')
                speak('Searching youtube')
                query = query.replace('search on youtube', "")
                pywhatkit.playonyt(query)
            else:
                webbrowser.get(browser).open('https://www.youtube.com')
        elif 'google' in query:
            if 'search on google' in query:
                print('Searching.....')
                speak('Searching google')
                query = query.replace('search on google', "")
                pywhatkit.search(query)
            else:
                webbrowser.get(browser).open('https://www.google.com')
        elif 'stack over' in query:
            webbrowser.get(browser).open('https://www.stackoverflow.com')
        elif 'github' in query:
            webbrowser.get(browser).open('https://github.com/pranavarora1895')
        elif 'whatsapp web' in query:
            webbrowser.get(browser).open('https://web.whatsapp.com/')
        elif 'gmail' in query:
            webbrowser.get(browser).open('https://www.gmail.com')
        elif 'play music' in query:
            mus_dir = "C:\\Users\\major\\Music\\Favourites"
            songs = os.listdir(mus_dir)
            print(list(songs))
            os.startfile(os.path.join(mus_dir, random.choice(songs)))
        elif 'stream' in query:
            print('Searching your song...')
            speak('finding your song')
            query = query.replace('stream', "song")
            pywhatkit.playonyt(query)
        elif 'writer' in query:
            swriter_path = "C:\\Program Files\\LibreOffice\\program\\swriter.exe"
            os.startfile(swriter_path)
        elif 'zoom' in query:
            zoom = "C:\\Users\\major\\AppData\\Roaming\\Zoom\\bin\\zoom.exe"
            os.startfile(zoom)
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'The time is {strTime}')
        elif 'send email' in query:
            sure = True
            try:
                while sure:
                    speak('What should be the subject of the email?')
                    header = takeCommand()
                    speak('What should I write in the email?')
                    content = takeCommand()
                    try:
                        speak('Whom should I send it to?')
                        send_to = takeCommand().lower()
                        to = mydata.get(send_to)[0]
                        speak(f'Subject of email: {header}. Body of email: {content}. Are you sure you want to send '
                              f'this mail to {send_to}?')
                        surity = takeCommand()
                        if surity == 'yes':
                            sure = False
                    except Exception as e:
                        speak(f'Email for {send_to} not found')
                sendEmail(to, content, header)
                speak('The Email has been sent')
            except Exception as e:
                print(e)
                speak('Sorry Pranav!! I was unable to send the email!')
        elif 'send whatsapp' in query:
            sure = True
            try:
                while sure:
                    speak('What should I write?')
                    message = takeCommand()
                    try:
                        speak('Whom should I send the message to?')
                        send_message_to = takeCommand().lower()
                        to_message = mydata.get(send_message_to)[1]
                    except Exception as e:
                        speak(f'{send_message_to} not found')
                    speak(f'{message}. Are you sure you want to send this message to {send_message_to}')
                    surity = takeCommand()
                    if 'yes' in surity:
                        sure = False
                speak('Your message will be delivered within 2 minutes')
                sendWhatsapp(to_message, message)
                speak('The message has been sent')
            except Exception as e:
                print(e)
                speak('Sorry Pranav!! I was unable to send the message!')

        elif 'the weather' in query:
            speak('For which place you want to get the weather data?')
            myloc = takeCommand()
            getWeather(myloc)

        elif 'what is the distance between' in query:
            distance = query.replace('what is the distance between','')
            distance_list = distance.split('and')
            #print(distance_list)
            getDistance(distance_list)

        elif matched_query(query, dd.query_news) in query:
            print('Searching news...')
            speak('Searching news!!')
            getNews()

        elif matched_query(query, dd.query_read_mails) in query:
            readEmails()

        elif matched_query(query, dd.query_schedule) in query:
            speak('Setting up your Schedule')
            speak('Getting the weather details')
            getWeather('Jhansi')
            speak('Getting news!!')
            getNews()
            speak('Fetching your emails')
            readEmails()

        elif matched_query(query,dd.query_dictation) in query:
            speak('Which feature in dictation you want to use? Read, Edit or Clear Dictation?')
            feature = takeCommand().lower()
            if 'read' in feature:
                readDictation()
            elif 'edit' in feature:
                writeDictation()
            elif 'clear' in feature:
                clearDictation()
            else:
                speak('Sorry!! Please choose between Read, Write or Clear')

        elif matched_query(query, dd.query_who_am_i) in query:
            who_are_you()

        elif matched_query(query,dd.query_age) in query:
            myAge()

        elif matched_query(query, dd.query_thank_you) in query:
            thank = dd.thank_you
            speak(f'{random.choice(thank)} Pranav')
            break
