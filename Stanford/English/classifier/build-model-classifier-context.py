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
	##predicted_context_labels = read_without_context_labels() ##
	##f = 0 ##
	##t = 0 ##
	for inst in pb_instances[:]:
	 if int(str(inst).split('/')[1]) > 01 and int(str(inst).split('/')[1]) < 22:	# for getting training data according to CoNLL 2005 task
	 #if int(str(inst).split('/')[1]) == 23:	# for getting testing data according to CoNLL 2005 task
		if str(inst).find('*') == -1 and str(inst).find(',') == -1:
			arguments = []
			tree = inst.tree
			#tree.draw()
			pred_tree =  inst.predicate.select(tree)
			(pred,r) = parseExpr(str(pred_tree),0,0)
			(parsed,r) = parseExpr(str(tree),0,0)
			#remove_functional_tags(parsed)
			#all_sub_trees = all_sub_trees + print_all_subtrees(parsed,[]) # use this function to print all subtrees and then use java program to find heads 
			gold_context_labels_list = []
			for (argloc,argid) in inst.arguments:
				if str(argloc.select(tree)).split(')')[0].find('*') == -1:
					#print('%s' % (argloc.select(tree).pprint(10000)[:]))
					wordNum = int(str(argloc).split(':')[0])
					h = int(str(argloc).split(':')[1])
					#print wordNum
					#print h
					arg = traverse_tree_depth(parsed,wordNum,h)
					arguments.append((arg,wordNum,argid))
					gold_context_labels_list.append(argid)
			#for a in arguments:
				#print a.data
			#pruned = pruning(parsed,pred,inst.predicate.wordnum,[])
			#print 
			t_word = pred.word
			t_w_pos = pred.data
			#t_word = inst.roleset.split('.')[0]
			#t_w_pos = inst.predicate.select(inst.tree).node
			pred_parrent = find_pred_parrent(parsed,inst.predicate.wordnum,None)
			subcat = find_subcat(pred_parrent)
			if pred_parrent.word != None:
				ParentWord = pred_parrent.word # word of the parrent node of pred
			else:
				ParentWord = 'none'
			ParentWordPos = pred_parrent.data.rstrip() # pos of the parrent node of pred
			## gold context labels
			context_labels_all = gold_context_labels_list # for training
			#predicted
			##t = t + len(arguments) ##
			##context_labels_all = predicted_context_labels[f:t] ## for testing
			##f = t ##
			d = 0
			#print len(inst.arguments)
			for (arg,wordNum,label) in arguments:
				 
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
				
		
				if wordNum < inst.wordnum:
					position = 'before'
				else:
					position = 'after'
				
				temp = []
				for i in range(0,len(context_labels_all)):
					if i != d:
						temp.append(context_labels_all[i])
				context_labels = ':'.join(temp)
				#context_labels = ':'.join([a for a in context_labels_all if context_labels_all.index(a) != d]) ##
				d = d + 1 ##
				#print ft + ' ' + str(context_labels_all) + ' ' + context_labels + '   ' + str(len(inst.arguments))
				#without context labels
				#print 't_word='+str(t_word)+' t_w_pos='+str(t_w_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+' pt='+pt+' position='+position+' ParentWord='+ParentWord+' ParentWordPos='+ParentWordPos+ ' '+label
				#print 't_word='+str(t_word)+' t_w_pos='+str(t_w_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+' pt='+pt+' position='+position+' ParentWord='+ParentWord+' ParentWordPos='+ParentWordPos+ ' ?'
				
				#with context labels
				print 't_word='+str(t_word)+' t_w_pos='+str(t_w_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+' pt='+pt+' position='+position+' ParentWord='+ParentWord+' ParentWordPos='+ParentWordPos+' context_labels='+context_labels+ ' '+label
				#print 't_word='+str(t_word)+' t_w_pos='+str(t_w_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+' pt='+pt+' position='+position+' ParentWord='+ParentWord+' ParentWordPos='+ParentWordPos+' context_labels='+context_labels+ ' ?'
				
			#tree.draw()
			#print ''.join(print_tree_file(parsed,[]))
			#print ''.join(print_tree_file(pred,[]))
			
			
	# to print subtrees for head finding
	#for one in list(set(all_sub_trees)):
	#	print one
	 
def read_without_context_labels():
	lines = open('propbank-results.txt').readlines()
	labels = [l.split(' ')[0] for l in lines]
	return labels
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