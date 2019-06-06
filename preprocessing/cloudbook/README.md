# AGENTS for dataset processing with Cloudbook
This folder has been prepared to be capable of executing the process_dataset original source code using Cloudbook.
There must be 4 agents to execute the distributed software. They must be on a local network.
Inside the FS folder, the deployable units are available in the du_files folder. The rest of the files are used by different parts of Cloudbook to perform their activities.
The FS folder must be SHARED between the different agents. I used NFS to solve that.

It requires the following libraries: pynat, flask and urllib.

To launch the application, it can be done in two different ways: through the GUI or by command line.
- Launching agents with the GUI:

	`python gui.py`

	And launch one agent per machine.
 
- Launching agent with the command line:

	`python agent.py agentN`  

	Where is 0 to 3. Only one agent per machine.
  
 
When the agents are launched and the DUs have been loaded the execution can be started with:
`http://localhost/invoke?invoked_function=du_0.main'`


