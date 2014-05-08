//import semanticrolelabeling.*;
import java.io.*;
//import edu.stanford.nlp.trees.Tree;
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

public class SRLClient
{
    
    
	public static void main(String[] args)
    {
    /** Define a host server */
    String host = "localhost";
    /** Define a port */
    int port = 29999;
    System.out.println("SocketClient initialized");
	
		try
        {	
			
			// parsing
			//DataStream ds =
		    //new PlainTextByLineDataStream(
			//new FileReader(new File("input.txt")));
			//String sentence = (String)ds.nextToken() + (char) 13;
			//System.out.println(sentence);
			//System.out.println("Parsing....");
			
			InetAddress address = InetAddress.getByName(host);
			// Establish a socket connetion 
			Socket connection = new Socket(address, port);
			BufferedOutputStream bos = new BufferedOutputStream(connection.
			getOutputStream());
			OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
			osw.write("Sent: to java server"+ (char) 13);
			osw.flush();
			System.out.println("SRL....");
			BufferedReader fromServer = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			String serverResponse = fromServer.readLine();
			System.out.println(serverResponse);
			System.out.println("Hybridization");
			Runtime rlabeler = Runtime.getRuntime();
            String srlClassifier = "python hybridization.py" ;
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