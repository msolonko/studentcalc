import numpy as np
import csv

def generate(act_min, act_max, gpa_min, gpa_max, sat2_min, sat2_max, num, file_name):
    #generates data rows and saves them
    
    #empty lists for data
    gpa_list = []
    act_list = []
    subject_test_list = []
    
    #data generation
    for i in range(num):    
        gpa = gpa_min + i/num*(gpa_max-gpa_min) - 0.1 + 0.2 * np.random.random()
        act = act_min + i/num*(act_max-act_min) - 2 + 4 * np.random.random()
        sat2 = sat2_min + i/num*(sat2_max-sat2_min) - 20 + 40 * np.random.random()
        
        gpa_list.append(round(gpa, 2))
        act_list.append(round(act))
        subject_test_list.append(round(sat2))
        
    act_list = [[val] for val in list(map(str, act_list))]
    gpa_list = [[val] for val in list(map(str, gpa_list))]
    subject_test_list = [[val] for val in list(map(str, subject_test_list))]

    data = [['GPA', 'ACT', 'SAT II']] + [a + b + c for a, b, c in zip(gpa_list, act_list, subject_test_list)]
    saveData(data, file_name)   
        
def saveData(data, name):
    #saves data to CSV file
    file_name = name+".csv"
    with open(file_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
    csvFile.close()
    print("Data saved to CSV")    


generate(12, 24, 3.5, 4.0, 430, 630, 150, "sat2_data_1")
generate(28, 36, 0.5, 2.8, 430, 630, 150, "sat2_data_2")
generate(12, 24, 0.5, 2.8, 430, 580, 150, "sat2_data_3")