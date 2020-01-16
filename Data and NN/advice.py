from keras.models import load_model
import numpy as np
from sklearn.externals import joblib #for loading standard scaler

'''This program makes slight changes to a students stats and then record the change in sigmoid output. The higher the output, the more important the change.'''

'''Use by inputting stats as well as threshold (should vary per Tier), also input file names for scaler and model'''


    #PERFECT: model.predict(scaler.transform(np.array([[4, 36, 800, 1, 2, 9, 9, 1, 3]])))
    #BAD: model.predict(scaler.transform(np.array([[3.6, 32, 710, 0, -1, 7, 7, 0, 1]])))



def analyze(gpa, act, sat2, gender, race, essay, recommendation, school, region, ACT_THRESHOLD, GPA_THRESHOLD, SAT2_THRESHOLD, REC_THRESHOLD, ESSAY_THRESHOLD, model_filename, scaler_filename):
    model = loadModel(model_filename)
    scaler = loadScaler(scaler_filename)
    baseline = runModel(model, scaler, np.array([[gpa, act, sat2, gender, race, essay, recommendation, school, region]]))
    
    #ACT
    if act < ACT_THRESHOLD:
        act_output = runModel(model, scaler, np.array([[gpa, ACT_THRESHOLD, sat2, gender, race, essay, recommendation, school, region]]))
    else:
        act_output = -1
    
    #GPA
    if gpa < GPA_THRESHOLD:
        gpa_output = runModel(model, scaler, np.array([[GPA_THRESHOLD, act, sat2, gender, race, essay, recommendation, school, region]]))
    else:
        gpa_output = -1
    
    #SAT2
    if sat2 < SAT2_THRESHOLD:
        sat2_output = runModel(model, scaler, np.array([[gpa, act, SAT2_THRESHOLD, gender, race, essay, recommendation, school, region]]))
    else:
        sat2_output = -1
        
    #Essay
    if essay < ESSAY_THRESHOLD:
        essay_output = runModel(model, scaler, np.array([[gpa, act, sat2, gender, race, ESSAY_THRESHOLD, recommendation, school, region]]))
    else:
        essay_output = -1
        
    #Recommendation
    if recommendation < REC_THRESHOLD:
        rec_output = runModel(model, scaler, np.array([[gpa, act, sat2, gender, race, essay, REC_THRESHOLD, school, region]]))
    else:
        rec_output = -1
        
    #Home State Applicant
    home_output = runModel(model, scaler, np.array([[gpa, act, sat2, gender, race, essay, recommendation, school, 4]]))

    
    #changes in output after small alterations
    deltas = {"act": act_output-baseline, "gpa": gpa_output-baseline, "sat2": sat2_output-baseline, "essay": essay_output-baseline, "recommendation": rec_output-baseline, "home": home_output-baseline}
    
    sorted_deltas = sorted(deltas.items(), key=lambda x: x[1], reverse=True)
    print(sorted_deltas)
    
    print("#1 Improvement is: ")
    print(sorted_deltas[0][0])
    print("#2 Improvement is: ")
    print(sorted_deltas[1][0])
    print("#3 Improvement is: ")
    print(sorted_deltas[2][0])
    
def runModel(model, scaler, data):
    return model.predict(scaler.transform(data))[0][0]

def loadModel(name=None):
    # load json and create model
    fileName = name+".h5"
    print("Loading model from file: " + fileName + "...")
    return load_model(fileName)
def loadScaler(name):
    #load scaler
    fileName = name+".save"
    print("Loading scaler from file: " + fileName + "...")
    return joblib.load(fileName) 