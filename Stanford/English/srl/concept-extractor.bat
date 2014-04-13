@echo off
cd ..\stanford-parser
java -mx150m -cp "*;" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ..\srl\input.txt > ..\srl\parse-output.txt
cd ..\srl
python srl-identifier.py
cd ..\identifier\maxent
java -classpath .;./lib/trove-3.0.3.jar;./output/classes Predict train.test > output.txt
cd ..\..\classifier\maxent
java -classpath .;./lib/trove-3.0.3.jar;./output/classes Predict train.test > output.txt
cd ..\..\srl
python srl-labeler.py > output.txt
echo 'Done!'