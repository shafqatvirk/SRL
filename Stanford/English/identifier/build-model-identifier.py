import sys
sys.path.append("../shared")
from prepareData import *
from buildModelAuxiliaries import *
import nltk
import os
import itertools
from nltk.corpus import propbank_ptb
def build(tree_head_dict):
#def build():
	pb_instances = propbank_ptb.instances()
	all_sub_trees = []
	for inst in pb_instances[:]:
		if str(inst).find('*') == -1 and str(inst).find(',') == -1:
			arguments = []
			tree = inst.tree
			#tree.draw()
			pred_tree =  inst.predicate.select(tree)
			(pred,r) = parseExpr(str(pred_tree),0,0)
			(parsed,r) = parseExpr(str(tree),0,0)
			remove_functional_tags(parsed)
			#print ''.join(print_tree_file(parsed,[]))
			#all_sub_trees = all_sub_trees + print_all_subtrees(parsed,[]) # use this function to print all subtrees and then use java program to find heads 
			for (argloc,argid) in inst.arguments:
				if str(argloc.select(tree)).split(')')[0].find('*') == -1:
					#print('%s' % (argloc.select(tree).pprint(10000)[:]))
					wordNum = int(str(argloc).split(':')[0])
					h = int(str(argloc).split(':')[1])
					#print wordNum
					#print h
					arg = traverse_tree_depth(parsed,wordNum,h)
					arguments.append(arg)
			#for a in arguments:
				#print a.data
			pruned = pruning(parsed,pred,inst.predicate.wordnum,[])
			#print 
			t_word = pred.word
			t_w_pos = pred.data
			#t_word = inst.roleset.split('.')[0]
			#t_w_pos = inst.predicate.select(inst.tree).node
			#print t_word
			#print t_w_pos
			for c in pruned:
				path_list = get_path(c,parsed,inst.predicate.wordnum)
				(h,h_pos) = extract_head(c,tree_head_dict)
				path = ''.join(path_list)
				distance = len(path_list)
				pt = c.data.rstrip()
				t_word_pls_pt = str(t_word)+str(pt)
				t_word_pls_h_word = str(t_word)+str(h)
				distance_pls_t_word = str(distance)+str(t_word)
				if c in arguments:
					label = 'yes'
				else:
					label = 'no'
				print 'h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' '+label
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' ?'
				
			#tree.draw()
			#print ''.join(print_tree_file(parsed,[]))
			#print ''.join(print_tree_file(pred,[]))
			
	# to print subtrees for head finding
	#for one in list(set(all_sub_trees)):
	#	print one
	 
					
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