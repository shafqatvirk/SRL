python srl-identifier.py
cd ..\identifier\maxent
java -classpath .;./lib/trove-3.0.3.jar;./output/classes Predict train.test > output.txt
cd ..\..\classifier\maxent
java -classpath .;./lib/trove-3.0.3.jar;./output/classes Predict train.test > output.txt
cd ..\..\srl
python srl-labeler.py > output.txt