from keras.models import Sequential, load_model
from keras.layers import Dense
import numpy as np
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler #allows to reuse scale on new data
from sklearn.externals import joblib #for saving standard scaler

'''SOME INSTRUCTIONS
saveModel(model) saves it to a file (overloaded function [can specify a name to save it])
model = loadModel() loads model and weights (optional file name if titled differently)
'''

acc_list=scaler=X=Y=X_train=X_test=Y_train=Y_test=model=NAME=False

def start():
    global acc_list, scaler, X, Y, X_train, X_test, Y_train, Y_test, model, NAME
    data = np.loadtxt("sat2.csv", skiprows=1, delimiter = ",")
    X = data[0:1413,0:2]
    Y = data[0:1413,2]
        
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20)
    scaler = StandardScaler().fit(X_train) #defines a scaler and saves it
    X_test = scaler.transform(X_test) #applies transformation
    X_train = scaler.transform(X_train)
    #normal model
    model = Sequential()

    model.add(Dense(10, input_dim=np.shape(X)[1], activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='linear'))
    
    model.compile(loss='mse', optimizer='adam')
    #model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=1000, shuffle=True, batch_size=100)
    
    #Code to run 50 trials and save to disk the best model
    '''loss_list = []
    best_loss = 1e10
    num_epochs = 2000
    num_batches = 100
    for i in range(0, 20):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20)
        scaler = StandardScaler().fit(X_train) #defines a scaler and saves it
        X_test = scaler.transform(X_test) #applies transformation
        X_train = scaler.transform(X_train)
        md = Sequential()
        md.add(Dense(10, input_dim=np.shape(X)[1], activation='relu'))
        md.add(Dense(10, activation='relu'))
        md.add(Dense(1, activation='linear'))
        md.compile(loss='mse', optimizer='adam')
        print("Working on trial " + str(i))
        md.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=num_epochs, shuffle=True, batch_size=num_batches, verbose=0)
        loss = md.evaluate(X_test, Y_test)
        print("Loss: " + str(loss))
        loss_list.append(loss)
        if loss < best_loss:
            best_loss = loss
            saveModel(md)
            saveScaler(scaler)
            print("Best: " + str(best_loss))
    printAcc(loss_list)'''
    
    
    #PERFECT: model.predict(scaler.transform(np.array([[4, 36]])))
    #BAD: model.predict(scaler.transform(np.array([[3.6, 32]])))

#GRAPHING
def saveModel(mod):
    #save model
    mod.save("model_sat2.h5")
    print("Current model saved")
    
def loadModel():
    # load json and create model
    print("Loading model from file: model_sat2.h5...")
    return load_model("model_sat2.h5")

def saveScaler(scal):
    joblib.dump(scal, "scaler_sat2.save") 
    print("Scaler saved")
    
def loadScaler():
    #load scaler
    print("Loading scaler from file: scaler_sat2.save...")
    return joblib.load("scaler_sat2.save") 

def graphLoss(h):
    #graphs Loss and Accuracy (both train and validation)
    axes = plt.gca()
    axes.set_ylim([0.4,1.0])
    plt.plot(h.history['acc'], 'g')
    plt.title('Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.plot(h.history['val_acc'], 'r')
    plt.show()
    
    plt.plot(h.history['loss'], 'g')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')    
    plt.plot(h.history['val_loss'], 'r')
    plt.title('Loss')
    plt.show()
    
#used when many trials are run for statistics on validation accuracy
def printAcc(acc):
    print("Min: " + str(np.min(acc)))
    print("Mean: " + str(np.mean(acc)))
    print("Max: " + str(np.max(acc)))
    
start()