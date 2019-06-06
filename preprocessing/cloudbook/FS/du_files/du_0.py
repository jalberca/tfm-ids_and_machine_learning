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

def f0():
#Automated code for global var:
 #fun_name: main final fun name: f0 globalName: done destiny du: 1 global_fun_name: f1
#============================global vars automatic code=========================
	#done
	if not hasattr(f0, "done"):
		f0.done = None

	if not hasattr(f0, "ver_done"):
		f0.ver_done = 0
        
	aux_done,aux_ver = invoker(['du_1'],'f1',"'None',"+str(f0.ver_done))
	if aux_done != "None":
		f0.done = aux_done
	done=f0.done
	f0.ver_done= aux_ver
	ver_done= f0.ver_done
		#	global done#Aqui va el chorrazo de codigo
	start = time.time()
	print("################# STARTING CLOUDBOOK-BASED DATASET PREPROCESSING #################")
	counter=0
	while(counter<13):
		#__NONBLOCKING__
		col = invoker(['du_2'], 'f2',str())
		invoker(['du_0'], 'cloudbook_th_counter',"'++'")
		invoker(['du_10000'], 'f3',str(col))
		counter+=1
	while json.loads(cloudbook_th_counter("")) > 0: #This was sync
			time.sleep(0.01)
	json.loads(f4())
	print("Total time", (time.time()-start))
	print("################# CLOUDBOOK DONE #################")

	return json.dumps('cloudbook: done') 

def f4():
	dataset = pd.DataFrame()
	files = os.listdir("/home/javier_alberca27/cloudbook_agent/FS/output")
	files = list(map(int,files))
	files.sort()
	print(files)
	for fname in files:
		piece = pd.read_csv("/home/javier_alberca27/cloudbook_agent/FS/output"+"/"+str(fname),sep=",",squeeze=True)
		dataset = pd.concat([dataset,piece],axis=1)
		print(dataset)
	dataset.to_csv("/home/javier_alberca27/cloudbook_agent/FS/output/FINALDATASET.csv",header=False,index=False)


	return json.dumps('cloudbook: done') 

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

def cloudbook_print(element):
	print (element)
	return "cloudbook: done"
	
def cloudbook_th_counter(value):
	if not hasattr(cloudbook_th_counter, "val"):
		cloudbook_th_counter.val = 0
	if not hasattr(cloudbook_th_counter, "cerrojo"):
		cloudbook_th_counter.cerrojo = Lock()
	if value == "++":
		with cloudbook_th_counter.cerrojo:
			cloudbook_th_counter.val += 1
	if value == "--":
		with cloudbook_th_counter.cerrojo:
			cloudbook_th_counter.val -= 1
	return json.dumps(cloudbook_th_counter.val)

def main():
	#f0()
	#return "cloudbook: done"
	return f0()

if __name__ == '__main__':
	f0()
			