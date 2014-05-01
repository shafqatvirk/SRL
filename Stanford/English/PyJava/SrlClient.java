import semanticrolelabeling.*;
import java.io.*;
import edu.stanford.nlp.trees.Tree;
import java.util.*;
import java.io.File;
import java.io.FileReader;
import opennlp.maxent.DataStream;
import opennlp.maxent.PlainTextByLineDataStream;

//package bdn;
/*  The java.net package contains the basics needed for network operations. */
import java.net.*;
/* The java.io package contains the basics needed for IO operations. */
import java.io.*;
/** The SocketClient class is a simple example of a TCP/IP Socket Client.
 *
 */

public class SrlClient
{
    
    
	public static void main(String[] args)
    {
    /** Define a host server */
    String host = "localhost";
    /** Define a port */
    int port = 19999;
	int port2 = 19990;
	//int port3 = 19980;
    StringBuffer instr = new StringBuffer();
    String TimeStamp;
	Parser parser = new Parser();
    System.out.println("SocketClient initialized");
	
		try
        {	
			
			// parsing
			DataStream ds =
		    new PlainTextByLineDataStream(
			new FileReader(new File("input.txt")));
			String sentence = (String)ds.nextToken() + (char) 13;
			//System.out.println(str);
			System.out.println("Parsing....");
			
			Tree tree = parser.parse(sentence); 
			System.out.println(tree);
			
			System.out.println("Extracting features...");
			String srlIdentifier = "python srl-identifier.py " + '"'+tree+'"' ;
			//System.out.println(srlIdentifier);
			Runtime rr = Runtime.getRuntime();
            Process pp = rr.exec(srlIdentifier);
            BufferedReader brr = new BufferedReader(new InputStreamReader(pp.getInputStream()));
            pp.waitFor();
           
			
			BufferedReader reader = new BufferedReader(new FileReader("identifier.test"));
			BufferedReader classifier = new BufferedReader(new FileReader("classifier.test"));
			String line;
			PrintWriter identifierOutput = new PrintWriter("identifier-output.txt");
			PrintWriter classifierOutput = new PrintWriter("classifier-output.txt");
			BufferedReader preds = new BufferedReader(new FileReader("pred.test"));
			
			while ((line = reader.readLine()) != null)
			{
			//System.out.println("inside loop");
			String pred = preds.readLine();
			String features = line + (char) 13; 
			String classifierFeature = classifier.readLine() + (char) 13;
			//System.out.println("classifier features"+classifierFeature);
			
			InetAddress address = InetAddress.getByName(host);
			// Establish a socket connetion 
			Socket connection = new Socket(address, port);
			Socket connection2 = new Socket(address, port2);
			
			// Instantiate a BufferedOutputStream object 
			BufferedOutputStream bos = new BufferedOutputStream(connection.
			getOutputStream());

			// Instantiate an OutputStreamWriter object with the optional character
			// encoding.
			//
			
			OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
			
			BufferedReader fromServer = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			
			
			// Write across the socket connection and flush the buffer 
			
			osw.write(features);
			osw.flush();
			String identifierResponse = fromServer.readLine();
			identifierOutput.println(identifierResponse);
			//System.out.println(identifierResponse);
			
			
			BufferedOutputStream bos2 = new BufferedOutputStream(connection2.
			getOutputStream());

			// Instantiate an OutputStreamWriter object with the optional character
			// encoding.
			//
			OutputStreamWriter osw2 = new OutputStreamWriter(bos2, "US-ASCII");
			
			BufferedReader fromServer2 = new BufferedReader(
       		new InputStreamReader(connection2.getInputStream()));
			
			osw2.write(classifierFeature);
			osw2.flush();
			String ClassifierResponse = fromServer2.readLine();
			classifierOutput.println(pred+' '+ClassifierResponse);
			//System.out.println(ClassifierResponse);
			//}
			}
			identifierOutput.close();
			classifierOutput.close();
			
			Runtime rlabeler = Runtime.getRuntime();
            String srlClassifier = "python concept-formulator.py" ;
			Process p = rlabeler.exec(srlClassifier);
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            p.waitFor();
            //System.out.println("here i am");
			String line2;
			while((line2 = br.readLine()) != null) {
				System.out.println(line2);
			//while (br.ready())
               // System.out.println(br.readLine());
			  }
			
        }
        catch (Exception e)
        {
		String cause = e.getMessage();
		if (cause.equals("python: not found"))
			System.out.println("No python interpreter found.");
        }
    }
}