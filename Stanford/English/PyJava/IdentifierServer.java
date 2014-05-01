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
public class IdentifierServer {
	static ServerSocket socket1;
	protected final static int port = 19999;
	static Socket connection;

	static boolean first;
	static StringBuffer process;
	static String TimeStamp;
	
    MaxentModel _model;
    ContextGenerator _cg = new BasicContextGenerator();
    
    public IdentifierServer (MaxentModel m) {
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
    System.out.println("SingleSocketServer Initialized");
    int character;
	
	String  modelFileName;
    boolean real = false;
    String type = "maxent";
    int ai = 0;
	//outputFileName = "";

	//dataFileName = args[0];
	modelFileName = "IdentifierModel.txt";
	//System.out.println(dataFileName);
	//System.out.println(modelFileName);
	//outputFileName = args[1];
	//System.out.println(outputFileName);
	
	
	IdentifierServer predictor = null;
	try {
      MaxentModel m = new GenericModelReader(new File(modelFileName)).getModel();
	  predictor = new IdentifierServer(m);
	} catch (Exception e) {
	    e.printStackTrace();
	    System.exit(0);
	}
	
	
	while (true) {
        connection = socket1.accept();

        //BufferedInputStream is = new BufferedInputStream(connection.getInputStream());
        //InputStreamReader isr = new InputStreamReader(is);
        BufferedReader fromClient = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
		//s = new StringBuffer();
		String s;
		s = fromClient.readLine();
        System.out.println("read from client"+s);
		String output = predictor.eval(s.substring(0, s.lastIndexOf(' ')),real);
        System.out.println(output);
        //need to wait 10 seconds for the app to update database
        //try {
          //Thread.sleep(10000);
        //}
        //catch (Exception e){}
        TimeStamp = new java.util.Date().toString();
        String returnCode = "SingleSocketServer repsonded at "+ TimeStamp + (char) 13;
        BufferedOutputStream os = new BufferedOutputStream(connection.getOutputStream());
        OutputStreamWriter osw = new OutputStreamWriter(os, "US-ASCII");
        osw.write(returnCode);
        osw.flush();
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
    

