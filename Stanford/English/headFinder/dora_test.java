import java.io.*;
import java.util.*;
import java.util.Properties;

import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.trees.CollinsHeadFinder;
//import edu.stanford.nlp.trees.international.pennchinese.ChineseHeadFinder;


public class dora_test
{
	public static void main(String args[])
	{
		
		//test Class CollinsHeadFinder
		CollinsHeadFinder test_for_head=new CollinsHeadFinder();
		CollinsHeadFinder test_for_head2=new CollinsHeadFinder(new PennTreebankLanguagePack());
		String[] path_tree={"argument-trees2.txt"};
		//String[] path_tree={"argument-tree.txt"};
		//String[] path_tree={"test.txt"};
		//String[] path_tree={"( (S (NP-SBJ (NP (NNP Pierre) (NNP Vinken) )(, ,) (ADJP (NP (CD 61) (NNS years) )(JJ old) )(, ,) ) (VP (MD will) (VP (VB join) (NP (DT the) (NN board) )(PP-CLR (IN as) (NP (DT a) (JJ nonexecutive) (NN director) ))(NP-TMP (NNP Nov.) (CD 29) )))(. .) ))"};
		
		//test_for_head2.main(path_tree);
		Treebank treebank = new DiskTreebank();
		CategoryWordTag.suppressTerminalDetails = true;
		//treebank.loadPath("argument-tree.txt");
		treebank.loadPath("argument-trees2.txt");
		//treebank.loadPath("test.txt");
		final HeadFinder chf = new CollinsHeadFinder();
		treebank.apply(new TreeVisitor() {
			public void visitTree(Tree pt) {
				pt.percolateHeads(chf);
				//pt.pennPrint();
			pt.headTerminal(chf).toString();
			System.out.println(pt.headPreTerminal(chf).toString());
			//System.out.println("headTerminal : "+pt.headTerminal(chf).toString()+"\n");
		
			}
		});
		
	}
}