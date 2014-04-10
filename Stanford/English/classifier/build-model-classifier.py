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
			#all_sub_trees = all_sub_trees + print_all_subtrees(parsed,[]) # use this function to print all subtrees and then use java program to find heads 
			for (argloc,argid) in inst.arguments:
				if str(argloc.select(tree)).split(')')[0].find('*') == -1:
					#print('%s' % (argloc.select(tree).pprint(10000)[:]))
					wordNum = int(str(argloc).split(':')[0])
					h = int(str(argloc).split(':')[1])
					#print wordNum
					#print h
					arg = traverse_tree_depth(parsed,wordNum,h)
					arguments.append((arg,argid))
			#for a in arguments:
				#print a.data
			#pruned = pruning(parsed,pred,inst.predicate.wordnum,[])
			#print 
			t_word = inst.roleset.split('.')[0]
			t_w_pos = inst.predicate.select(inst.tree).node
			pred_parrent = find_pred_parrent(parsed,inst.predicate.wordnum,None)
			subcat = find_subcat(pred_parrent)
			#print t_word
			#print t_w_pos
			for (arg,label) in arguments:
				path_list = get_path(arg,parsed,inst.predicate.wordnum)
				(h,h_pos) = extract_head(arg,tree_head_dict)
				path = ''.join(path_list)
				distance = len(path_list)
				pt = arg.data.rstrip()
				t_word_pls_pt = str(t_word)+str(pt)
				t_word_pls_h_word = str(t_word)+str(h)
				distance_pls_t_word = str(distance)+str(t_word)
				subcatStar = find_subcat(arg.parent)
				subcatAt = find_subcat(arg)
				
				
				print 'h='+str(h)+' h_pos='+str(h_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+ ' '+label
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+ ' ?'
				
			#tree.draw()
			#print ''.join(print_tree_file(parsed,[]))
			#print ''.join(print_tree_file(pred,[]))
			'''complex_NP_concept_trees = extract_complex_NP_concept(parsed,[])
			complex_NP_concept_trees_flats = [nltk.Tree(''.join(print_tree_file(t,[]))).flatten() for t in complex_NP_concept_trees]
			for complex in complex_NP_concept_trees_flats:
				complex_NP_str = ' '.join(str(complex).split(' ')[1:]).split(')')[0]
				complex_NP.append(' '.join([c.rstrip() for c in complex_NP_str.split(' ')]))
			(predicate) = traverse_tree_depth(parsed,predicate_no,0)
			#target = ids[4].split('.')[0]
			#target_POS = predicate.data
			if predicate != None:
				arg_list = []
				arg_list2 = []
			##print 'Sentences:\t' + raw_line
			sentences.append(raw_line)
			for arg in args:
				label = '-'.join(arg.split('-')[1:])
				if label.rstrip() != 'rel':
					#if label.rstrip() in ['ARG0','ARG1','ARG2','ARG3','ARG4']:
					nh_pairs = arg.split('-')[0]
					if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
							arg_str = find_features_without_traces(nh_pairs,parsed,predicate)
							#print arg_str
							if arg_str != 0:
								flat_arg = nltk.Tree(arg_str).flatten()
								arg_list.append(' '.join(str(flat_arg).split(' ')[1:]).split(')')[0])
								#print pred_str.rstrip() + '\t' + str(flat_arg)
								#print flat_arg
							if arg_str != 0:
								flat_arg = nltk.Tree(arg_str).flatten()
								flat_arg_str = ' '.join(str(flat_arg).split(' ')[1:]).split(')')[0]
								flat_arg_str = ' '.join([el.rstrip() for el in flat_arg_str.split(' ')])
								if label.rstrip() == 'ARG0':
									arg_list2.append(flat_arg_str+'_'+pred_lemma)
								elif label.rstrip() == 'ARGM-COM':
									arg_list2.append(pred_lemma+'_{with}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-LOC':
									arg_list2.append(pred_lemma+'_{in}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-DIR':
									arg_list2.append(pred_lemma+'_{in_the_direction}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-PRP':
									arg_list2.append(pred_lemma+'_{in_order_to}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-CAU':
									arg_list2.append(pred_lemma+'_{because}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-NEG':
									arg_list2.append(pred_lemma+'_{not}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-GOL':
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-MNR':
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-TMP':
									arg_list2.append(pred_lemma+'_{when}_'+flat_arg_str)
								elif label.rstrip() == 'ARGM-EXT':
									arg_list2.append(pred_lemma+'_{by}_'+flat_arg_str)
								else:
									arg_list2.append(pred_lemma+'_'+flat_arg_str)'''
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