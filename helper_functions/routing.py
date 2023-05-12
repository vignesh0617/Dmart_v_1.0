from helper_functions.custom_helpers import main_app,decode_token
from pages.about_page import layout as about_page
from pages.home_page import layout as home_page
from pages.login_page import layout as login_page
from pages.page_not_found import layout as page_not_found
import time

c = 0

# This function updates the following
# 1 -> url2 component's pathname
# 2 -> app_output component's children
# 3 -> token component's clear_data
# It takes 2 inpiuts (1 input and 1 state)
# Input -> url1 components pathname
# State -> token components data
def validate_token_and_update_screen(pathname,token):
    global c
    c+=1
    print(f'''----------------------
            Loop number = {c}
            pathname =========== {pathname}
            ---------------------------''')
    try:
        payload = decode_token(token)
        session_not_over = payload['session_end_time'] > int(time.time())
        if session_not_over:
            if(pathname == main_app.environment_details['home_page_link'] or pathname == main_app.environment_details['login_page_link']):
                print("1.1--------------------")
                # return home_page,False
                return main_app.environment_details['home_page_link'],home_page,False
            elif (pathname == main_app.environment_details['about_page_link']):
                # return about_page, False
                return pathname, about_page, False
            elif(pathname == main_app.environment_details['logout_page_link']):
                print("1.2--------------------")
                main_app.connector = ""
                # return login_page,True
                return main_app.environment_details['logout_page_link'],login_page,True
            else:
                print("1.3--------------------")
                # return page_not_found,False
                return pathname,page_not_found,False
        else:
            print("1.4--------------------")
            # return login_page,False
            return main_app.environment_details['login_page_link'],login_page,False
    except Exception as e:
        print("1.5 ---------------------Not a valid Token")
        # return login_page, False
        return main_app.environment_details['login_page_link'],login_page, False
