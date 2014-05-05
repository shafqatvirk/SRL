import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.*;
//import edu.stanford.nlp.trees.Tree;
import java.util.*;
import java.io.File;
import java.io.FileReader;
import opennlp.tools.sentdetect.SentenceDetector;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.util.Span;
//import opennlp.maxent.DataStream;

public class MakeData {

public static void main(String[] args) throws IOException{

SentenceDetector sd = null;
if (sd == null) {
      sd = new SentenceDetectorME(new SentenceModel(new FileInputStream(new File("../models/en-sent.bin"))));
    }


String toMatch=readFile();
//System.out.println(toMatch);
//Pattern pattern=Pattern.compile(".*?<text.*?>(.*?)</text>.*?",Pattern.DOTALL);
Pattern pattern=Pattern.compile(".*?<review_text>(.*?)</review_text>.*?",Pattern.DOTALL);
//Pattern pattern=Pattern.compile(".*?<table class=\"claroTable\".*?>(.*?)</table>.*?"); //I want this one to work
Matcher matcher=pattern.matcher(toMatch);

/*
if(matcher.matches()) {
	String sentences[] = sd.sentDetect(matcher.group(1));
	PrintWriter output = new PrintWriter("input.sent");
	for (String sent : sentences) {
		output.println(sent);
            System.out.println(sent);
        }
	output.close();
	//System.out.println(sentences[0]);
    //System.out.println(matcher.group(1));
}
*/
 final List<String> reviews = new ArrayList<String>();
 while (matcher.find()) {
        reviews.add(matcher.group(1));
    }
 //System.out.println(tagValues);
 for (String review : reviews ) {
		
		PrintWriter output = new PrintWriter("../input/input"+reviews.indexOf(review)+".sent");
        String sentences[] = sd.sentDetect(review);
		for (String sent : sentences) {
		output.println(sent);
        //System.out.println(sent);
        }
		output.close();
        }

}

 private static String readFile() {

      try{
            // Open the file that is the first 
            // command line parameter
            //FileInputStream fstream = new FileInputStream("data.txt");
			FileInputStream fstream = new FileInputStream("../data/short.review");
            // Get the object of DataInputStream
            DataInputStream in = new DataInputStream(fstream);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String strLine = null;
            //Read File Line By Line
			String line;
            while ((line = br.readLine()) != null)   {
                // Print the content on the console
                //System.out.println (strLine);
                strLine+=line;
            }
            //Close the input stream
            in.close();
            return strLine;
            }catch (Exception e){//Catch exception if any

                System.err.println("Error: " + e.getMessage());
                return "";
            }
}
}