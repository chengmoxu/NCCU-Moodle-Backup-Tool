# NCCU Moodle Backup Tool
# Version: v0.0.1 Beta
# Build: 20240630.1

import os
import time
import selenium
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()
driver.get("https://i.nccu.edu.tw/Login.aspx?app=moodle&ReturnUrl=%2fsso_app%2fMoodleSSO.aspx")

mode = ""
while mode == "":
    print ("請在自動化視窗中輸入您的政大單一化登入窗口帳號密碼，並在跳轉完成後在此輸入1以繼續")
    print ("或者，輸入0結束自動化工具\n")
    userinput = input ('請輸入：')
    userinput_judge = str.isdigit(userinput)
    if userinput_judge == True: 
        if  userinput == "1":
            mode = "1"
            break
        elif userinput == "0":
            mode = "9"
            break
        else:
           print ("請重新輸入正確選項！")
    elif userinput_judge == False:
        print ("請重新輸入正確選項！")
while mode == "1":
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".content .unlist .column.c1 a")
    courses = {course.get_attribute("title"): course.get_attribute("href") for course in course_elements}
    for course_name, course_link in courses.items():
        # 去除不合規則的文件名字元
        valid_course_name = "".join(char for char in course_name if char.isalnum() or char in " _-")
        os.makedirs(valid_course_name, exist_ok=True)
        # 載入課程頁面
        driver.get(course_link)
        time.sleep(2)  # 等待頁面載入完成
        # section-0 = 公告/課程大綱
        # section-1至# section-18 = 課程內容
    break
#driver.quit()
while mode == "9":
    print("即將退出程式")
    os.system('pause')
