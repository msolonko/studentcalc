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
URL_LISTS = [[
"https://talk.collegeconfidential.com/brown-university/1713666-brown-class-of-2019-ed-results-thread.html",
"https://talk.collegeconfidential.com/brown-university/1752948-brown-university-rd-class-of-2019-results.html",
"https://talk.collegeconfidential.com/brown-university/1870558-official-brown-2020-regular-decision-results-thread.html",
"https://talk.collegeconfidential.com/brown-university/1839447-brown-class-of-2020-early-decision-results-only.html",
"https://talk.collegeconfidential.com/brown-university/1977682-official-brown-class-of-2021-rd-results.html", 
"https://talk.collegeconfidential.com/brown-university/1944026-official-brown-class-of-2021-ed-results-only.html",
"https://talk.collegeconfidential.com/brown-university/2040001-brown-ed-2022-results-thread.html",
"https://talk.collegeconfidential.com/brown-university/2115582-brown-2023-ed-results-thread.html",
"https://talk.collegeconfidential.com/brown-university/2095781-brown-class-of-2023-applicants-discussion.html"
],
            [
"https://talk.collegeconfidential.com/claremont-mckenna-college/1756488-claremont-mckenna-class-of-2019-official-results-thread.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/1715234-official-ed1-results-class-of-2019.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/1841884-claremont-mckenna-2020-decisions-thread.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/1968461-cmc-rd-class-of-2021-discussion-results-thread.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/1964135-cmc-ed2-class-of-2021-results-thread.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/2061152-cmc-class-of-2022-rd-applicants-thread.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/2108627-cmc-ed-1-class-of-2023.html",
"https://talk.collegeconfidential.com/claremont-mckenna-college/2129998-claremont-mckenna-rd-2023.html"
],
             
             [
"https://talk.collegeconfidential.com/cornell-university/1749631-official-cornell-university-class-of-2019-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/cornell-university/1713310-offical-class-of-2019-ed-results-only.html",
"https://talk.collegeconfidential.com/cornell-university/1867304-cornell-class-of-2020-rd-results-only.html",
"https://talk.collegeconfidential.com/cornell-university/1835971-cornell-class-of-2020-ed-results-only.html",
"https://talk.collegeconfidential.com/cornell-university/1940785-cornell-ed-class-of-2021-results-p1.html",
"https://talk.collegeconfidential.com/cornell-university/1977671-cornell-rd-class-of-2021-results.html",
"https://talk.collegeconfidential.com/cornell-university/1962789-official-cornell-university-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/cornell-university/2038991-cornell-ed-class-of-2022-results.html",
"https://talk.collegeconfidential.com/cornell-university/2070903-cornell-rd-class-of-2022-results.html",
"https://talk.collegeconfidential.com/cornell-university/2134011-cornell-rd-class-of-2023-results-only.html",
"https://talk.collegeconfidential.com/cornell-university/2113776-cornell-ed-class-of-2023-results.html"
],
              
            [
"https://talk.collegeconfidential.com/dartmouth-college/1755066-dartmouth-college-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/1716729-dartmouth-college-class-of-2019-ed-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/1876552-official-dartmouth-college-2020-rd-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/1836230-dartmouth-college-class-of-2020-ed-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/1977173-official-dartmouth-college-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/dartmouth-college/1945416-dartmouth-class-of-2021-early-decision-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/2067109-dartmouth-class-of-2022-rd-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/2039858-dartmouth-class-of-2022-early-decision-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/2115324-dartmouth-class-of-2023-early-decision-results.html",
"https://talk.collegeconfidential.com/dartmouth-college/2134015-dartmouth-rd-class-of-2023-results-only.html"
],
            
            [
"https://talk.collegeconfidential.com/duke-university/1755538-official-duke-2019-rd-results-only-thread.html",
"https://talk.collegeconfidential.com/duke-university/1714877-official-duke-2019-ed-results-only-thread.html",
"https://talk.collegeconfidential.com/duke-university/1872765-duke-university-rd-2020-results-thread.html",
"https://talk.collegeconfidential.com/duke-university/1837158-official-duke-2020-ed-results-only-thread.html",
"https://talk.collegeconfidential.com/duke-university/1977392-official-duke-rd-class-of-2021-results-thread.html",
"https://talk.collegeconfidential.com/duke-university/1945126-official-duke-2021-ed-results-only-thread.html",
"https://talk.collegeconfidential.com/duke-university/2040394-duke-ed-results-class-of-2022.html",
"https://talk.collegeconfidential.com/duke-university/2069046-duke-class-of-2022-results.html",
"https://talk.collegeconfidential.com/duke-university/2134134-duke-rd-class-of-2023-results-only.html",
"https://talk.collegeconfidential.com/duke-university/2115574-duke-class-of-2023-ed-results.html"
],
            
            [
"https://talk.collegeconfidential.com/harvey-mudd-college/1752949-official-hmc-class-of-2019-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/harvey-mudd-college/1717366-official-2019-ed-i-ii-results-thread.html",
"https://talk.collegeconfidential.com/harvey-mudd-college/1871451-harvey-mudd-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/harvey-mudd-college/2040482-harvey-mudd-class-of-2022-ed1-results-thread.html",
"https://talk.collegeconfidential.com/harvey-mudd-college/2115257-harvey-mudd-class-of-2023-ed1-result-thread.html"
],
             
            [
"https://talk.collegeconfidential.com/johns-hopkins-university/1717635-johns-hopkins-class-of-2019-results-ed.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/1753137-official-johns-hopkins-university-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/1837647-official-johns-hopkins-2020-ed-results.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/1871313-johns-hopkins-university-rd-2020-results-thread.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/1970639-official-johns-hopkins-2021-rd-results-only.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/1972922-johns-hopkins-class-of-2021-rd-results-only.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/1942783-johns-hopkins-2021-ed-decision-thread.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/2038852-johns-hopkins-ed-2022-results-only-thread.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/2064371-johns-hopkins-rd-class-of-2022-results-only.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/2116047-jhu-class-of-2023-ed-results-only.html",
"https://talk.collegeconfidential.com/johns-hopkins-university/2131144-johns-hopkins-rd-class-of-2023-results-only.html"
],
                    
           [
"https://talk.collegeconfidential.com/northwestern-university/1706068-official-northwestern-ed-class-of-2019-results.html",
"https://talk.collegeconfidential.com/northwestern-university/1753369-official-northwestern-university-class-of-2019-rd-results-thread.html",
"https://talk.collegeconfidential.com/northwestern-university/1840071-official-northwestern-ed-class-of-2020-results.html",
"https://talk.collegeconfidential.com/northwestern-university/1871074-northwestern-university-class-of-2020-rd-results-thread.html",
"https://talk.collegeconfidential.com/northwestern-university/1972933-northwestern-rd-results-class-of-2021.html",
"https://talk.collegeconfidential.com/northwestern-university/1942957-official-northwestern-2021-ed-results-only-thread.html",
"https://talk.collegeconfidential.com/northwestern-university/2066016-northwestern-class-of-2022-rd-results.html",
"https://talk.collegeconfidential.com/northwestern-university/2037853-official-northwestern-2022-ed-results-only-thread-p1.html",
"https://talk.collegeconfidential.com/northwestern-university/2132054-official-northwestern-class-of-2023-rd-results-thread.html",
"https://talk.collegeconfidential.com/northwestern-university/2115594-northwestern-class-of-2023-ed-results-thread.html"
],
[
"https://talk.collegeconfidential.com/pomona-college/1716453-pomona-stats-decisions-thread-for-the-class-of-2019.html",
"https://talk.collegeconfidential.com/pomona-college/1839379-class-of-2020-ed-results-thread.html",
"https://talk.collegeconfidential.com/pomona-college/1957097-official-pomona-college-class-of-2021-ed-edii-rd-results-thread.html",
"https://talk.collegeconfidential.com/pomona-college/1957097-official-pomona-college-class-of-2021-ed-edii-rd-results-thread.html",
"https://talk.collegeconfidential.com/pomona-college/2120585-pomona-class-of-2023-edii.html",
"https://talk.collegeconfidential.com/pomona-college/2113844-pomona-college-class-of-2023-ed-edi-rd-results-thread.html"
],
[
"https://talk.collegeconfidential.com/university-chicago/1748338-university-of-chicago-2019-rd-results.html",
"https://talk.collegeconfidential.com/university-chicago/1709510-university-of-chicago-class-of-2019-early-action-results-only.html",
"https://talk.collegeconfidential.com/university-chicago/1870805-uchicago-2020-rd-results.html",
"https://talk.collegeconfidential.com/university-chicago/1838644-uchicago-class-of-2020-early-action-results.html",
"https://talk.collegeconfidential.com/university-chicago/1972968-uchicago-rd-2021-results-thread.html", 
"https://talk.collegeconfidential.com/university-chicago/1964119-uchicago-class-of-2021-ed-ii-results.html",
"https://talk.collegeconfidential.com/university-chicago/2064326-university-of-chicago-class-of-2022-rd-results.html",
"https://talk.collegeconfidential.com/university-chicago/2036687-uchicago-class-of-2022-ea-edi-results-only.html",
"https://talk.collegeconfidential.com/university-chicago/2057114-uchicago-class-of-2022-edii-results-only.html",
"https://talk.collegeconfidential.com/university-chicago/2116712-uchicago-class-of-2023-ea-edi-results-only.html"
]
]

FILE_NAME = "Tier 2"
COLLEGE_STATE_NAMES = ['Rhode Island', 'California', 'New York', 'New Hampshire', 'North Carolina', 'California', 'Maryland', 'Illinois', 'California', 'Illinois']
COLLEGE_STATE_ABBRS = ['RI', 'CA', 'NY', 'NH', 'NC', 'CA', 'MD', 'IL', 'CA', 'IL']
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