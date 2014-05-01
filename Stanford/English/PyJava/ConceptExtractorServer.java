///////////////////////////////////////////////////////////////////////////////
// Copyright (C) 2001 Chieu Hai Leong and Jason Baldridge
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
//////////////////////////////////////////////////////////////////////////////   
//package bdn;
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


/**
 * Test the model on some input.
 *
 * @author  Jason Baldridge
 * @version $Revision: 1.4 $, $Date: 2008/11/06 20:00:34 $
 */
public class ConceptExtractorServer {
	static ServerSocket socket1;
	//static ServerSocket socket2;
	//static ServerSocket socket3;
	protected final static int port = 19999;
	//protected final static int port2 = 19990;
	//protected final static int port3 = 19980;
	static Socket connection;
	//static Socket connection2;
	//static Socket connection3;
	static boolean first;
	static StringBuffer process;
	//static String TimeStamp;
	
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
	  //System.out.println("best outcme: \n" + _model.getBestOutcome(ocs) + "\n");
	  //System.out.println("all: \n" + _model.getAllOutcomes(ocs) + "\n");
	  BestOutcomes=_model.getBestOutcome(ocs);
	 
	  start1=AllOutcomes.indexOf(BestOutcomes)+BestOutcomes.length()+1;
	  //start1=AllOutcomes.indexOf(BestOutcomes);
	  end1=start1+6;
	  //System.out.println(_model.getBestOutcome(ocs)+" "+AllOutcomes.substring(start1,end1));
	  return (_model.getBestOutcome(ocs)+" "+AllOutcomes.substring(start1,end1)+"\n");
	  //System.out.println(AllOutcomes);
	
    }
    
    private static void usage() {
      
    }

    /**
     * Main method. Call as follows:
     * <p>
     * java Predict dataFile (modelFile)
     */
	 
    public static void main(String[] args) {
	try{
	socket1 = new ServerSocket(port);
	//socket2 = new ServerSocket(port2);
	//socket3 = new ServerSocket(port3);
    int character;
	
	String  modelFileName,modelFileNameClassifier;
    boolean real = false;
    String type = "maxent";
    int ai = 0;
	//outputFileName = "";

	//dataFileName = args[0];
	modelFileName = "identifierModel.txt";
	modelFileNameClassifier = "classifierModel.txt";
	//System.out.println(dataFileName);
	//System.out.println(modelFileName);
	//outputFileName = args[1];
	//System.out.println(outputFileName);
	
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
		//connection2 = socket2.accept();
		
        //BufferedInputStream is = new BufferedInputStream(connection.getInputStream());
        //InputStreamReader isr = new InputStreamReader(is);
        BufferedReader fromClient = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			
		//BufferedReader fromClient2 = new BufferedReader(
       		//new InputStreamReader(connection2.getInputStream()));
			
		
		//s = new StringBuffer();
		String sentence;
		sentence = fromClient.readLine();
        //System.out.println("read from client"+s);
		
		Tree tree = parser.parse(sentence); 
		System.out.println(tree);
			
		System.out.println("Extracting features...");
		String srlIdentifier = "python srl-identifier.py " + '"'+tree+'"' ;
		//System.out.println(srlIdentifier);
		Runtime rr = Runtime.getRuntime();
        Process pp = rr.exec(srlIdentifier);
        BufferedReader brr = new BufferedReader(new InputStreamReader(pp.getInputStream()));
		pp.waitFor();
        System.out.println("Semantic Role Labeling..."); 
		BufferedReader reader = new BufferedReader(new FileReader("identifier.test"));
		BufferedReader classifier = new BufferedReader(new FileReader("classifier.test"));
		
		PrintWriter identifierOutput = new PrintWriter("identifier-output.txt");
		PrintWriter classifierOutput = new PrintWriter("classifier-output.txt");
		BufferedReader preds = new BufferedReader(new FileReader("pred.test"));
				
		String line;
		while ((line = reader.readLine()) != null)
			{
			//System.out.println("inside loop");
			String pred = preds.readLine();
			String identifierFeatures = line + (char) 13; 
			String classifierFeature = classifier.readLine() + (char) 13;
			
			String identOutput = predictorIdentifier.eval(identifierFeatures.substring(0, identifierFeatures.lastIndexOf(' ')),real);
			String classiOutput = predictorClassifier.eval(classifierFeature.substring(0, classifierFeature.lastIndexOf(' ')),real);
			identifierOutput.println(identOutput);
			classifierOutput.println(pred+' '+classiOutput);
			
			}
			identifierOutput.close();
			classifierOutput.close();
			
		System.out.println("Done!");
        String returnCode = "Done!" + (char) 13;
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
    

