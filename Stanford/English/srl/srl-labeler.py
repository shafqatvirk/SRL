import sys
sys.path.append("../shared")
from prepareData import *
from buildModelAuxiliaries import *
import nltk
import os
import itertools
#from nltk.corpus import propbank_ptb
def build(tree_head_dict):
#def build():
		input = open('input.txt')
		input_tree_lines = input.readlines()
		tree = ' '.join([l.rstrip().lstrip().rstrip(' ').lstrip(' ')  for l in input_tree_lines])
		#print tree
		#if str(inst).find('*') == -1 and str(inst).find(',') == -1:
		#arguments = []
		#tree = inst.tree
		#tree.draw()
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
			t_word = pred.word
			#t_w_pos = pred.data
			#pred_parrent = find_pred_parrent(parsed,pred_terNo,None)
			#subcat = find_subcat(pred_parrent)
			for c in pruned:
				identifier_line = identif_output.readline()
				identifier = identifier_line.rstrip().split(' ')[0]
				classifier_line = classif_output.readline()
				classifier = classifier_line.rstrip().split(' ')[0]
				if identifier == 'yes':
						flat_argument = ' '.join([w.rstrip() for w in str(nltk.Tree(''.join(print_tree_srl(c,[]))).flatten()).split(' ')[1:]]).rstrip(')')
						concepts.append((t_word,classifier,str(flat_argument)))
		
		#print ''.join(print_tree_srl(parsed,[]))			
		for conc in concepts:
			print conc
					
if __name__ == "__main__":
 import sys
 try:
	tree_head_dict = build_tree_head_dict()
	#(roles_7_dict,total_7_dict,roles_6a_dict,total_6a_dict,roles_6b_dict,total_6b_dict,roles_6c_dict,total_6c_dict,roles_6d_dict,total_6d_dict,roles_5a_dict,total_5a_dict,roles_5b_dict,total_5b_dict,roles_5c_dict,total_5c_dict,roles_5d_dict,total_5d_dict,roles_3a_dict,total_3a_dict,roles_2a_dict,total_2a_dict,roles_1a_dict,total_1a_dict,roles_baseline_dict,total_baseline_dict) = build()
	build(tree_head_dict)
	#build()
	#output_model(roles_7_dict,total_7_dict,roles_6a_dict,total_6a_dict,roles_6b_dict,total_6b_dict,roles_6c_dict,total_6c_dict,roles_6d_dict,total_6d_dict,roles_5a_dict,total_5a_dict,roles_5b_dict,total_5b_dict,roles_5c_dict,total_5c_dict,roles_5d_dict,total_5d_dict,roles_3a_dict,total_3a_dict,roles_2a_dict,total_2a_dict,roles_1a_dict,total_1a_dict,roles_baseline_dict,total_baseline_dict)
 except:
	print >>sys.stderr, __doc__
	raise