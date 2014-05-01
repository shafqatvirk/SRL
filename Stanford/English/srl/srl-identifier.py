import sys
sys.path.append("../shared")
from prepareData import *
from buildModelAuxiliaries import *
#import nltk
import os
import itertools
#from nltk.stem.snowball import SnowballStemmer
#from nltk.corpus import propbank_ptb
def build(tree_head_dict):
#def build():
		#stemmer = SnowballStemmer("english")
		input = open('parse-output.txt')
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
		identif_file = open('../identifier/maxent/train.test','w')
		classif_file = open('../classifier/maxent/train.test','w')
		preds_file = open('preds.txt','w')
			
		for (pred,pred_terNo) in pred_trees[:]:
			pruned = pruning(parsed,pred,pred_terNo,[])
			#print 
			t_word = pred.word
			#t_word = str(stemmer.stem(pred.word))
			t_w_pos = pred.data
			pred_parrent = find_pred_parrent(parsed,pred_terNo,None)
			subcat = find_subcat(pred_parrent)
			#print t_word
			#identif_file = open(t_word+str(pred_trees.index((pred,pred_terNo)))+'-ident.txt','w')
			#classif_file = open(t_word+str(pred_trees.index((pred,pred_terNo)))+'-classif.txt','w')
			#print t_w_pos
			for c in pruned:
				path_list = get_path(c,parsed,pred_terNo)
				(h,h_pos) = extract_head(c,tree_head_dict)
				path = ''.join(path_list)
				distance = len(path_list)
				pt = c.data.rstrip()
				t_word_pls_pt = str(t_word)+str(pt)
				t_word_pls_h_word = str(t_word)+str(h)
				distance_pls_t_word = str(distance)+str(t_word)
			
				subcatStar = find_subcat(c.parent)
				subcatAt = find_subcat(c)
				flat_argument = '_'.join([w.rstrip() for w in my_flatten(c,[])])
				# features for identification
				identif_file.write('h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' ?\n')
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' ?'
				# features for classification
				classif_file.write('h='+str(h)+' h_pos='+str(h_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+ ' ?\n')
				preds_file.write(t_word+' '+flat_argument+'\n')
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
	#(roles_7_dict,total_7_dict,roles_6a_dict,total_6a_dict,roles_6b_dict,total_6b_dict,roles_6c_dict,total_6c_dict,roles_6d_dict,total_6d_dict,roles_5a_dict,total_5a_dict,roles_5b_dict,total_5b_dict,roles_5c_dict,total_5c_dict,roles_5d_dict,total_5d_dict,roles_3a_dict,total_3a_dict,roles_2a_dict,total_2a_dict,roles_1a_dict,total_1a_dict,roles_baseline_dict,total_baseline_dict) = build()
	build(tree_head_dict)
	#build()
	#output_model(roles_7_dict,total_7_dict,roles_6a_dict,total_6a_dict,roles_6b_dict,total_6b_dict,roles_6c_dict,total_6c_dict,roles_6d_dict,total_6d_dict,roles_5a_dict,total_5a_dict,roles_5b_dict,total_5b_dict,roles_5c_dict,total_5c_dict,roles_5d_dict,total_5d_dict,roles_3a_dict,total_3a_dict,roles_2a_dict,total_2a_dict,roles_1a_dict,total_1a_dict,roles_baseline_dict,total_baseline_dict)
 except:
	print >>sys.stderr, __doc__
	raise