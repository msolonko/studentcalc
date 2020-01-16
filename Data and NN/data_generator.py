import numpy as np
import csv

def generate(act_min, act_max, gpa_min, gpa_max, sat2_min, sat2_max, num, file_name):
    #generates data rows and saves them
    
    #empty lists for data
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
    
    #data generation
    for i in range(num):        
        decision_list.append(0)
        gpa_list.append(round(gpa_min + np.random.random() * (gpa_max - gpa_min), 2))
        act_list.append(round(act_min + np.random.random() * (act_max - act_min)))
        subject_test_list.append(round(sat2_min + np.random.random() * (sat2_max - sat2_min)))
        gender_list.append(round(np.random.random()))
        ethnicity_list.append(round(np.random.random() * 3 - 1))
        essay_list.append(round(np.random.random() * 6 + 4, 1))
        rec_list.append(round(np.random.random() * 6 + 4, 1))
        school_type_list.append(round(np.random.random()))
        region_list.append(round(np.random.random() * 4))
        
    decision_list = [[val] for val in list(map(str, decision_list))]
    act_list = [[val] for val in list(map(str, act_list))]
    gpa_list = [[val] for val in list(map(str, gpa_list))]
    subject_test_list = [[val] for val in list(map(str, subject_test_list))]
    essay_list = [[val] for val in list(map(str, essay_list))]
    rec_list = [[val] for val in list(map(str, rec_list))]
    gender_list = [[val] for val in list(map(str, gender_list))]
    ethnicity_list = [[val] for val in list(map(str, ethnicity_list))]
    school_type_list = [[val] for val in list(map(str, school_type_list))]
    region_list = [[val] for val in list(map(str, region_list))]
    
    data = [['Decision', 'GPA', 'ACT', 'SAT II', 'Gender', 'Ethnicity', 'Essay', 'Recommendation', 'School Type', 'Region']] + [a + b + c + d + e + f + g + h + i + j for a, b, c, d, e, f, g, h, i, j in zip(decision_list, gpa_list, act_list, subject_test_list, gender_list, ethnicity_list, essay_list, rec_list, school_type_list, region_list)]
    saveData(data, file_name)   
        
def saveData(data, name):
    #saves data to CSV file
    file_name = name+".csv"
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
    csvFile.close()
    print("Data saved to CSV")    


generate(9, 24, 3.5, 4.0, 500, 650, 15, "low_scores_tier_41")
generate(28, 33, 0, 2.92, 500, 680, 15, "low_scores_tier_42")