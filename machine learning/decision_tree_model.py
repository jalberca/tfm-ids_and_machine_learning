############ DECISION TREES ############

import time
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import os     
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
from sklearn.metrics import multilabel_confusion_matrix, zero_one_loss
from sklearn.utils.multiclass import unique_labels
import numpy as np
import matplotlib.pyplot as plt
import itertools

#Only for Windows to print the PNG file representing the decision tree.
#os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


dataset = "/home/javier_alberca27/FINALDATASET.csv"
col_names = ["Duration","Src_IP","Dst_IP","Src_Port","Dest_Port","Proto","Flags","Service_type","Number_of_Packets","Bytes","Result"]
features = ["Duration","Src_Port","Dest_Port","Proto","Flags","Service_type","Number_of_Packets","Bytes"]

df1 = pd.read_csv(dataset,encoding="utf-8",names=col_names,low_memory=False,error_bad_lines=False,header=None,chunksize=100000)
df = pd.concat(df1, ignore_index=True)
df.drop(columns=['Src_IP'],axis=1,inplace=True)
df.drop(columns=['Dst_IP'],axis=1,inplace=True)
print(df[0:10])

x = df[features]
y = df.Result
print("Number of different results:")
print(y.value_counts())

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42) # 70% training and 30% test
var = time.time()

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(criterion='entropy',splitter='best',max_depth=10)
#clf = DecisionTreeClassifier(criterion='entropy',splitter='random',max_depth=10)
#clf = DecisionTreeClassifier(criterion='gini',splitter='best',max_depth=10)
#clf = DecisionTreeClassifier(criterion='gini',splitter='random',max_depth=10)

# Train Decision Tree Classifer
clf = clf.fit(x_train,y_train)

#Predict the response for test dataset
pred = clf.predict(x_test)
print("Training time:",time.time()-var) 
print("Accuracy:",metrics.accuracy_score(y_test, pred))
error = zero_one_loss(y_test, pred)
print ("Error:{}".format(error))

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = features,class_names=['dos','scan','botnet','blacklist','spam','background'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('decisiontree.png')
Image(graph.create_png())

print("pred{}".format(pred))
#pred = np.argmax(pred, axis=1)
y_eval = y_test
print("y_eval{}]".format(y_eval))

score = metrics.accuracy_score(y_eval, pred.round(), normalize=False)
print("Validation score: {}".format(score))

results = multilabel_confusion_matrix(y_test, pred)


print ("Confusion matrix:\n{}".format(results))


print(df["Result"].value_counts())
print(y_test[0:100])


from mlxtend.evaluate import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

cm = confusion_matrix(y_test, pred, binary=False)
print(cm)

fig, ax = plot_confusion_matrix(conf_mat=cm)
plt.savefig('cm.png')

#classes=['dos','scan','botnet','blacklist','Rest scan','spam','No attack']
