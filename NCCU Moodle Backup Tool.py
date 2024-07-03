# NCCU Moodle Backup Tool(NMBT)
# Version: v0.0.4 Beta
# Build: 20240703.1
'''
      ###     ###     #####    ####     #########         #######
     ####    ###     ######  #####     ####   ###        ###
    #####   ###     ### ### # ###     ####   ###        ###
   ### ##  ###     ###  ###  ###     #########         ###
  ###  ## ###     ###       ###     ####   ###        ###
 ###   #####     ###       ###     ####   ###        ###
###    ####     ###       ###     #########      ######
[BETA] v0.0.4-20240703.1

'''

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

service = Service (verbose = True)
options = webdriver.EdgeOptions ()
options.add_argument ("--start-maximized")
options.add_experimental_option ("detach", True) # Keep browser open
driver = webdriver.Edge (service = service, options = options)
os.chdir ('C:\\')
debug_folder_name = 'NMBT_debug'
if not os.path.exists (debug_folder_name):
    os.mkdir (debug_folder_name)
    print (f"{debug_folder_name}資料夾已建立")
elif os.path.exists (debug_folder_name):
    print (f"{debug_folder_name}資料夾已存在")
os.chdir ('C:\\NMBT_debug')
debug_webdriver_folder_name = 'webdriver'
if not os.path.exists (debug_webdriver_folder_name):
    os.mkdir (debug_webdriver_folder_name)
    print (f"{debug_webdriver_folder_name}資料夾已建立")
elif os.path.exists (debug_folder_name):
    print (f"{debug_webdriver_folder_name}資料夾已存在")
service = webdriver.EdgeService(service_args=['--log-level=DEBUG'], log_output="C:\\NMBT_debug\\webdriver")

UserEULAjudge = ""
while UserEULAjudge == "":
    print ("本程式僅基於您所提供的資料進行存取，概不負責您的政大帳號資訊安全，若開始使用視同同意以上說法")
    UserEULA = str (input ("若同意開始請輸入Yes，不同意輸入No以離開本程式："))
    if UserEULA == "Yes" or "yes":
        print ("感謝使用NMBT")
        print ("請注意，能力越強，責任越大")
        print ("Please notice, with great power comes great responsibility.")
        print ("若有使用上的問題，敬請至 https://github.com/chengmoxu/NCCU-Moodle-Backup-Tool 提交Issues")
        print ("NCCU Moodle Backup Tool(NMBT)存檔位置為C:\\NMBT")
        UserEULAjudge = "Start"
        break
    elif UserEULA == "No" or "no":
        print ("感謝使用，期待再次相逢")
        print ("若有使用上的問題，敬請至 https://github.com/chengmoxu/NCCU-Moodle-Backup-Tool 提交Issues")
        print ("本程式即將結束")
        UserEULAjudge = "Exit"
        break
    else:
        print ("輸入錯誤，請重新輸入")
        UserEULAjudge = ""

while UserEULAjudge == "Start":
    driver.get("https://i.nccu.edu.tw/Login.aspx?app=moodle&ReturnUrl=%2fsso_app%2fMoodleSSO.aspx")
    print ("請在自動化視窗中輸入您的政大單一化登入窗口帳號密碼，並在跳轉完成後在此輸入1以繼續")
    print ("或者，輸入0結束\n")
    userinput = input("請輸入：")
    mode = ""
    while mode == "":
        userinput_judge = str.isdigit (userinput)
        if userinput_judge == True: 
            if  userinput == "1":
                mode = "Continue"
                break
            elif userinput == "0":
                mode = "Exit"
                break
            else:
                print ("請重新輸入正確選項！")
                mode = ""
        elif userinput_judge == False:
            print ("請重新輸入正確選項！")
            mode = ""
    
    while mode == "Continue":
        os.chdir ("C:\\")
        NMBT_folder_name = 'NMBT'
        if not os.path.exists (NMBT_folder_name):
            os.mkdir (NMBT_folder_name)
            print (f"{NMBT_folder_name}資料夾已建立")
        elif os.path.exists (NMBT_folder_name):
            print (f"{NMBT_folder_name}資料夾已存在")
        os.chdir ('C:\\NMBT')
        # Get Moodle Main Page via find_elements
        course_list = driver.find_elements(By.CSS_SELECTOR, ".content .unlist .column.c1 a") # content/unlist/r0 or r1/column.c1/a
        course_title = {course.get_attribute("title") for course in course_list}
        course_link = {course.get_attribute("href") for course in course_list}
        courses = (course_title,course_link)
        for course_title, course_link in courses.items ():
            # 去除不合規則的文件名字元
            valid_course_name = "".join (char for char in course_title if char.isalnum() or char in " _-[]！？（）()")
            os.makedirs (valid_course_name, exist_ok = True)
        # 切換資料夾，載入課程頁面進行存取
        for range in courses:
            os.chdir (course_title)
            driver.get (course_link)
            time.sleep (3)  # 等待頁面載入完成
            # section-0 = 公告/課程大綱 資料讀取
            section0 = driver.find_element(By.CSS_SELECTOR, '#section-0')
            folder_name = "課程大綱及公告"
            os.mkdir (folder_name)
            os.chdir (folder_name)
            outline_jump_page = driver.find_elements(By.CSS_SELECTOR, ".content .section img-text .activity url modtype_url .mod-indent-outer .activity-wrapper .activityinstance")
            outline_jump_page_true = outline_jump_page.get_attribute("href")
            driver.get (outline_jump_page_true)
            outline_page = driver.find_elements(By.CSS_SELECTOR, "#region-main .urlworkaround a")
            outline_page_true = outline_page.get_attribute("href")
            with open('Introducing.txt', 'w') as file:
                file.write("課程大綱網址: ")
                file.write(outline_page_true)
            driver.get (course_link)
            # activity-wrapper > activity resource modtype_resource / activity assign modtype_assign / activity assign modtype_assign > mod-indent-outer > activity-wrapper > activityinstance > a
            # section-1至# section-18 = 課程內容 資料讀取
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

while UserEULAjudge == "Exit" or mode == "Exit":
    os.system('pause')
