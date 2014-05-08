BUILDING MODELS
===============
1. Run python build-model.py from './system/' to build 10 probabilistic modesls, and also train.dat file for training maximum entropy models
2. Copy train.dat file to ../classifier/maxent/ and run the following command inside maxent folder

maxent>java -cp .;.\lib\trove-3.0.3.jar;.\output\classes CreateModel train.dat

This will create trainModel.txt file, copy this file to 'system/models' folder

RUNNING THE SYSTEM
==================
1. Copy the tree to be labeled in input.txt file
2. Run python server by running the following command inside 'system' folder
	>python SRLServer.py
3. Run java server by running the following command inside 'system' folder
	>java -cp .;..\classifier\maxent\lib\trove-3.0.3.jar;..\classifier\maxent\output\classes SRLServer
	
4. Run java client program to do SRL

	>java -cp .;..\classifier\maxent\lib\trove-3.0.3.jar;..\classifier\maxent\output\classes SRLClient

5. The output is placed inside output.txt file