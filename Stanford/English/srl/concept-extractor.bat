@echo off
cd ..\stanford-parser-full-2014-01-04
echo "Parsing"
java -mx150m -cp "*;" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ..\srl\input.txt > ..\srl\parse-output.txt
cd ..\srl
echo "Identification"
python srl-identifier.py
cd ..\identifier\maxent
java -classpath .;./lib/trove-3.0.3.jar;./output/classes Predict train.test > output.txt
cd ..\..\classifier\maxent
echo "Classification"
java -classpath .;./lib/trove-3.0.3.jar;./output/classes Predict train.test > output.txt
cd ..\..\srl
echo "Formulation"
REM python srl-labeler.py > output.txt
python concept-formulator.py
echo 'Done!'