import base64
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import zscore
from sklearn.metrics import accuracy_score
from sklearn import preprocessing

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.callbacks import EarlyStopping
from keras.callbacks import TensorBoard
from sklearn import metrics
from sklearn.metrics import confusion_matrix, zero_one_loss
from sklearn.model_selection import train_test_split
import itertools
from keras.utils import plot_model



ENCODING = 'utf-8'

path = "C:/Users/javie/Desktop/Datasets/1Mdataset.csv"

# Encode text values to dummy variables(i.e. [1,0,0],[0,1,0],[0,0,1] for red,green,blue)
def encode_text_dummy(df, name):
    dummies = pd.get_dummies(df[name])
    for x in dummies.columns:
        dummy_name = f"{name}-{x}"
        df[dummy_name] = dummies[x]
    df.drop(name, axis=1, inplace=True)


# Encode text values to a single dummy variable.  The new columns (which do not replace the old) will have a 1
# at every location where the original column (name) matches each of the target_values.  One column is added for
# each target value.
def encode_text_single_dummy(df, name, target_values):
    for tv in target_values:
        l = list(df[name].astype(str))
        l = [1 if str(x) == str(tv) else 0 for x in l]
        name2 = f"{name}-{tv}"
        df[name2] = l


# Encode text values to indexes(i.e. [1],[2],[3] for red,green,blue).
def encode_text_index(df, name):
    le = preprocessing.LabelEncoder()
    df[name] = le.fit_transform(df[name])
    return le.classes_


# Encode a numeric column as zscores
def encode_numeric_zscore(df, name, mean=None, sd=None):
    if mean is None:
        mean = df[name].mean()

    if sd is None:
        sd = df[name].std()

    df[name] = (df[name] - mean) / sd


# Convert all missing values in the specified column to the median
def missing_median(df, name):
    med = df[name].median()
    df[name] = df[name].fillna(med)


# Convert all missing values in the specified column to the default
def missing_default(df, name, default_value):
    df[name] = df[name].fillna(default_value)


# Convert a Pandas dataframe to the x,y inputs that TensorFlow needs
def to_xy(df, target):
    result = []
    for x in df.columns:
        if x != target:
            result.append(x)
    # find out the type of the target column.  Is it really this hard? :(
    target_type = df[target].dtypes
    target_type = target_type[0] if hasattr(
        target_type, '__iter__') else target_type
    # Encode to int for classification, float otherwise. TensorFlow likes 32 bits.
    if target_type in (np.int64, np.int32):
        # Classification
        dummies = pd.get_dummies(df[target])
        return df[result].values.astype(np.float32), dummies.values.astype(np.float32)
    # Regression
    return df[result].values.astype(np.float32), df[[target]].values.astype(np.float32)

# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return f"{h}:{m:>02}:{s:>05.2f}"


# Regression chart.
def chart_regression(pred, y, sort=True):
    t = pd.DataFrame({'pred': pred, 'y': y.flatten()})
    if sort:
        t.sort_values(by=['y'], inplace=True)
    plt.plot(t['y'].tolist(), label='expected')
    plt.plot(t['pred'].tolist(), label='prediction')
    plt.ylabel('output')
    plt.legend()
    plt.show()

# Remove all rows where the specified column is +/- sd standard deviations
def remove_outliers(df, name, sd):
    drop_rows = df.index[(np.abs(df[name] - df[name].mean())
                          >= (sd * df[name].std()))]
    df.drop(drop_rows, axis=0, inplace=True)


# Encode a column to a range between normalized_low and normalized_high.
def encode_numeric_range(df, name, normalized_low=-1, normalized_high=1,
                         data_low=None, data_high=None):
    if data_low is None:
        data_low = min(df[name])
        data_high = max(df[name])

    df[name] = ((df[name] - data_low) / (data_high - data_low)) \
        * (normalized_high - normalized_low) + normalized_low

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Plot a confusion matrix.
# cm is the confusion matrix, names are the names of the classes.

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    plt.ioff()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig('test.png')
    

# Plot an ROC. pred - the predictions, y - the expected output.
def plot_roc(pred,y):
    fpr, tpr, _ = roc_curve(y, pred)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.show()

##########################################
#                  START                 #
##########################################

## Reading the file using chunksize to use less memory. Afterwards it concatenate all the columns into an unique dataframe.
df1 = pd.read_csv(path,encoding=ENCODING,low_memory=False,error_bad_lines=False,header=None,chunksize=100000)
df = pd.concat(df1, ignore_index=True)


#df = df.sample(n=500000, replace=False) # Uncomment this line to sample only 10% of the dataset

#Set columns name and attach it to the dataframe.
colname = ["Timestamp","Duration","Src_IP","Dst_IP","Src_Port","Dest_Port","Proto","Flags","Forward_Status","Service_type","Number_of_Packets","Bytes","Result"]
df.columns=colname

#Drop timestamps -> for now, they are not useful.
df.drop(columns=['Timestamp'],axis=1,inplace=True)
df.drop(columns=['Forward_Status'],axis=1,inplace=True)
df.dropna(inplace=True, axis=1)

print(df[0:10])

encode_numeric_zscore(df, 'Duration')
encode_text_index(df, 'Src_IP')
encode_text_index(df, 'Dst_IP')
encode_text_index(df, 'Src_Port')
encode_text_index(df, 'Dest_Port')
encode_text_index(df, 'Proto')
encode_text_index(df, 'Flags')
#encode_numeric_zscore(df, 'Forward_Status')
encode_numeric_zscore(df, 'Number_of_Packets')
encode_numeric_zscore(df, 'Bytes')

#If background set to 0, if attack set to 1
df.loc[df.Result != 'background', 'Result'] = 1
df.loc[df.Result == 'background', 'Result'] = 0

print(df[0:10])

print("Number of different results:")
print(df['Result'].value_counts())

##This will be x: everything except "result" column
features=df.columns.drop('Result')
x=df[features].values
#This will be y: just "result" column
dummies=pd.get_dummies(df['Result'])
results = dummies.columns
y=dummies.values
print(y)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=42)


model = Sequential()
model.add(Dense(50, input_dim=x.shape[1], kernel_initializer='normal', activation='relu'))
model.add(Dense(25,activation='relu',kernel_initializer='normal'))
model.add(Dense(y.shape[1], kernel_initializer='normal', activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("STARTING FIT")
model.fit(x_train,y_train,validation_data=(x_test,y_test), callbacks=None,epochs=1, batch_size=2)
print("FINISHING FIT")
plot_model(model, to_file='model.png')
pred = model.predict(x_test)
#plot_roc(pred,y_test)
cnf_matrix = confusion_matrix(y_test.argmax(axis=1), pred.argmax(axis=1))
print(cnf_matrix)
plot_confusion_matrix(cnf_matrix, classes=["No attack", "Attack"])
