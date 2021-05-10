# import geopy
# from geopy.distance import geodesic
# def getDistance():
#     try:
#         geolocator = geopy.Nominatim(user_agent='maya')
#         distance = input('Enter two locations: ')
#         distance_list = distance.split('and')
#         print(distance_list)
#         location1 = geolocator.geocode(distance_list[0])
#         location2 = geolocator.geocode((distance_list[1]))
#         loc_coord1 = (location1.latitude, location1.longitude)
#         loc_coord2 = (location2.latitude, location2.longitude)
#         distance_calc = round(geodesic(loc_coord1, loc_coord2).km)
#         print(f"The distance between {location1.address} and {location2.address} is {distance_calc}kms.")
#         imp1 = location1.raw.get('importance')
#         imp2 = location2.raw.get('importance')
#         print(imp1, imp2)
#         if max(imp1, imp2) == imp1:
#             print(f'I feel that {location1}is more important administrative place than{location2} ')
#         elif max(imp1, imp2) == imp2:
#             print(f'I feel {location2} is more important administrative place than {location1} ')
#         else:
#             print(f'Both {location1} and {location2} must be of equal administrative importance. ')
#         if distance_calc < 500:
#             print(f'You can either take a car, bus or train to travel to {location2}')
#         elif 500 <= distance_calc < 2000:
#             print(f'Either a flight or the train can be a good option to reach {location2}')
#         else:
#             print(f'Book a flight to reach {location2}')
#     except Exception:
#         print('Invalid Address')
#
# getDistance()

# import pyautogui
# x,y = 900,500
# print(pyautogui.size())
# print(pyautogui.onScreen(1000, 500))
#pyautogui.moveTo(x, y, duration=7)
#pyautogui.dragTo(500, 200, duration=10)
#pyautogui.scroll(-200)
# import time
# import os
# command = input('Enter a String: ')
# dictate = open('dictation.txt','r').read()
# cmd_list = dictate.split(" ")
# swriter_path = "C:\\Program Files\\LibreOffice\\program\\swriter.exe"
# os.startfile(swriter_path)
# time.sleep(10)
#
# for cmd in cmd_list:
#     if cmd in pyautogui.KEYBOARD_KEYS:
#         pyautogui.typewrite([cmd], interval=0.3)
#     else:
#         pyautogui.typewrite(cmd+' ', interval=0.3)
#
# #print(pyautogui.KEYBOARD_KEYS)

import pyautogui

pyautogui.PAUSE = 0.25
pyautogui.FAILSAFE = False
# pyautogui.click()
# pyautogui.moveTo(732,51)
# pyautogui.typewrite('gmail.com')
# pyautogui.typewrite(['enter'])
#pyautogui.mouseInfo()

pyautogui.hotkey('ctrl', 't')

pyautogui.moveTo(535, 50)





