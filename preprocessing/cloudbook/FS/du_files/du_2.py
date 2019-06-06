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

def f2():
#Automated code for global var:
 #fun_name: assign_piece final fun name: f2 globalName: done destiny du: 1 global_fun_name: f1
#============================global vars automatic code=========================
	#done
	if not hasattr(f2, "done"):
		f2.done = None

	if not hasattr(f2, "ver_done"):
		f2.ver_done = 0
        
	aux_done,aux_ver = invoker(['du_1'],'f1',"'None',"+str(f2.ver_done))
	if aux_done != "None":
		f2.done = aux_done
	done=f2.done
	f2.ver_done= aux_ver
	ver_done= f2.ver_done
		#	global done#Aqui va el chorrazo de codigo
	aux1 = ["Timestamp","Duration","Src_IP","Dst_IP","Src_Port","Dest_Port","Proto","Flags","Forward_Status","Service_type","Number_of_Packets","Bytes","Result"]
	chosen = random.choice(aux1)
	while(chosen in done):
		chosen = random.choice(aux1)
	col = aux1.index(chosen)
	print("The chosen is:",chosen)
	invoker(['du_1'], 'f1','"f1.done.append(\''+str(chosen)+'\')"'+' , '+str(ver_done))
	print("Already done:",done)
	return json.dumps(col)


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

