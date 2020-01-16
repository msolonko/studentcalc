# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 19:47:43 2018

@author: msolonko
"""

import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import re
from extraction import Extractor
from convert import Converter
import numpy as np
from fake_useragent import UserAgent
import csv
from time import time
from keras.models import load_model
from sklearn.externals import joblib


#MODIFY BELOW VARIABLES
#**********************
URL_LISTS = [
    [
"https://talk.collegeconfidential.com/boston-college/1871029-boston-college-class-of-2020-rd-results-only.html",
"https://talk.collegeconfidential.com/boston-college/1842019-official-boston-college-ea-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/boston-college/1972561-boston-college-class-of-2021-rd-results-only.html",
"https://talk.collegeconfidential.com/boston-college/1944445-official-boston-college-class-of-2021-rea-results-thread.html",
"https://talk.collegeconfidential.com/boston-college/2040417-boston-college-ea-class-of-2022-results.html",
"https://talk.collegeconfidential.com/boston-college/2115185-boston-college-rd-2023.html"
],
     [
"https://talk.collegeconfidential.com/boston-university/1871655-bu-rd-2020-decisions-only.html",
"https://talk.collegeconfidential.com/boston-university/1842078-boston-university-ed-2-class-of-2020-applicants.html",
"https://talk.collegeconfidential.com/boston-university/1973043-bu-class-of-2021-rd-decisions.html",
"https://talk.collegeconfidential.com/boston-university/1926551-boston-university-early-decision-class-of-2021-thread.html",
"https://talk.collegeconfidential.com/boston-university/2039156-bu-rd-class-of-2022.html",
"https://talk.collegeconfidential.com/boston-university/2044212-regular-decision-class-of-2022.html",
"https://talk.collegeconfidential.com/boston-university/2114740-boston-university-2023-ed-results.html",
"https://talk.collegeconfidential.com/boston-university/2116033-boston-university-rd-2023.html"
],
      [
"https://talk.collegeconfidential.com/georgia-institute-technology/1729605-official-georgia-tech-early-action-2019-decisions-thread.html",
"https://talk.collegeconfidential.com/georgia-institute-technology/1869631-georgia-tech-rd-results.html",
"https://talk.collegeconfidential.com/georgia-institute-technology/1751592-official-georgia-tech-class-of-2019-rd-decision-thread.html",
"https://talk.collegeconfidential.com/georgia-institute-technology/1955681-georgia-tech-class-of-2021-ea-results-thread.html",
"https://talk.collegeconfidential.com/georgia-institute-technology/2048475-georgiatech-class-of-2022-ea-results-thread.html",
"https://talk.collegeconfidential.com/georgia-institute-technology/2127893-georgia-tech-class-of-2023-rd-discussion-results.html",
"https://talk.collegeconfidential.com/georgia-institute-technology/2103174-georgia-tech-class-of-2023-ea-thread.html"
],
       [
"https://talk.collegeconfidential.com/university-rochester/1743310-rochester-2019-rd-results-only-thread.html",
"https://talk.collegeconfidential.com/university-rochester/1865409-university-of-rochester-rd-class-of-2020-decisions.html",
"https://talk.collegeconfidential.com/university-rochester/1838992-university-of-rochester-ed-class-of-2020.html",
"https://talk.collegeconfidential.com/university-rochester/1941648-university-of-rochester-class-of-2021-regular-decision-discussion.html",
"https://talk.collegeconfidential.com/university-rochester/1930140-university-of-rochester-class-of-2021-early-decision-thread.html",
"https://talk.collegeconfidential.com/university-rochester/1838992-university-of-rochester-ed-class-of-2020.html",
"https://talk.collegeconfidential.com/university-rochester/1865409-university-of-rochester-rd-class-of-2020-decisions.html"
],
        [
"https://talk.collegeconfidential.com/university-california-irvine/1741774-uc-irvine-class-of-2019-admissions-results-stats-discussion.html",
"https://talk.collegeconfidential.com/university-california-irvine/1862532-uc-irvine-class-of-2020-admissions-results-stats-discussion.html",
"https://talk.collegeconfidential.com/university-california-irvine/1963951-uci-results-thread-2021.html",
"https://talk.collegeconfidential.com/university-california-irvine/2051107-uc-irvine-class-of-2022-applicants.html",
"https://talk.collegeconfidential.com/university-california-irvine/2129468-uc-irvine-class-of-2023-decision-thread-stats-only.html"
],
                [
"https://talk.collegeconfidential.com/university-california-santa-barbara/1872774-ucsb-class-of-2020-results-discussion-page.html",
"https://talk.collegeconfidential.com/university-southern-california/1938675-usc-class-of-2021-discussion-results-thread.html",
"https://talk.collegeconfidential.com/university-california-santa-barbara/2038717-ucsb-admission-class-of-2022.html",
"https://talk.collegeconfidential.com/university-california-santa-barbara/2129469-uc-santa-barbara-class-of-2023-decision-thread-stats-only.html"
],
                        [
"https://talk.collegeconfidential.com/university-california-san-diego/1748764-ucsd-class-of-2019-decisions-discussion.html",
"https://talk.collegeconfidential.com/university-california-san-diego/1865832-uc-san-diego-class-of-2020-decisions-thread.html",
"https://talk.collegeconfidential.com/university-california-san-diego/1948748-ucsd-class-of-2021-discussion-decisions.html",
"https://talk.collegeconfidential.com/university-california-san-diego/2041381-ucsd-class-of-2022.html",
"https://talk.collegeconfidential.com/university-california-san-diego/2129465-uc-san-diego-class-of-2023-decision-thread-stats-only.html"
],
   ["https://talk.collegeconfidential.com/university-michigan-ann-arbor/2117611-university-of-michigan-class-of-2023-ea-results-thread.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1840250-michigan-ea-class-of-2020-results-thread.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1858738-university-of-michigan-regular-decision-class-of-2020-results-thread.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1941695-umichigan-ann-arbor-class-of-2021-results-only.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1960631-umich-ann-arbor-class-of-2021-rd.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/2047203-university-of-michigan-regular-decision-class-of-2022.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1578190-official-class-of-2018-university-of-michigan-ea-decisions-thread.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1589223-official-university-of-michigan-class-of-2018-ea-results-thread-stats-only.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1704751-official-class-of-2019-university-of-michigan-ea-decisions-thread.html",
            "https://talk.collegeconfidential.com/university-michigan-ann-arbor/1721049-class-of-2019-university-of-michigan-ea-results-thread-stats.html",
	    "https://talk.collegeconfidential.com/university-michigan-ann-arbor/2117016-university-of-michigan-class-of-2023-regular-decision.html"
],
    [
"https://talk.collegeconfidential.com/university-north-carolina-chapel-hill/1757215-unc-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/university-north-carolina-chapel-hill/1735864-unc-class-of-2019-ea-decision-thread.html",
"https://talk.collegeconfidential.com/university-north-carolina-chapel-hill/1821047-unc-class-of-2020-ea-discussion-thread.html",
"https://talk.collegeconfidential.com/university-north-carolina-chapel-hill/1959107-unc-2021-ea-results-official.html",
"https://talk.collegeconfidential.com/university-north-carolina-chapel-hill/2052003-unc-2022-ea-results.html",
"https://talk.collegeconfidential.com/university-north-carolina-chapel-hill/2123342-unc-2023-ea-results-thread.html"
],
     [
"https://talk.collegeconfidential.com/university-virginia/1754061-uva-class-of-2019-regular-decision-results-thread.html",
"https://talk.collegeconfidential.com/university-virginia/1734367-uva-class-of-2019-ea-results-thread.html",
"https://talk.collegeconfidential.com/university-virginia/1843394-uva-2020-ea-results-discussion-thread.html",
"https://talk.collegeconfidential.com/university-virginia/1849757-university-of-virginia-early-action-results-2020.html",
"https://talk.collegeconfidential.com/university-virginia/1958526-official-uva-2021-early-action-results-decision-thread.html",
"https://talk.collegeconfidential.com/university-virginia/2051755-uva-ea-results-decision-thread-class-of-2022.html",
"https://talk.collegeconfidential.com/university-virginia/2066357-uva-rd-results-decisions-class-of-2022.html",
"https://talk.collegeconfidential.com/university-virginia/2062370-uva-class-of-2022-rd-decisions.html",
"https://talk.collegeconfidential.com/university-virginia/2131713-uva-regular-decision-decisions-only-class-of-2023.html",
"https://talk.collegeconfidential.com/university-virginia/2123281-uva-early-action-decisions-only-class-of-2023.html"
],
[
"https://talk.collegeconfidential.com/wake-forest-university/1975382-wake-forest-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/wake-forest-university/1951199-wake-forest-regular-decision-thread.html",
"https://talk.collegeconfidential.com/wake-forest-university/2120762-wake-forest-2023-ed-2.html"
]     
]

FILE_NAME = "Tier 4"
COLLEGE_STATE_NAMES = ['Massachusetts', 'Massachusetts', 'Georgia', 'New York', 'California', 'California', 'California', 'Michigan', 'North Carolina', 'Virginia', 'North Carolina']
COLLEGE_STATE_ABBRS = ['MA', 'MA', 'GA', 'NY', 'CA', 'CA', 'CA', 'MI', 'NC', 'VA', 'NC']
PRINT_UPDATES = True
MAX_FALSE = 0
FALSE_VALUE = -5

#**********************


print("Enter start() to begin process...")


#REST OF THE PROGRAM (NO CHANGES REQUIRED)
#objects to call necessary functions
extractor = Extractor()
converter = Converter()

#lists for storing data
decision_list = []  
gpa_list = []
act_list = []
subject_test_list = []
gender_list = []
ethnicity_list = []
essay_list = []
rec_list = []
school_type_list = []
region_list = []

sat2model = False
sat2scaler = False
sat2counter = 0

        
#PATTERNS
#decision information
decision_marker = re.compile(r'decision:', re.IGNORECASE)
sat_marker = re.compile(r'SAT I(?!I)(?=.*:)')
act_marker = re.compile(r'ACT(?=.*:)')
subject_test_marker = re.compile(r'SAT II(?=.*:)')
gpa_marker = re.compile(r'(unweighted GPA(?=.*:))|(GPA(?=.*unweighted)(?=.*:))', re.IGNORECASE)
essay_marker = re.compile(r'(Essays|common app)(?=.*:)', re.IGNORECASE)
rec_marker = re.compile(r'(Rec|Interview|Teacher|Counselor)(?=.*:)', re.IGNORECASE)
gender_marker = re.compile(r'Gender(?=.*:)', re.IGNORECASE)
ethnicity_marker = re.compile(r'Ethnicity(?=.*:)', re.IGNORECASE)
school_marker = re.compile(r'school type(?=.*:)', re.IGNORECASE)
region_marker = re.compile(r'state(?!ment)(?=.*:)', re.IGNORECASE)



#log in information (if needed in the future)
#email = "caxamexabo@nyrmusic.com"
#password = "calculator1819"

#adds proper URL ending to enable looping through pages


def start():
    global sat2model, sat2scaler
    start_time = time()
    sat2model = getSat2Model()
    sat2scaler = getSat2Scaler()
    for ind in range(len(URL_LISTS)):
        
        #data for each individual college
        URL_LIST = URL_LISTS[ind]
        COLLEGE_STATE_NAME = COLLEGE_STATE_NAMES[ind]
        COLLEGE_STATE_ABBR = COLLEGE_STATE_ABBRS[ind]
        
        if len(URL_LIST) == 0:
            print("Check the length of your input lists!")
            return False
        
        for i in range(len(URL_LIST)):
            if URL_LIST[i].find("-p1.html") == -1:
                URL_LIST[i] = URL_LIST[i][0:-5] + "-p1.html"
        
        for i in range(len(URL_LIST)):  
            printUpdate("\n\n*********************\nNow checking URL "+str(i)+"\n*********************\n\n")
            url = URL_LIST[i]
            page_number = 1
            while True:
                #handles URL changes with each new page
                if page_number != 1:
                    old_ending = "p" + str(page_number - 1) + ".html"
                    new_ending = "p" + str(page_number) + ".html"
                    url = url.replace(old_ending, new_ending)
                
                #opening a page that does not exist may fail
                try:
                    #opening connection to URL & tricking site into thinking that this is a human user
                    ua = UserAgent()
                    req = Request(url, headers={'User-Agent':str(ua.chrome)}) #MAKE MORE COMPLICATED TO AVOID DETECTION
                    client = urlopen(req)
                    
                    #downloading html data
                    page_html = client.read()
                    page_soup = soup(page_html, "html.parser")
                    
                    #unordered list of comments given three classes of container
                    comments = page_soup.select("ul.MessageList.DataList.Comments li.Item.ItemComment div.Message.userContent")
                    for comment in comments:
                        decision = gpa = act = sat = subject_test = gender = ethnicity = essay = rec = school = region = "False"
                        temp_essay_list = []
                        essay_tracker = False
                        temp_rec_list = []
                        def processLine(ln):
                            #print(line)
                            nonlocal decision, gpa, sat, act, subject_test, gender, ethnicity, school, region, essay_tracker
                            if decision == "False":
                                if decision_marker.search(ln):
                                    decision = extractor.getDecision(ln)
                            else:
                                if gpa == "False":
                                    if gpa_marker.search(ln):
                                        gpa = extractor.getGPA(ln)
                                if sat == "False":
                                    if sat_marker.search(ln):
                                        sat = extractor.getSAT(ln)
                                if act == "False":
                                    if act_marker.search(ln):
                                        act = extractor.getACT(ln)
                                if subject_test == "False":
                                    if subject_test_marker.search(ln):
                                        subject_test = extractor.getSubjectTests(ln)
                                if gender == "False":
                                    if gender_marker.search(ln):
                                        gender = extractor.getGender(ln)
                                if ethnicity == "False":
                                    if ethnicity_marker.search(ln):
                                        ethnicity = extractor.getEthnicity(ln)
                                if school == "False":
                                    if school_marker.search(ln):
                                        school = extractor.getSchoolType(ln)
                                if region == "False":
                                    if region_marker.search(ln):
                                        region = extractor.getRegion(ln, COLLEGE_STATE_NAME, COLLEGE_STATE_ABBR)
                                if essay_marker.search(ln):
                                    essay_tracker = True
                                if rec_marker.search(ln):
                                        essay_tracker = False
                                        rec = extractor.getRec(ln)
                                        if rec != "False":
                                            temp_rec_list.append(rec)
                                if essay_tracker:
                                    essay = extractor.getEssay(ln)
                                    if essay != "False":
                                        temp_essay_list.append(essay)
                                        
                                        
                                        
                        for line in comment:
                            if isinstance(line, bs4.element.Tag):
                                for el in line:
                                    processLine(str(el))
                            else:
                                line_string = str(line)
                                processLine(line_string)
                                #below code checks for indicators of various data in current line
                                
                        
                        #checks if comment is valid
                        essay = round(np.mean(temp_essay_list), 1) if len(temp_essay_list)>0 else "False"
                        rec = round(np.mean(temp_rec_list), 1) if len(temp_rec_list)>0 else "False" 
                        act = toACT(act, sat)
                        checkValidityAndEnter(decision, gpa, act, subject_test, gender, ethnicity, essay, rec, school, region)
                        
                    #closing connection
                    client.close()
                    printUpdate("Checked page " + str(page_number))
                    page_number += 1
                except Exception as e:
                    #print(line_string)
                    print(e)
                    printUpdate("The following URL was not found. Program terminated.\n" + url + "\n")
                    break
            
            
    #prints out retrieved data
    #for i in range(len(decision_list)):
        #printUpdate("Student " + str(i) + " Decision: " + str(decision_list[i]) + " GPA: " + str(gpa_list[i]) + " ACT: " + str(act_list[i]) + " SAT II: " + str(subject_test_list[i]) + " \nGender: " + str(gender_list[i])+ " Ethnicity: " + str(ethnicity_list[i])+ " Essay: " + str(essay_list[i])+ " Rec: " + str(rec_list[i])+ " \nSchool Type: " + str(school_type_list[i])+" Region: " + str(region_list[i])+ " Round: " + str(application_round_list[i]))
        #printUpdate('\n')
            
    printUpdate('\n\n\n***SAVING DATA***\n\n\n')
    printUpdate("Users added with SAT2 Neural Network: " + str(sat2counter))
    #saving extracted data to lists
    saveData()
    end_time = time()
    print("Time elapsed: " + str(round(end_time-start_time, 2)) + "s")
    
    
    
#checks if analyzed comment is valid
def checkValidityAndEnter(decision, gpa, act, subject_test, gender, ethnicity, essay, rec, school, region):
    global sat2counter
    if decision != "False":
        num_false = sum(1 for x in [gpa, act, gender, ethnicity, essay, rec, school, region] if x == "False")
        if num_false <= MAX_FALSE:
            decision_list.append(decision)
            gpa_list.append(defalsify(gpa))
            act_list.append(defalsify(act))
            gender_list.append(defalsify(gender))
            ethnicity_list.append(defalsify(ethnicity))
            essay_list.append(defalsify(essay))
            rec_list.append(defalsify(rec))
            school_type_list.append(defalsify(school))
            region_list.append(defalsify(region))
            if subject_test == "False":
                sat2counter += 1
                subject_test_list.append(round(sat2model.predict(sat2scaler.transform(np.array([[gpa, act]])))[0][0]))
            else:
                subject_test_list.append(defalsify(subject_test))

        
def toACT(a, s):
    if a == "False" and s == "False":
        return "False"
    elif a == "False" and s != "False":
        return converter.convert_test([s])[0]
    elif a != "False" and s == "False":
        return a
    else:
        converted = converter.convert_test([s])[0]
        return np.max([a, converted])
    
def saveData():
    #saves data to CSV file
    data_list = getRows()
    printUpdate("Data successfully converted...")
    file_name = FILE_NAME+".csv"
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data_list)
    csvFile.close()
    printUpdate("Data saved to CSV")    
    
def defalsify(inp):
    return FALSE_VALUE if inp == "False" else inp

def getRows():
    str_decision = [[val] for val in list(map(str, decision_list))]
    str_act = [[val] for val in list(map(str, act_list))]
    str_gpa = [[val] for val in list(map(str, gpa_list))]
    str_subject_tests = [[val] for val in list(map(str, subject_test_list))]
    str_essay = [[val] for val in list(map(str, essay_list))]
    str_rec = [[val] for val in list(map(str, rec_list))]
    str_gender = [[val] for val in list(map(str, gender_list))]
    str_ethnicity = [[val] for val in list(map(str, ethnicity_list))]
    str_school = [[val] for val in list(map(str, school_type_list))]
    str_region = [[val] for val in list(map(str, region_list))]
    data = [a + b + c + d + e + f + g + h + i + j for a, b, c, d, e, f, g, h, i, j in zip(str_decision, str_gpa, str_act, str_subject_tests, str_gender, str_ethnicity, str_essay, str_rec, str_school, str_region)]
    return [['Decision', 'GPA', 'ACT', 'SAT II', 'Gender', 'Ethnicity', 'Essay', 'Recommendation', 'School Type', 'Region']] + data

def getSat2Model():
    # load json and create model
    print("Loading model from file: model_sat2.h5...")
    return load_model("model_sat2.h5")
    
def getSat2Scaler():
    #load scaler
    print("Loading scaler from file: scaler_sat2.save...")
    return joblib.load("scaler_sat2.save")

def printUpdate(s):
    if PRINT_UPDATES:
        print(s)