
import semanticrolelabeling.*;
import edu.stanford.nlp.trees.Tree;
import java.net.*;
import java.io.*;
import java.util.*;

import java.io.File;
import java.io.FileReader;

import opennlp.maxent.BasicContextGenerator;
import opennlp.maxent.ContextGenerator;
import opennlp.maxent.DataStream;
import opennlp.maxent.PlainTextByLineDataStream;
import opennlp.model.GenericModelReader;
import opennlp.model.MaxentModel;
import opennlp.model.RealValueFileEventStream;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;


public class ConceptExtractorServer {
	static ServerSocket socket1;
	protected final static int port = 19999;
	static Socket connection;
	//static boolean first;
	//static StringBuffer process;
	
	
    MaxentModel _model;
    ContextGenerator _cg = new BasicContextGenerator();
    
    public ConceptExtractorServer (MaxentModel m) {
	_model = m;
    }
    
    private void eval (String predicates) {
      eval(predicates,false);
    }
    
    private String eval (String predicates, boolean real) {
      String[] contexts = predicates.split(" ");
      double[] ocs;
	  String AllOutcomes;
	  String BestOutcomes;
	  int best_idx;
	  double[] ocs_best;
	  int start1,end1;
      if (!real) {
        ocs = _model.eval(contexts);
      }
      else {
        float[] values = RealValueFileEventStream.parseContexts(contexts);
        ocs = _model.eval(contexts,values);
      }
      AllOutcomes=_model.getAllOutcomes(ocs);
	  BestOutcomes=_model.getBestOutcome(ocs);
	  start1=AllOutcomes.indexOf(BestOutcomes)+BestOutcomes.length()+1;
	  end1=start1+6;
	  return (_model.getBestOutcome(ocs)+" "+AllOutcomes.substring(start1,end1)+"\n");
	
    }
    
    private static void usage() {
      
    }
 
    public static void main(String[] args) {
	try{
	socket1 = new ServerSocket(port);
    int character;
	
	String  modelFileName,modelFileNameClassifier;
    boolean real = false;
    //String type = "maxent";
    //int ai = 0;
	
	modelFileName = "../models/identifierModel.txt";
	modelFileNameClassifier = "../models/classifierModel.txt";
	
	Parser parser = new Parser();
	
	ConceptExtractorServer predictorIdentifier = null;
	ConceptExtractorServer predictorClassifier = null;
	try {
      MaxentModel m = new GenericModelReader(new File(modelFileName)).getModel();
	  MaxentModel m2 = new GenericModelReader(new File(modelFileNameClassifier)).getModel();
	  predictorIdentifier = new ConceptExtractorServer(m);
	  predictorClassifier = new ConceptExtractorServer(m2);
	  //Parser parser = new Parser();
	} catch (Exception e) {
	    e.printStackTrace();
	    System.exit(0);
	}
		
	System.out.println("Server Initialized, Waiting for input...");
	while (true) {
	
		
		try{
		connection = socket1.accept();
		
        BufferedReader fromClient = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			
		String sentence;
		sentence = fromClient.readLine();
		
		Tree tree = parser.parse(sentence); 
		//System.out.println(tree);
			
		//System.out.println("Extracting features...");
		//String srlIdentifier = "python srl-identifier.py " + '"'+tree+'"' ;
		String srlIdentifier = "python featureExtractorClient.py " + '"'+tree+'"' ;
		//System.out.println(srlIdentifier);
		Runtime rr = Runtime.getRuntime();
        Process pp = rr.exec(srlIdentifier);
        BufferedReader brr = new BufferedReader(new InputStreamReader(pp.getInputStream()));
		//System.out.println("Semantic Role Labeling...");
		pp.waitFor(); 
		BufferedReader reader = new BufferedReader(new FileReader("../temp/identifier-features.txt"));
		BufferedReader classifier = new BufferedReader(new FileReader("../temp/classifier-features.txt"));
		
		PrintWriter identifierOutput = new PrintWriter("../temp/identifier-output.txt");
		PrintWriter classifierOutput = new PrintWriter("../temp/classifier-output.txt");
		BufferedReader preds = new BufferedReader(new FileReader("../temp/pred.test"));
				
		String line;
		while ((line = reader.readLine()) != null)
			{
			//System.out.println("inside loop");
			String pred = preds.readLine();
			String identifierFeatures = line; 
			String classifierFeature = classifier.readLine();
			
			String identOutput = predictorIdentifier.eval(identifierFeatures.substring(0, identifierFeatures.lastIndexOf(' ')),real);
			String classiOutput = predictorClassifier.eval(classifierFeature.substring(0, classifierFeature.lastIndexOf(' ')),real);
			identifierOutput.println(identOutput);
			classifierOutput.println(pred+' '+classiOutput);
			
			}
			identifierOutput.close();
			classifierOutput.close();
			
		System.out.println("Serverd!");
        String returnCode = "Concepts:" + (char) 13;
        BufferedOutputStream os = new BufferedOutputStream(connection.getOutputStream());
        OutputStreamWriter osw = new OutputStreamWriter(os, "US-ASCII");
        osw.write(returnCode);
        osw.flush();
		}
		catch (Exception e)
        {
		String cause = e.getMessage();
		if (cause.equals("python: not found"))
			System.out.println("No python interpreter found.");
        }
		
		System.out.println("Waiting.....");
		
     } 
    }
	catch (IOException e) {}
	}
	
	
    }
    

