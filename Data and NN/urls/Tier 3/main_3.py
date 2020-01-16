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
"https://talk.collegeconfidential.com/university-california-berkeley/1756889-uc-berkeley-class-of-2019-decision-stats-only.html",
"https://talk.collegeconfidential.com/university-california-berkeley/1860923-uc-berkeley-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/university-california-berkeley/1962787-uc-berkeley-class-of-2021-results-thread.html",
"https://talk.collegeconfidential.com/university-california-berkeley/2035401-uc-berkeley-class-of-2022-applicants-thread.html",
"https://talk.collegeconfidential.com/university-california-berkeley/2129467-uc-berkeley-class-of-2023-decision-thread-stats-only.html"
],
            [
"https://talk.collegeconfidential.com/bowdoin-college/1717543-official-class-of-2019-ed-i-results.html",
"https://talk.collegeconfidential.com/bowdoin-college/1754822-class-of-2019-official-rd-results.html",
"https://talk.collegeconfidential.com/bowdoin-college/1957006-bowdoin-rd-2021.html",
"https://talk.collegeconfidential.com/bowdoin-college/2131340-bowdoin-class-of-2023-rd-results.html",
"https://talk.collegeconfidential.com/bowdoin-college/2115925-bowdoin-ed-2023-results.html"
],
                    [
"https://talk.collegeconfidential.com/carnegie-mellon-university/1706803-carnegie-mellon-class-of-2019-rd-discussion-and-results-thread.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/1756750-carnegie-mellon-university-class-of-2019-rd-decision-only.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/1840086-official-carnegie-mellon-class-of-2020-ed-results.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/1870686-carnegie-mellon-university-class-of-2020-rd-decision-only.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/1943729-carnegie-mellon-class-of-2021-ed-results.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/1962791-official-carnegie-mellon-university-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/2069507-carnegie-mellon-regular-decision-results-class-of-2022.html",
"https://talk.collegeconfidential.com/carnegie-mellon-university/2104611-carnegie-mellon-university-class-of-2023-ed-thread.html"
],
                            [
"https://talk.collegeconfidential.com/emory-university/1756866-emory-university-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/emory-university/1717359-official-emory-university-class-of-2019-ed-results.html",
"https://talk.collegeconfidential.com/emory-university/1841379-emory-ed1-results-class-of-2020.html",
"https://talk.collegeconfidential.com/emory-university/1876286-emory-class-of-2020-rd-results-thread.html",
"https://talk.collegeconfidential.com/emory-university/1862085-emory-edii-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/emory-university/1964165-official-emory-2021-edii-results-only-thread.html",
"https://talk.collegeconfidential.com/emory-university/2066384-emory-class-of-2022-rd-results-thread.html"
],
                                    
[
"https://talk.collegeconfidential.com/georgetown-university/1758923-georgetown-university-class-of-2019-rd-results-stats.html",
"https://talk.collegeconfidential.com/georgetown-university/1717864-class-of-2019-ea-results.html",
"https://talk.collegeconfidential.com/georgetown-university/1874556-georgetown-rd-results-thread-class-of-2020.html",
"https://talk.collegeconfidential.com/georgetown-university/1837952-georgetown-ea-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/georgetown-university/1839346-class-of-2020-ea-results.html",
"https://talk.collegeconfidential.com/georgetown-university/1976674-georgetown-class-of-2021-rd-results.html",
"https://talk.collegeconfidential.com/georgetown-university/1942651-georgetown-2021-ea-results.html",
"https://talk.collegeconfidential.com/georgetown-university/1976481-georgetown-2021-rd-decisions.html",
"https://talk.collegeconfidential.com/georgetown-university/2067556-official-georgetown-class-of-2022-rd-results.html",
"https://talk.collegeconfidential.com/georgetown-university/2040271-georgetown-2022-ea-results.html",
"https://talk.collegeconfidential.com/georgetown-university/2116429-georgetown-ea-results-2023.html"
],
    [
"https://talk.collegeconfidential.com/new-york-university/1764054-nyu-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/new-york-university/1715163-official-new-york-university-class-of-2019-ed-1-results.html",
"https://talk.collegeconfidential.com/new-york-university/1750723-official-nyu-rd-class-of-2019-decisions-thread.html",
"https://talk.collegeconfidential.com/new-york-university/1861791-official-new-york-university-class-of-2020-ed-2-results.html",
"https://talk.collegeconfidential.com/new-york-university/1868597-nyu-rd-2020-discussion-results.html",
"https://talk.collegeconfidential.com/new-york-university/1841254-nyu-ed1-class-of-2020-decisions.html",
"https://talk.collegeconfidential.com/new-york-university/1946143-nyu-ed-i-2021-decisions.html",
"https://talk.collegeconfidential.com/new-york-university/2045187-nyu-rd-class-of-2022.html",
"https://talk.collegeconfidential.com/new-york-university/2134075-nyu-rd-class-of-2023-results-only.html",
"https://talk.collegeconfidential.com/new-york-university/2116813-nyu-ed-ii-class-of-2023.html"
],
[
"https://talk.collegeconfidential.com/university-notre-dame/1754423-official-notre-dame-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/university-notre-dame/1717386-official-notre-dame-class-of-2019-rea-decisions-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/1841226-notre-dame-ea-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/1870150-official-notre-dame-class-of-2020-rd-decisions-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/1945033-official-notre-dame-regular-decision-class-of-2021-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/1943879-official-notre-dame-class-of-2021-rea-decisions-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/2065975-official-notre-dame-class-of-2022-rd-decisions-results-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/2040005-official-notre-dame-class-of-2022-rea-decisions-results-thread.html",
"https://talk.collegeconfidential.com/university-notre-dame/2115112-notre-dame-class-of-2023-rea-decisions-results-thread.html"
],
[
"https://talk.collegeconfidential.com/rice-university/1754474-rice-university-class-of-2019-results-decisions.html",
"https://talk.collegeconfidential.com/rice-university/1704925-rice-ed-class-of-2019-results-official-thread.html",
"https://talk.collegeconfidential.com/rice-university/1823896-rice-university-ed-class-of-2020-official-thread.html",
"https://talk.collegeconfidential.com/rice-university/1977659-official-rice-class-of-2021-regular-decision-results-only.html",
"https://talk.collegeconfidential.com/rice-university/2066631-rice-class-of-2022-rd-results.html",
"https://talk.collegeconfidential.com/rice-university/2133687-rice-rd-class-of-2023-results-only.html",
"https://talk.collegeconfidential.com/rice-university/2109973-rice-university-class-of-2023-rd-thread.html"
],
 [
"https://talk.collegeconfidential.com/tufts-university/1719148-official-tufts-university-class-of-2019-ed1-decision-thread.html",
"https://talk.collegeconfidential.com/tufts-university/1876660-tufts-class-of-2020-rd-results-thread.html",
"https://talk.collegeconfidential.com/tufts-university/1860732-tufts-edii-class-of-2020-results.html",
"https://talk.collegeconfidential.com/tufts-university/1970678-tufts-class-of-2021-rd-results.html",
"https://talk.collegeconfidential.com/tufts-university/1943713-tufts-class-of-2021-ed-results.html",
"https://talk.collegeconfidential.com/tufts-university/2068756-tufts-class-of-2022-rd-results-only.html",
"https://talk.collegeconfidential.com/tufts-university/2038499-tufts-class-of-2022-ed-results.html",
"https://talk.collegeconfidential.com/tufts-university/2115531-tufts-ed-class-of-2023-results-only.html"
],
  [
"https://talk.collegeconfidential.com/university-california-los-angeles/1753982-ucla-class-of-2019-decisions-only.html",
"https://talk.collegeconfidential.com/university-california-los-angeles/1871389-ucla-class-of-2020-decisions-only.html",
"https://talk.collegeconfidential.com/university-california-los-angeles/1971538-ucla-class-of-2021-admission-decisions.html",
"https://talk.collegeconfidential.com/university-california-los-angeles/2129460-ucla-class-of-2023-decision-thread-stats-only.html"
],
   [
"https://talk.collegeconfidential.com/university-southern-california/1719773-official-usc-class-of-2019-results-discussion-thread-p184.html",
"https://talk.collegeconfidential.com/university-southern-california/1719773-official-usc-class-of-2019-results-discussion-thread.html",
"https://talk.collegeconfidential.com/university-southern-california/1842387-usc-class-of-2020-results-discussion-thread-p280.html",
"https://talk.collegeconfidential.com/university-southern-california/1938675-usc-class-of-2021-discussion-results-thread.html",
"https://talk.collegeconfidential.com/university-southern-california/2050692-usc-class-of-2022-decisions-stats-only-thread.html",
"https://talk.collegeconfidential.com/university-southern-california/2122705-usc-class-of-2023-decisions-stats-only-thread.html"
],
[
"https://talk.collegeconfidential.com/vanderbilt-university/1754841-vanderbilt-class-of-2019-rd-results.html",
"https://talk.collegeconfidential.com/vanderbilt-university/1742962-offical-class-of-2019-ed-results-only.html",
"https://talk.collegeconfidential.com/vanderbilt-university/1867510-official-vanderbilt-class-of-2020-results-thread.html",
"https://talk.collegeconfidential.com/vanderbilt-university/1839658-official-vanderbilt-2020-ed1-results-thread.html",
"https://talk.collegeconfidential.com/vanderbilt-university/1946231-official-vanderbilt-class-of-2021-results-thread.html",
"https://talk.collegeconfidential.com/vanderbilt-university/2057513-official-vanderbilt-class-of-2022-rd-results-thread.html",
"https://talk.collegeconfidential.com/vanderbilt-university/2043900-vanderbilt-ed2-class-of-2022-thread.html",
"https://talk.collegeconfidential.com/vanderbilt-university/2133693-vandy-rd-class-of-2023-results-only.html"
],
[
"https://talk.collegeconfidential.com/washington-university-st-louis/1749558-wustl-rd-2019-decision-thread.html",
"https://talk.collegeconfidential.com/washington-university-st-louis/1839656-wash-u-class-of-2020-results-only-thread.html",
"https://talk.collegeconfidential.com/washington-university-st-louis/1837301-wustl-ed-class-of-2020.html",
"https://talk.collegeconfidential.com/washington-university-st-louis/1944038-wash-u-2021-results-only-thread.html",
"https://talk.collegeconfidential.com/washington-university-st-louis/1951310-class-of-2021-scholarship-discussion-results.html",
"https://talk.collegeconfidential.com/washington-university-st-louis/2115572-washu-2023-ed-results-only-thread.html",
"https://talk.collegeconfidential.com/washington-university-st-louis/2132218-class-of-2023-rd-results-only-washington-u-sl.html"
]
]

FILE_NAME = "Tier 3"
COLLEGE_STATE_NAMES = ['California', 'Maine', 'Pennsylvania', 'Georgia', 'Maryland', 'California', 'Maryland', 'New York', 'Indiana', 'Texas', 'Massachusetts', 'California', 'California', 'Tennessee', 'Missouri']
COLLEGE_STATE_ABBRS = ['CA', 'ME', 'PA', 'GA', 'MD', 'NY', 'IN', 'TX', 'MA', 'CA', 'CA', 'TN', 'MO']
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