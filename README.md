# Anomaly-based Intrussion Detection System with machine learning and distributed execution.

##  Source code

### Dataset preprocessing

The dataset preprocessing has been done using Cloudbook. The original source code is available inside the folder *preprocessing*. The Cloudbook splitted software and the agent to run it in four different machines is inside the folder *cloudbook*.

Required dependencies:
`pip install flask, pynat urllib pandas numpy scikit-learn`

This folder has been prepared to be capable of executing the process_dataset original source code using Cloudbook.
There must be 4 agents to execute the distributed software. They must be on a local network.
Inside the FS folder, the deployable units are available in the du_files folder. The rest of the files are used by different parts of Cloudbook to perform their activities.
The FS folder must be SHARED between the different agents. I used NFS to solve that.

The agent can be launched in two modes: through the GUI or by command line.

- Launching agents with the GUI:

`python gui.py`

And follow the friendly instructions to create and launch agents.

- Launching agent with the command line:

`python agent.py agentN`

Where N is 0 to 3. Only one agent per machine.

When the agents are launched and the DUs have been loaded the execution can be started with: http://localhost/invoke?invoked_function=du_0.main'

------------

### Machine learning training scripts
There are three different scripts with different trials. Two of them are prepared to run over neural networks with TensorFlow and the last one is a decision tree.

#### Neural Networks
The file ***mlp_first_trial.py*** is the first approach to the IDS training with neural networks. It preprocess the dataset (not using the Cloudbook solution) encoding the labels as binary (1=attack, 0=no attack) and training with it.

It requires: 
`pip install numpy scipy scikit-learn matplotlib pandas tensorflow keras`

The file ***mlp_multi_gpu_model.py*** is prepared to use the already preprocessed dataset by Cloudbook and train over multiple GPUs at the same time. It uses Tensorflow and Keras to achieve that objective. It is prepared to run over 8 GPUs.

It requires: 
`pip install numpy scipy scikit-learn matplotlib pandas tensorflow-gpu keras`

The file ***mlp_data_generator.py*** is prepared to use the already preprocessed dataset by Cloudbook. To feed the deep learning generated model with information from the dataset, it uses a data generator to avoid loading the full dataset at the same time.

It requires: 
`pip install numpy scipy scikit-learn matplotlib pandas tensorflow keras`


#### Decision tree
The script ***decision_tree_model.py*** is prepared to use the already preprocessed dataset by Cloudbook. The script has the different algorithms for decision tree coded, but the only uncommented line is the decision tree model that achieved better results.

------------

## Additional files
As a simple example, inside the folder *datasets* two files have been included. The first one is a file containing 100,000 lines from the original dataset, it is called *100dataset.csv*. The second file contains the same 100,000 lines from the original dataset, but preprocessed with Cloudbook. The file is called *100preprocessed.csv*.

The files that were actually processed and used in each of the algorithms reach 20 gigabytes in size and it is impossible to upload them to GitHub.