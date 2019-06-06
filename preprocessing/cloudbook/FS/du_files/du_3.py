import random
from scipy import stats
import time
import json
import os
from sklearn import preprocessing
import pandas as pd
import threading
from threading import Lock
import sys

invoker=None

def f3(col):
	threadf3 = threading.Thread(target= parallel_f3, daemon = False, args = [col])
	threadf3.start()
	return json.dumps("thread launched")

def parallel_f3(col):
	print("########################### SPLITTING COLUMN "+str(col)+" #################################")
	actual = time.time()
	data = pd.read_csv("/home/javier_alberca27/1Mdataset.csv",sep=',',usecols=[col],squeeze=True,encoding='utf-8',header=None)
	print(data[0:5])
	if(int(col) == 1 or int(col) == 10 or int(col) == 11):
		data = stats.zscore(data)
		data = pd.DataFrame(data)
		print("Processed Data:",data[0:5])
		data.dropna(inplace=True)
		data.to_csv("/home/javier_alberca27/cloudbook_agent/FS/output/"+str(col),header=False,index=False)
		print("Processing time",time.time()-actual)
	elif(int(col) == 0 or int(col) == 8):
		print("Column not to be processed")
	elif(int(col) == 12):
		data = data.replace(["dos","scan11","scan44","nerisbotnet","blacklist","anomaly-udpscan","anomaly-sshscan","anomaly-spam","background"], [0,1,1,2,3,4,4,5,6])
		print("Processed Data:",data[0:5])
		data.dropna(inplace=True)
		data.to_csv("/home/javier_alberca27/cloudbook_agent/FS/output/"+str(col),header=False,index=False)
		print("Processing time",time.time()-actual)
	else:
		le = preprocessing.LabelEncoder()
		data = le.fit_transform(data)
		data = pd.DataFrame(data)
		print("Processed Data:",data[0:5])
		data.dropna(inplace=True)
		data.to_csv("/home/javier_alberca27/cloudbook_agent/FS/output/"+str(col),header=False,index=False)
		print("Processing time",time.time()-actual)


	invoker(['du_0'], 'cloudbook_th_counter',"'--'")

	return json.dumps('cloudbook: done') 

