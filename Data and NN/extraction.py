# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 08:49:01 2018

@author: nicks
"""
import re
import numpy as np

#CONVERSIONS
gender = {"male":0, "female":1}
ethnicity = {"white":0, "asian":-1, "hispanic":1, "black":2, "native":2}
region = {"northeast":0, "midwest":1, "west":2, "south":3, "home":4}
decision = {"accepted":1, "rejected":0, "deferred":0, "waitlisted":0}
school = {"public":0, "private":1}

#ETHNICITY
white_pattern = re.compile(r'white|caucasian|european', re.IGNORECASE)
asian_pattern = re.compile(r'asian|korea|china|chinese|vietnam|india', re.IGNORECASE)
black_pattern = re.compile(r'black|african', re.IGNORECASE)
native_pattern = re.compile(r'native', re.IGNORECASE)
hispanic_pattern = re.compile(r'hispanic|latino|mexican|puerto|cuba|brazil|peru', re.IGNORECASE)
    
#GENDER
male_pattern = re.compile('(?<!fe)male|guy|boy|(?<!wo)man|m\s|\sm', re.IGNORECASE)
female_pattern = re.compile('female|woman|girl|f\s|\sf', re.IGNORECASE)
    
#ACCEPTANCE
decision_accepted = re.compile(r'accepted', re.IGNORECASE)
decision_rejected = re.compile(r'rejected', re.IGNORECASE)
decision_deferred = re.compile(r'deferred', re.IGNORECASE)
decision_waitlist = re.compile(r'waitlist', re.IGNORECASE)

#SCHOOL TYPE
school_private = re.compile(r'private', re.IGNORECASE)
school_public = re.compile(r'public', re.IGNORECASE)

#STATES
midwest_pattern = re.compile('(?<=:).*\s(North Dakota|ND|South Dakota|SD|Nebraska|NE|Kansas|KS|Iowa|IA|Missouri|MO|Minnesota|MN|Wisconsin|WI|Illinois|IL|Indiana|IN|Michigan|MI|Ohio|OH)(\W|$)', re.IGNORECASE)
west_pattern = re.compile('(?<=:).*\s(Alaska|AK|Hawaii|HI|Utah|UT|Colorado|CO|Arizona|AZ|New Mexico|NM|Washington|WA|Montana|MT|Oregon|OR|Idaho|ID|Wyoming|WY|California|CA|Nevada|ND)(\W|$)', re.IGNORECASE)
south_pattern = re.compile('(?<=:).*\s(Delaware|DE|Maryland|MD|Florida|FL|South Carolina|SC|North Carolina|NC|Virginia|VA|West Virginia|WV|Kentucky|KY|Tennessee|TN|Oklahoma|OK|Texas|TX|Arkansas|AR|Louisiana|LA|Mississippi|MS|Alabama|AL|Georgia|GA)(\W|$)', re.IGNORECASE)
northeast_pattern = re.compile('(?<=:).*\s(Massachusetts|MA|Connecticut|CT|Maine|ME|New Hampshire|NH|New Jersey|NJ|New York|NY|Pennsylvania|PA|Rhode Island|RI|Vermont|VT)(\W|$)', re.IGNORECASE)

        
#class that handles all extraction stuff
class Extractor:
    
    def getGPA(self, s):
        #assumes Unweighted GPA contained in string
        try:
            scores = [score for score in list(map(float, re.findall(r'(\d*\.\d+|\d+)/', s))) if score<=4 and score>=2.5]
            if len(scores) == 0:
                #if failed, try looking for standalone numbers after a colon (negative look ahead)
                scores = [score for score in list(map(float, re.findall(r'(\d*\.\d+|\d+)(?!.*:)', s))) if score<=4 and score>=2.5]
                return "False" if len(scores) == 0 else scores[0]
            else:
                return np.mean(scores)
        except:
            return -5
        
    def getRegion(self, s, state, abbr):
        #assumes string contains region
        
        #this line checks if student in same state as university
        home_state_pattern = re.compile('(?<=:).*\s('+state+'|'+abbr+')(\W|$)', re.IGNORECASE)
        if re.findall(home_state_pattern, s):
            #print(re.findall(home_state_pattern, s))
            return region["home"]
        elif re.findall(south_pattern, s):
            #print("south")
            return region["south"]
        elif re.findall(midwest_pattern, s):
            #print("midwest")
            return region["midwest"]
        elif re.findall(west_pattern, s):
            #print("west")
            return region["west"]
        elif re.findall(northeast_pattern, s):
           # print("northeast")
            return region["northeast"]
        else:
            return "False"
    
    def getEssay(self, s):
        #assumes essay score contained in string
        try:
            scores = [score for score in list(map(float, re.findall(r'(\d*\.\d+|\d+)/', s))) if score<=10]
            if len(scores) == 0:
                #if failed, try looking for standalone numbers after a colon (negative look ahead)
                scores = [score for score in list(map(float, re.findall(r'(\d*\.\d+|\d+)(?!.*:)', s))) if score<=10]
                if len(scores) == 0:
                    scores = [score for score in list(map(float, re.findall(r'(?<!1-)(?<!1-1)(\d*\.\d+|\d+)(?!-10)', s))) if score<=10]
                    return "False" if len(scores) == 0 else np.mean(scores)
                else:
                    return np.mean(scores)
            else:
                return np.mean(scores)
        except:
            return -5
    
    def getRec(self, s):
        #assumes rec rating contained in string (includes interview)
        try:
            scores = [score for score in list(map(float, re.findall(r'(\d*\.\d+|\d+)/', s))) if score<=10 and score>=5]
            if len(scores) == 0:
                #if failed, try looking for standalone numbers after a colon (negative look ahead)
                scores = [score for score in list(map(float, re.findall(r'(\d*\.\d+|\d+)(?!.*:)', s))) if score<=10 and score>=5]
                return np.mean(scores) if len(scores) == 1 else "False"
            else:
                return np.mean(scores) 
        except:
            return -5
    
    def getEthnicity(self, s):
        #assumes string contains ethnicity
        if re.findall(native_pattern, s):
            return ethnicity["native"]
        elif re.findall(black_pattern, s):
            return ethnicity["black"]
        elif re.findall(hispanic_pattern, s):
            return ethnicity["hispanic"]
        elif re.findall(white_pattern, s):
            return ethnicity["white"]
        elif re.findall(asian_pattern, s):
            return ethnicity["asian"]
        else:
            return "False"
        
        
    def getGender(self, s):
        #assumes string contains gender
        if re.findall(female_pattern, s):
            return gender["female"]
        elif re.findall(male_pattern, s):
            return gender["male"]
        else:
            return "False"
        
    def getRank(self, s):
        #assumes line includes rank
        numerator = re.findall(r'\d+(?=/)', s)
        denominator = re.findall(r'(?<=/)\d+', s)
        if len(numerator) > 0 and len(denominator) > 0:
            return round(int(float(numerator[0]))/int(float(denominator[0]))*100, 2)
        else:
            return "False"
        
                
    def getACT(self, s):
        #assumes line contains ACT keyword
        try:
            act = [score for score in list(map(int, re.findall('(\d*\.\d+|\d+)', s ))) if score>12]
            return "False" if len(act) == 0 else int(round(np.mean(act)))
        except:
            return -5
        
    def getSAT(self, s):
        #assumes line contains SAT I keyword
        try:
            sat = [score for score in list(map(int, re.findall('(\d*\.\d+|\d+)', s ))) if score>24]
            if len(sat) == 0:
                return "False"
            else:
                return np.sum(sat) if np.max(sat) <= 800 else np.max(sat)
        except:
            return -5
        
    def getSchoolType(self, s):
        #assumes line includes school type
        if school_private.search(s):
            return school["private"]
        elif school_public.search(s):
            return school["public"]
        else:
            return "False"
        
    def getSubjectTests(self, s):
        #assumes line contains SAT I keyword
        try:
            sat = [score for score in list(map(int, re.findall('(\d*\.\d+|\d+)', s))) if score>200]
            return "False" if len(sat) == 0 else int(float(np.mean(sat)))
        except:
            return -5
    
    def getDecision(self, s):
        #assumes string contains decision keyword
        if decision_accepted.search(s):
            return decision["accepted"]
        elif decision_rejected.search(s):
            return decision["rejected"]
        elif decision_deferred.search(s):
            return decision["deferred"]
        elif decision_waitlist.search(s):
            return decision["waitlisted"]
        else:
            return "False"