import json
import subprocess
import os, ast

def load_cloudbook(filename, configuration = None):
	with open(filename, "r") as file:
		txt = str(file.read())
		aux = dict(ast.literal_eval(txt))
		return aux

def load_cloudbook_agent_dus(my_agent_ID, cloudbook_dict_agents, configuration = None):
	# this function loads the list of deployable units belonging to certain agent ID
	#with open('./du_files/cloudbook_agents.json', 'r') as file:
	#	cloudbook_dict_agents = json.load(file)
	du_list=[]
	for du in cloudbook_dict_agents:
		for agent in cloudbook_dict_agents[du]:
			if agent == my_agent_ID:
				du_list.append(du)
	
	#my_agent_dict={}
	#for key in cloudbook_dict_agents:
	#	if (key==my_agent_ID):
	#		print ("-->",cloudbook_dict_agents.get(key))
	#		my_agent_dict=cloudbook_dict_agents.get(key)

	#du_list=[]
	#for key, value in my_agent_dict.items():
	#	du_list=value

	print (du_list)
	print ("du_list to load: "+str(du_list))
	return du_list
	#return ["du_0"]

def load_dictionary(filename, configuration = None):
	with open(filename, 'r') as file:
		aux = json.load(file)
	return aux

def write_dictionary(data, filename, configuration = None):
	with open(filename, 'w') as file:
		json_data=json.dumps(data)
		file.write(json_data)
		file.close()
	
"""

#Not neccesary like this as long as the cloudbook_dict will only contain the pair agent : du
def compute_dus(agents):
	

	dus={}

	max_du=0
	for key in agents:
		agent=agents.get(key)
		print ("agent", agent)
		for host,agent_dus in agent.items():
			for item in agent_dus:
				index =int (item[item.find("_")+1:])
				if index> max_du :
					max_du=index

	print ("max_du", max_du)
	print ("agents", agents)
	for i in range (0,max_du+1):
		print ("du=",i)
		du="du_"+str(i)
		dus[du]=[]
		for key in agents:
			agent=agents.get(key)
			for host,agent_dus in agent.items():
				if  du in agent_dus:
					dus[du].append(key)

	print ("------------------------")
	print (dus)
	print ("------------------------")
	return dus
"""


"""
def load_cloudbook_dus():
	# this function loads the list of dus and their machines
	with open('./du_files/cloudbook_dus.json', 'r') as file:
		dus = json.load(file)

	print "--- dus location loaded ---"
	print dus
	return dus

def load_cloudbook_agents():
	# this function loads the list of dus and their machines
	with open('./du_files/cloudbook_agents.json', 'r') as file:
		cloudbook_dict_agents = json.load(file)

	return cloudbook_dict_agents
"""