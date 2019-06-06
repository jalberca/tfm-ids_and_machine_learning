import time
import os
import random
import pandas as pd
from sklearn import preprocessing
from scipy import stats
import json

# Global vars
done = []

# This function assigns a single column to be processed.
def assign_piece():
	global done
	aux1 = ["Timestamp","Duration","Src_IP","Dst_IP","Src_Port","Dest_Port","Proto","Flags","Forward_Status","Service_type","Number_of_Packets","Bytes","Result"]
	chosen = random.choice(aux1)
	while(chosen in done):
		chosen = random.choice(aux1)
	col = aux1.index(chosen)
	print("The chosen is:",chosen)
	done.append(chosen)
	print("Already done:",done)
	return col

#__CLOUDBOOK:PARALLEL__
def process_piece(col):
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


def create_final_dataset():
	dataset = pd.DataFrame()
	files = os.listdir("/home/javier_alberca27/cloudbook_agent/FS/output")
	files = list(map(int,files))
	files.sort()
	print(files)
	for fname in files:
		piece = pd.read_csv("/home/javier_alberca27/cloudbook_agent/FS/output"+"/"+str(fname),sep=",",squeeze=True)
		dataset = pd.concat([dataset,piece],axis=1)
		print(dataset)
	piece=None
	dataset.to_csv("/home/javier_alberca27/cloudbook_agent/FS/output/FINALDATASET.csv",header=False,index=False)


def main():
	global done
	start = time.time()
	print("################# STARTING CLOUDBOOK-BASED DATASET PREPROCESSING #################")
	counter=0
	while(counter<13):
		#__NONBLOCKING__
		col = assign_piece()
		process_piece(col)
		counter+=1
	#SYNC
	create_final_dataset()
	print("Total time", (time.time()-start))
	print("################# CLOUDBOOK DONE #################")

main()