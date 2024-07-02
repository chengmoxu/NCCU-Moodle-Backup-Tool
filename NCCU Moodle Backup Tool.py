# NCCU Moodle Backup Tool
# Version: v0.0.2 Beta
# Build: 20240702.1

import os
import time
import selenium
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree

driver = webdriver.Edge()
driver.get("https://i.nccu.edu.tw/Login.aspx?app=moodle&ReturnUrl=%2fsso_app%2fMoodleSSO.aspx")

edge_options = webdriver.EdgeOptions()
prefs = {
    "profile.default_content_settings.popups": 0,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}
edge_options.add_experimental_option("prefs", prefs)

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
    # Get Moodle MAain Page via find_elements
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".content .unlist .column.c1 a")
    courses = {course.get_attribute("title"): course.get_attribute("href") for course in course_elements} # Name and Direct Link
    for course_name, course_link in courses.items():
        # 去除不合規則的文件名字元
        valid_course_name = "".join(char for char in course_name if char.isalnum() or char in " _-")
        os.makedirs(valid_course_name, exist_ok=True)
        # 載入課程頁面
        driver.get(course_link)
        time.sleep(2)  # 等待頁面載入完成
        # section-0 = 公告/課程大綱
        section0 = driver.find_element(By.CSS_SELECTOR, '#section-0')
        folder_name = "課程大綱及公告"

        # section-1至# section-18 = 課程內容
        #判斷16/18週
        if driver.find_element (By.CSS_SELECTOR, '#section-16') == True:
            if driver.find_element (By.CSS_SELECTOR, '#section-18') == True:
                sx = 1
                for sx in range(1,18,1):
                    sx_css_selector_con = str("#section-"+sx)
                    sectionX= driver.find_element (By.CSS_SELECTOR, sx_css_selector_con)
                    folder_name = sectionX.get_attribute ('aria-label')
                    content_element = sectionX.find_element (By.CSS_SELECTOR, '.no-overflow')
                    content = content_element.get_attribute ('innerHTML')
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    file_path = os.path.join(folder_name, "介紹.txt")
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)
                    course_resource_links = sectionX.find_elements(By.CSS_SELECTOR, '.activityinstance a')
                    for link in course_resource_links:
                        link_url = link.get_attribute('href')
                        driver.get(link_url)
                        time.sleep(10)
            else:
                sx = 1
                for sx in range(1,16,1):
                    sx_css_selector_con = str("#section-"+sx)
                    sectionX= driver.find_element (By.CSS_SELECTOR, sx_css_selector_con)
                    folder_name = sectionX.get_attribute ('aria-label')
                    content_element = sectionX.find_element (By.CSS_SELECTOR, '.no-overflow')
                    content = content_element.get_attribute ('innerHTML')
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    file_path = os.path.join(folder_name, "介紹.txt")
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)
                    course_resource_links = sectionX.find_elements(By.CSS_SELECTOR, '.activityinstance a')
                    for link in course_resource_links:
                        link_url = link.get_attribute('href')
                        driver.get(link_url)
                        time.sleep(10)
    break
#driver.quit()
while mode == "9":
    print("即將退出程式")
    os.system('pause')
