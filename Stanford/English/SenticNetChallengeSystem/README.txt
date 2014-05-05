
COMPILE CLIENT
==============
>javac -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3-bin\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar ConceptExtractorBatchClient.java

RUN CLIENT
============

>java -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3-bin\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar ConceptExtractorBatchClient

COMPILE SERVER
==============

>javac -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3-bin\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar ConceptExtractorServer.java

RUN SERVER
==========

>java -cp .;..\stanford-parser-full-2014-01-04\stanford-parser.jar;..\stanford-parser-full-2014-01-04\stanford-parser-3.3.1-models.jar;..\classifier\maxent\lib\trove-3.0.3.jar;..\apache-opennlp-1.5.3-bin\apache-opennlp-1.5.3\lib\opennlp-maxent-3.0.3.jar ConceptExtractorServer

RUN PYTHON SERVER
=================

>python featureExtractorServer.py



