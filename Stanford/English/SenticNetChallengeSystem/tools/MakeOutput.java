import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.*;
import java.io.File;
import java.io.FileReader;
import java.util.*;
import java.io.File;
import java.io.*;


public class MakeOutput {

public static void main(String[] args) throws IOException {
	try{
	//List<String> outputLines = Files.readLines("../output/output.txt");// Get the object of DataInputStream
			String outputFileName = "../output/output.txt";
			List<String> outputLines = Files.readAllLines(Paths.get(outputFileName),
                    Charset.defaultCharset());
			File dir = new File("../input");
			File[] directoryListing = dir.listFiles();
			if (directoryListing != null) {
			int from = 0;
			int to = 0;
			int file_index = 0;
			for (File child : directoryListing) {
			// Do something with child
			PrintWriter output = new PrintWriter("../output/output"+file_index+".txt");
			String inputFileName = child.getPath();
			List<String> inputLines = Files.readAllLines(Paths.get(inputFileName),
                    Charset.defaultCharset());
			output.println("<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">");
			output.println("<rdf:Description rdf:about=\"http://sentic.net/challenge/sentence\">");
			output.println("<sentence xmlns=\"http://sentic.net/challenge/\" rdf:resource=\"http://sentic.net/challenge/sentence\">");
			output.println("<text xmlns=\"http://sentic.net/challenge/\" rdf:datatype=\"http://www.w3.org/TR/rdf-text/\">");
			to = to + inputLines.size();
			List<String> sub = (List<String>) outputLines.subList(from, to);
			//System.out.println(sub);
			for (String l : sub)
			{
			//System.out.println(l);
			String[] concepts = l.split("::");
			//System.out.println(StringUtils.join(Arrays.toString(concepts), ""));
			for (String con : concepts ){
				output.println("<semantics xmlns=\"http://sentic.net/challenge/\" rdf:resource=\"http://sentic.net/api/en/concept/"+con+"\"/>");
				//System.out.println(con);
				}
			output.println("</sentence>");
			output.println("</rdf:Description>");
			output.println("</rdf:RDF>");
			output.close();
			}
			from = to;
			file_index += 1;	
			}		
			}
			else {
				// Handle the case where dir is not really a directory.
				// Checking dir.isDirectory() above would not be sufficient
				// to avoid race conditions with another process that deletes
				// directories.
			}

		}
		catch (Exception e){//Catch exception if any

                System.err.println("Error: " + e.getMessage());
                //return "";
            }

	}
}