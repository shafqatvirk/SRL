//import semanticrolelabeling.*;
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

public class ConceptExtractorBatchClient
{
    
    
	public static void main(String[] args)
    {
    /** Define a host server */
    String host = "localhost";
    /** Define a port */
    int port = 19999;
    System.out.println("SocketClient initialized");
	
		try
        {	
			
			File dir = new File("../input");
			File[] directoryListing = dir.listFiles();
			if (directoryListing != null) {
			for (File child : directoryListing) {
			// Do something with child
			
			BufferedReader inputReader = new BufferedReader(new FileReader(child));
			String sent;
			while ((sent = inputReader.readLine()) != null)
			{
			System.out.println("Sentence: "+sent);
			System.out.println("Parsing....");
			String sentence = sent + (char) 13;
			
			InetAddress address = InetAddress.getByName(host);
			// Establish a socket connetion 
			Socket connection = new Socket(address, port);
			BufferedOutputStream bos = new BufferedOutputStream(connection.
			getOutputStream());
			OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
			osw.write(sentence);
			osw.flush();
			System.out.println("Concept Extraction....");
			BufferedReader fromServer = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			String serverResponse = fromServer.readLine();
			System.out.println(serverResponse);
			
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
			
			}
		} else {
				// Handle the case where dir is not really a directory.
				// Checking dir.isDirectory() above would not be sufficient
				// to avoid race conditions with another process that deletes
				// directories.
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