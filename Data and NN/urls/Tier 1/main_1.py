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
URL_LISTS = [["https://talk.collegeconfidential.com/stanford-2018/2036784-stanford-class-of-2022-rea-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-2018/2069289-stanford-class-of-2022-rd-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1977925-stanford-class-of-2021-rd-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1938730-stanford-class-of-2021-rea-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1873356-stanford-2020-regular-decision-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1833324-stanford-class-of-2020-rea-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1712948-stanford-class-of-2019-rea-results-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1757051-official-stanford-class-of-2019-rd-results-only-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1587085-stanford-2018-rea-results-only-thread.html",
            "https://talk.collegeconfidential.com/stanford-university/1630186-official-stanford-2018-rd-results-only-thread.html"
            ],
            ["https://talk.collegeconfidential.com/yale-university/2038993-yale-university-class-of-2022-scea-decision-results.html",
            "https://talk.collegeconfidential.com/yale-university/2115024-yale-university-class-of-2023-scea-decision-result.html",
            "https://talk.collegeconfidential.com/yale-university/2070184-yale-university-class-of-2022-regular-decision-results-only.html",
            "https://talk.collegeconfidential.com/yale-university/1939888-yale-university-class-of-2021-scea-results.html",
            "https://talk.collegeconfidential.com/yale-university/1872256-yale-university-class-of-2020-rd-results.html",
            "https://talk.collegeconfidential.com/yale-university/1829684-yale-university-class-of-2020-scea-results.html",
            "https://talk.collegeconfidential.com/yale-university/1713050-yale-class-of-2019-scea-decisions.html",
            "https://talk.collegeconfidential.com/yale-university/1752938-yale-university-class-of-2019-rd-results.html",
            "https://talk.collegeconfidential.com/yale-university/1629434-official-yale-class-of-2018-rd-results-thread.html",
	    "https://talk.collegeconfidential.com/yale-university/2134398-yale-rd-2023-results-only.html"],
             
             ["https://talk.collegeconfidential.com/california-institute-technology/2114552-caltech-2023-ea-results.html",
"https://talk.collegeconfidential.com/california-institute-technology/2038749-official-caltech-2022-ea-results.html",
"https://talk.collegeconfidential.com/california-institute-technology/2062434-official-caltech-2022-ra-results.html",
"https://talk.collegeconfidential.com/california-institute-technology/1970814-caltech-2021-rd-results-thread.html",
"https://talk.collegeconfidential.com/california-institute-technology/1943946-official-caltech-class-of-2021-ea-results-thread.html",
"https://talk.collegeconfidential.com/california-institute-technology/1840314-caltech-class-of-2020-ea-results-thread.html",
"https://talk.collegeconfidential.com/california-institute-technology/1715300-official-caltech-class-of-2019-ea-results-thread.html",
"https://talk.collegeconfidential.com/california-institute-technology/2128153-caltech-rd-2023-applicants-results-deferred-applicants-results.html"
],
              
            [
"https://talk.collegeconfidential.com/columbia-university/2114919-columbia-class-of-2023-ed-results.html",
"https://talk.collegeconfidential.com/columbia-university/2039160-columbia-class-of-2022-ed-results.html",
"https://talk.collegeconfidential.com/columbia-university/2070141-official-columbia-university-class-of-2022-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/columbia-university/1975653-official-columbia-university-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/columbia-university/1943963-columbia-class-of-2021-ed-results.html", 
"https://talk.collegeconfidential.com/columbia-university/1876676-columbia-university-class-of-2020-rd-results.html",
"https://talk.collegeconfidential.com/columbia-university/1827281-columbia-class-of-2020-ed-results.html",
"https://talk.collegeconfidential.com/columbia-university/1752936-columbia-university-class-of-2019-results.html",
"https://talk.collegeconfidential.com/columbia-university/1713743-columbia-class-of-2019-e-d-results-only.html",
"https://talk.collegeconfidential.com/columbia-university/2134076-columbia-rd-class-of-2023-results-only.html"
],
            
            ["https://talk.collegeconfidential.com/harvard-university/2115368-harvard-scea-2023-results.html",
"https://talk.collegeconfidential.com/harvard-university/2039011-harvard-university-class-of-2022-scea-results.html",
"https://talk.collegeconfidential.com/harvard-university/2041489-harvard-university-class-of-2022-rd-thread.html",
"https://talk.collegeconfidential.com/harvard-university/1939648-harvard-class-of-2021-scea-results-only-thread.html",
"https://talk.collegeconfidential.com/harvard-university/1962932-harvard-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/harvard-university/1865655-harvard-rd-class-of-2020-result-thread.html",
"https://talk.collegeconfidential.com/harvard-university/1838690-official-harvard-university-class-of-2020-scea-decisions.html",
"https://talk.collegeconfidential.com/harvard-university/1752941-harvard-university-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/harvard-university/1714730-official-harvard-university-2019-scea-decisions-only.html"
],
            
            ["https://talk.collegeconfidential.com/massachusetts-institute-technology/2111642-mit-class-of-2023-discussion-decisions.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/2116066-mit-ea-2023-results.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/2040000-mit-class-of-2022-ea-results-thread.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/2063828-official-mit-rd-results-class-of-2022.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/1962774-official-mit-rd-results-discussion-class-of-2021.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/1944289-mit-ea-results-discussion-class-of-2021.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/1870162-mit-class-of-2020-rd-results-thread.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/1841817-mit-class-of-2020-ea-results-thread.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/1751457-mit-class-of-2019-rd-results-thread.html",
"https://talk.collegeconfidential.com/massachusetts-institute-technology/1717092-mit-class-of-2019-ea-results-thread.html"
],
             
            [
"https://talk.collegeconfidential.com/princeton-university/2114122-princeton-university-class-of-2023-scea-results-thread.html",
"https://talk.collegeconfidential.com/princeton-university/2039825-princeton-university-class-of-2022-scea-results.html",
"https://talk.collegeconfidential.com/princeton-university/2070177-official-princeton-university-class-of-2022-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/princeton-university/1962844-official-princeton-university-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/princeton-university/1946109-princeton-university-class-of-2021-scea-decisions-thread.html",
"https://talk.collegeconfidential.com/princeton-university/1876271-princeton-regular-decision-2020-results-thread.html",
"https://talk.collegeconfidential.com/princeton-university/1831713-princeton-university-class-of-2020-scea-results.html",
"https://talk.collegeconfidential.com/princeton-university/1752939-princeton-university-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/princeton-university/1713233-official-princeton-university-class-of-2019-scea-results.html",
"https://talk.collegeconfidential.com/princeton-university/2134017-princeton-rd-class-of-2023-results-only.html"
],
                    
           [
"https://talk.collegeconfidential.com/university-pennsylvania/2114631-penn-class-of-2023-ed-results-only.html",
"https://talk.collegeconfidential.com/university-pennsylvania/2039187-penn-class-of-2022-ed-results-only.html",
"https://talk.collegeconfidential.com/university-pennsylvania/1977696-upenn-class-of-2021-rd-results.html",
"https://talk.collegeconfidential.com/university-pennsylvania/1940225-university-of-pennsylvania-ed-class-of-2021-results.html",
"https://talk.collegeconfidential.com/university-pennsylvania/1876807-university-of-pennsylvania-rd-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/university-pennsylvania/1829755-university-of-pennsylvania-ed-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/university-pennsylvania/1742882-official-university-of-pennsylvania-class-of-2019-rd-results-only-thread.html",
"https://talk.collegeconfidential.com/university-pennsylvania/1713628-official-university-of-pennsylvania-class-of-2019-ed-results-thread.html",
"https://talk.collegeconfidential.com/university-pennsylvania/2115679-upenn-class-of-2023-rd.html"
]
]

FILE_NAME = "Tier 1"
COLLEGE_STATE_NAMES = ['California', 'Connecticut', 'California', 'New York', 'Massachusetts', 'Massachusetts', 'New Jersey', 'Pennsylvania']
COLLEGE_STATE_ABBRS = ['CA', 'CT', 'CA', 'NY', 'MA', 'MA', 'NJ', 'PA']
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