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
//import semanticrolelabeling.*;
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
public class ClassifierServer {
	static ServerSocket socket1;
	static ServerSocket socket2;
	//static ServerSocket socket3;
	protected final static int port = 19999;
	protected final static int port2 = 19990;
	//protected final static int port3 = 19980;
	static Socket connection;
	static Socket connection2;
	//static Socket connection3;
	static boolean first;
	static StringBuffer process;
	static String TimeStamp;
	
    MaxentModel _model;
    ContextGenerator _cg = new BasicContextGenerator();
    
    public ClassifierServer (MaxentModel m) {
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
	socket2 = new ServerSocket(port2);
	//socket3 = new ServerSocket(port3);
    System.out.println("SingleSocketServer Initialized");
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
	
	//Parser parser = new Parser();
	
	ClassifierServer predictorIdentifier = null;
	ClassifierServer predictorClassifier = null;
	try {
      MaxentModel m = new GenericModelReader(new File(modelFileName)).getModel();
	  MaxentModel m2 = new GenericModelReader(new File(modelFileNameClassifier)).getModel();
	  predictorIdentifier = new ClassifierServer(m);
	  predictorClassifier = new ClassifierServer(m2);
	} catch (Exception e) {
	    e.printStackTrace();
	    System.exit(0);
	}
		
	
	while (true) {
	
		
		/*
		connection3 = socket3.accept();
        
		
		BufferedReader fromClient3 = new BufferedReader(
       		new InputStreamReader(connection3.getInputStream()));
		String s3;
		s3 = fromClient3.readLine();
        System.out.println("read from client3"+s3);
		//String output3 = predictorClassifier.eval(s2.substring(0, s.lastIndexOf(' ')),real);
		Tree tree = parser.parse(s3);       
		System.out.println(tree);
        PrintWriter writer = new PrintWriter("parser-output.txt", "UTF-8");
		//writer.println("its written");
		writer.println(tree);
		writer.close();
		System.out.println("parsing done");
        String returnCode3 = "Done!" + (char) 13;
        BufferedOutputStream os3 = new BufferedOutputStream(connection3.getOutputStream());
        OutputStreamWriter osw3 = new OutputStreamWriter(os3, "US-ASCII");
        osw3.write(returnCode3);
        osw3.flush();
		*/
		connection = socket1.accept();
		connection2 = socket2.accept();
		
        //BufferedInputStream is = new BufferedInputStream(connection.getInputStream());
        //InputStreamReader isr = new InputStreamReader(is);
        BufferedReader fromClient = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			
		BufferedReader fromClient2 = new BufferedReader(
       		new InputStreamReader(connection2.getInputStream()));
			
		
		//s = new StringBuffer();
		String s;
		s = fromClient.readLine();
        //System.out.println("read from client"+s);
		String output = predictorIdentifier.eval(s.substring(0, s.lastIndexOf(' ')),real);
        //System.out.println(output);
        //need to wait 10 seconds for the app to update database
        //try {
          //Thread.sleep(10000);
        //}
        //catch (Exception e){}
        //TimeStamp = new java.util.Date().toString();
        String returnCode = output + (char) 13;
        BufferedOutputStream os = new BufferedOutputStream(connection.getOutputStream());
        OutputStreamWriter osw = new OutputStreamWriter(os, "US-ASCII");
        osw.write(returnCode);
        osw.flush();
		
		
		String s2;
		s2 = fromClient2.readLine();
        //System.out.println("read from client2"+s2);
		String output2 = predictorClassifier.eval(s2.substring(0, s2.lastIndexOf(' ')),real);
        //System.out.println(output2);
       
        String returnCode2 = output2 +  (char) 13;
        BufferedOutputStream os2 = new BufferedOutputStream(connection2.getOutputStream());
        OutputStreamWriter osw2 = new OutputStreamWriter(os2, "US-ASCII");
        osw2.write(returnCode2);
        osw2.flush();
		
		
		
		
     } 
    }
	catch (IOException e) {}
	}
	/*
	    try {
		DataStream ds =
		    new PlainTextByLineDataStream(
			new FileReader(new File(dataFileName)));
		File statText = new File(outputFileName);
        FileOutputStream is = new FileOutputStream(statText);
        OutputStreamWriter osw = new OutputStreamWriter(is);    
        Writer w = new BufferedWriter(osw);
		while (ds.hasNext()) {
		    String s = (String)ds.nextToken();
		    String output = predictor.eval(s.substring(0, s.lastIndexOf(' ')),real);
			//System.out.println(output);
			w.write(output);
		}
		w.close();
		return;
	    }
	    catch (Exception e) {
	      System.out.println("Unable to read from specified file: "+modelFileName);
	      System.out.println();
	      e.printStackTrace();
	    }
		*/
	
    }
    

