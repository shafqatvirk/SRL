import sys
sys.path.append("../shared")
from prepareData import *
from buildModelAuxiliaries import *
#import nltk
import os
#import itertools
from nltk.stem.snowball import SnowballStemmer
#from nltk.corpus import propbank_ptb
def build(tree_head_dict):
#def build():
		stemmer = SnowballStemmer("english")
		input = open('parse-output.txt')
		input_tree_lines = input.readlines()
		tree = ' '.join([l.rstrip().lstrip().rstrip(' ').lstrip(' ')  for l in input_tree_lines])
		(parsed,r) = parseExpr(str(tree),0,0)
		#print parsed.data
		pred_trees =  find_pred_trees(parsed,[])
		#print pred_trees
		identif_output = open('../identifier/maxent/output.txt','r')
		classif_output = open('../classifier/maxent/output.txt','r')
		concepts = []	
		for (pred,pred_terNo) in pred_trees[:]:
			pruned = pruning(parsed,pred,pred_terNo,[])
			#print 
			t_word = str(stemmer.stem(pred.word))
			for c in pruned:
				identifier_line = identif_output.readline()
				identifier = identifier_line.rstrip().split(' ')[0]
				classifier_line = classif_output.readline()
				classifier = classifier_line.rstrip().split(' ')[0]
				if identifier == 'yes':
						#flat_argument = ' '.join([w.rstrip() for w in str(nltk.Tree(''.join(print_tree_srl(c,[]))).flatten()).split(' ')[1:]]).rstrip(')')
						flat_argument = ' '.join([w.rstrip() for w in my_flatten(c,[])])
						concepts.append((t_word,classifier,str(flat_argument)))
		
		#print ''.join(print_tree_srl(parsed,[]))			
		arg_list2 = []
		for (pred_lemma,label,arg_str) in concepts:
						flat_arg_str_list = [arg.replace(' ','_') for arg in arg_str.split(' and ')]
						for flat_arg_str in flat_arg_str_list:
								#flat_arg_str = arg_str.replace(' ','_')
								if label.rstrip() == 'ARG0':
									arg_list2.append(flat_arg_str+'_'+pred_lemma)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-COM':
									arg_list2.append(pred_lemma+'_{with}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-LOC':
									arg_list2.append(pred_lemma+'_{in}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-DIR':
									arg_list2.append(pred_lemma+'_{in_the_direction}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-PRP':
									arg_list2.append(pred_lemma+'_{in_order_to}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-CAU':
									arg_list2.append(pred_lemma+'_{because}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-NEG':
									arg_list2.append(pred_lemma+'_{not}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-GOL':
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-MNR':
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-TMP':
									arg_list2.append(pred_lemma+'_{when}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								elif label.rstrip() == 'ARGM-EXT':
									arg_list2.append(pred_lemma+'_{by}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
								else:
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
		for concept in list(set(arg_list2)):
			print concept
def my_flatten(node,flat_list):
	if node.data != None and node.data not in ['IN','TO'] and node.word != None and node.word != []:
		flat_list.append(node.word)
	for ch in node.children:
		my_flatten(ch,flat_list)
	return flat_list
if __name__ == "__main__":
 import sys
 try:
	tree_head_dict = build_tree_head_dict()
	build(tree_head_dict)
 except:
	print >>sys.stderr, __doc__
	raise