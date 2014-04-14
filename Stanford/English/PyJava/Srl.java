import semanticrolelabeling.*;
import java.io.*;
import edu.stanford.nlp.trees.Tree;

import java.io.File;
import java.io.FileReader;
import opennlp.maxent.DataStream;
import opennlp.maxent.PlainTextByLineDataStream;

public class Srl
{
    
    
	public static void main(String[] args)
    {
        try
        {
            
			DataStream ds =
		    new PlainTextByLineDataStream(
			new FileReader(new File("input.txt")));
			String str = (String)ds.nextToken();
			System.out.println(str);
			//String str = "My dog also likes eating sausage.";
			Parser parser = new Parser();
			Tree tree = parser.parse(str); 
			//System.out.println(tree);
			//PrintWriter writer = new PrintWriter("parser-output.txt", "UTF-8");
			//writer.println(tree);
			//writer.close();
			//Predict predictor = new Predict();
			String srlIdentifier = "python srl-identifier.py " + '"'+tree+'"' ;
			//System.out.println(srlIdentifier);
			Runtime rr = Runtime.getRuntime();
            Process pp = rr.exec(srlIdentifier);
            BufferedReader brr = new BufferedReader(new InputStreamReader(pp.getInputStream()));
            //pp.waitFor();
            //String line2 = "";
            //while (brr.ready())
              //  System.out.println(brr.readLine());
			
			String[] identifier_arguments = new String[] {"identifier.test","identifier-output.txt"};
			String[] classifier_arguments = new String[] {"classifier.test","classifier-output.txt"};
			Predict.main(identifier_arguments);
			Predict.main(classifier_arguments);
			
			
			Runtime r = Runtime.getRuntime();
            String srlClassifier = "python srl-labeler.py " + '"'+tree+'"' ;
			Process p = r.exec(srlClassifier);
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            p.waitFor();
            String line = "";
            while (br.ready())
                System.out.println(br.readLine());

        }
        catch (Exception e)
        {
		String cause = e.getMessage();
		if (cause.equals("python: not found"))
			System.out.println("No python interpreter found.");
        }
    }
}