from keras.models import Sequential, load_model
from keras.layers import Dense
import numpy as np
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler #allows to reuse scale on new data
from keras.callbacks import EarlyStopping
from sklearn.externals import joblib #for saving standard scaler

'''SOME INSTRUCTIONS
saveModel(model) saves it to a file (overloaded function [can specify a name to save it])
model = loadModel() loads model and weights (optional file name if titled differently)
'''
earlyStopping = EarlyStopping(monitor='val_acc', 
                              patience=200,
                              restore_best_weights=True)
callbacks_list = [earlyStopping]
acc_list=scaler=X=Y=X_train=X_test=Y_train=Y_test=model=NAME=False

def start():
    global acc_list, scaler, X, Y, X_train, X_test, Y_train, Y_test, model, NAME
    NAME = "Tier 4"
    data = np.loadtxt(NAME+".csv", skiprows=1, delimiter = ",")
    X = data[0:,1:len(data)]

    Y = data[0:,0]
    
        
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20)
    scaler = StandardScaler().fit(X_train) #defines a scaler and saves it
    X_test = scaler.transform(X_test) #applies transformation
    X_train = scaler.transform(X_train)
    
    #normal model
    model = Sequential()
    model.add(Dense(6, input_dim=np.shape(X)[1], activation='relu'))
    model.add(Dense(1, activation='sigmoid'))   
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    #fitting/graphing
    history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test),callbacks=callbacks_list, epochs=200, shuffle=True, batch_size=32)
    graphLoss(history)
    
    
    #Code to run 50 trials and save to disk the best model
    acc_list = []
    best_accuracy = 0.0
    num_epochs = 700
    for i in range(0, 200):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20)
        scaler = StandardScaler().fit(X_train) #defines a scaler and saves it
        X_test = scaler.transform(X_test) #applies transformation
        X_train = scaler.transform(X_train)
        md = Sequential()
        md.add(Dense(6, input_dim=np.shape(X)[1], activation='relu'))
        md.add(Dense(1, activation='sigmoid'))
        md.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        print("Working on trial " + str(i))
        history = md.fit(X_train, Y_train, validation_data=(X_test, Y_test), callbacks=callbacks_list, epochs=num_epochs, shuffle=True, batch_size=32, verbose=0)
        acc = md.evaluate(X_test, Y_test)[1]
        print("Acc: " + str(acc))
        acc_list.append(acc)
        if acc > best_accuracy:
            best_accuracy = acc
            saveModel(md, "model_4")
            saveScaler(scaler, "scaler_4")
            print("Best: " + str(best_accuracy))
    printAcc(acc_list)
    
    
    #PERFECT: model.predict(scaler.transform(np.array([[4, 36, 800, 1, 2, 9, 9, 1, 3]])))
    #BAD: model.predict(scaler.transform(np.array([[3.6, 32, 710, 0, -1, 7, 7, 0, 1]])))

#GRAPHING
def saveModel(mod, name=None):
    if name == None:
        name = "model_"+NAME
    #save model
    mod.save(name+".h5")
    print("Current model saved")
    
def loadModel(name=None):
    # load json and create model
    if name == None:
        name = "model_"+NAME
    fileName = name+".h5"
    print("Loading model from file: " + fileName + "...")
    return load_model(fileName)

def saveScaler(scal, name=None):
    if name == None:
        name = "scaler_"+NAME
    #save scaler
    fileName = name+".save"
    joblib.dump(scal, fileName) 
    print("Scaler saved")
    
def loadScaler(name=None):
    #load scaler
    if name == None:
        name = "scaler_"+NAME
    fileName = name+".save"
    print("Loading scaler from file: " + fileName + "...")
    return joblib.load(fileName) 

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