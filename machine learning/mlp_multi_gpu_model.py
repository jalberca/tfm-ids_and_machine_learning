############ MLP NEURAL NETWORK ############
# This script is prepared tu run over a machine with tensorflow-gpu and 8 GPUs.

import base64
import os
import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import zscore
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import time
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.callbacks import EarlyStopping
from keras.callbacks import TensorBoard
from sklearn import metrics
from sklearn.metrics import confusion_matrix, zero_one_loss
from sklearn.model_selection import train_test_split
import itertools



#dataset to load
data="/home/javier_alberca27/FINALDATASET.csv"

def load_data():
    ## Reading the file using chunksize to use less memory. Afterwards it concatenate all the columns into an unique dataframe.
    colname = ["Duration","Src_IP","Dst_IP","Src_Port","Dest_Port","Proto","Flags","Service_type","Number_of_Packets","Bytes","Result"]
    df1 = pd.read_csv(data,encoding='utf-8',low_memory=False,error_bad_lines=False,header=None,chunksize=100000)
    global df
    df = pd.concat(df1, ignore_index=True)

    #df.columns = df.iloc[0]
    df.columns = colname
    #df.drop(df.index[1])
    
    print("Dataset opened:")
    print(df[0:5])
    df.Result=df.Result.astype(int)
    print("Number of different results:")
    print(df['Result'].value_counts())
    print("Processing encoded dataframe:")
    ##This will be x: everything except "result" column
    features=df.loc[:,df.columns!='Result']
    #This will be y: just "result" column
    labels= df.Result.values.ravel()
    print(labels)
    global x
    global y
    x = pd.DataFrame(features)
    y = labels
    print(y.shape[0])


    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42)
    return (x_train, y_train), (x_test, y_test)


(x_train, y_train), (x_test, y_test) = load_data()
print("Done loading")

print ("Building model:")
var = time.time()
model = Sequential()

model.add(Dense(10,input_dim=x.shape[1], kernel_initializer='normal', activation='relu'))
model.add(Dense(15, kernel_initializer='random_normal', activation='relu'))
model.add(Dense(10, kernel_initializer='normal', activation='relu'))
model.add(Dense(y.shape[0],activation='softmax', kernel_initializer='random_normal'))

model = keras.utils.multi_gpu_model(model, cpu_relocation=True, gpus=8)
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=3, verbose=1, mode='auto')
print("STARTING FIT")
model.fit(x_train,y_train,validation_data=(x_test,y_test), callbacks=[monitor],epochs=100, batch_size=5)
print("FINISHING FIT")
print("Time needed:", time.time()-var)

model.save("firstmodel.h5")

pred = model.predict(x_test)
print(y_test)
print("pred{}".format(pred))
pred = np.argmax(pred, axis=1)
y_eval = y_test
print("y_eval{}]".format(y_eval))

score = metrics.accuracy_score(y_eval, pred.round(), normalize=False)
print("Validation score: {}".format(score))

results = confusion_matrix(y_test, pred)
error = zero_one_loss(y_test, pred)

print ("Confusion matrix:\n{}".format(results))
print ("Error:{}".format(error))

print(df["Result"].value_counts())


from mlxtend.evaluate import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

cm = confusion_matrix(y_test, pred, binary=False)
print(cm)

fig, ax = plot_confusion_matrix(conf_mat=cm)
plt.savefig('test.png')

#classes=['dos','scan','botnet','blacklist','Rest scan','spam','No attack']
