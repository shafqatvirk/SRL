# for experiments including null nodes, and using the context lables
from prepareData import *
from buildModelAuxiliaries3 import *
from auxiliaryFuns import *
from ehownet import *
#from jianfan import jtof
import os
def build(tree_head_dict,simplified_tradictional_dict):
	word2semType_dict = word2semType()
	frameset_file_dict = frameset_dict()
	e_hownet=EHowNetTree("ehownet_ontology.txt")
	context_labels_list = make_context_list() # for test
	#context_labels_list = build_context_labels() # for training will not used any more as we are building this list locally
	
	prop_bank = open('propbank.test').readlines()
	#prop_bank = open('dev.test').readlines()
	total = 0
	idx_1 = 0
	for prop in prop_bank[0:]:
	  #print prop
	#for prop in prop_bank[5193:5194]:
	#if list(prop)[0]!='#':
	  #print prop
	 
	  ids = prop.split(' ')
	  file_id = ids[0].split('/')[2]
	  tree_no = int(ids[1])
	  predicate_no = int(ids[2])
	  frameset = ids[4]
	  args = ids[6:]
	  ##############
	  '''args2 = []
	  for ar in args:
		l = '-'.join(ar.split('-')[1:])
		a = ar.split('-')[0]
		ags = [z+'-'+l for z in (sum([y.split(';') for y in sum([x.split(',') for x in a.split('*')],[])],[]))]
		args2.append(ags)
	  args = sum(args2,[])'''
	  ##############
	  file_path = os.path.join("./bracketed/", file_id)
	  trees = convert_trees(file_path)
	  
	  expr = ''.join(list(trees[tree_no].rstrip())[1:-1]).rstrip(' ').lstrip(' ')
	  #print expr
	  #print
	  (parsed,r) = parseExpr(expr,0,0)
	  #remove_functional_tags(parsed)
	  ### to get all words
	  
	  
	  (predicate,pred_terNo) = traverse_tree_depth(parsed,predicate_no,0)
	  if predicate != 0 and predicate.word == ids[4].split('.')[0]:
		#print predicate.word
		#print prop_bank.index(prop)
		
		#print predicate
		target = ids[4].split('.')[0]
		target_POS = predicate.data
	
		(verb_class,AllFrameSets) = find_verb_class(frameset,frameset_file_dict)
		subcat = find_subcat(predicate.parent)
		#print subcat
		#print AllFrameSets
		all_labels = []
		label_list = []
		#label_list = ['-'.join(a.split('-')[1:]) for a in args]
		#################
		for a in args:
			if a.find('*') == -1 and a.find(';')==-1 and a.find(';')==-1:
				label_list.append('-'.join(a.split('-')[1:]))
		#################
		
		if 'rel\n' in label_list:
			label_list.remove('rel\n')
		#if 'rel' in label_list:
			#label_list.remove('rel')
		counter = 0
		predicted_label_context_list = context_labels_list[idx_1]
		idx_1 = idx_1 + 1
		idx_2 = 0
		d = 0 #!
		for arg in args:
			
			features = []
			features.append('subcat='+subcat)
			label = '-'.join(arg.split('-')[1:])
			###################### this is used to build context label feature for training

			temp2 = [] #!
			for i in range(0,len(label_list)):
				if i != d:
					temp2.append(label_list[i].rstrip())
			label_context = ''.join(temp2)
			
			#########################
			
			if label.split('-')[0] in ['ARG0','ARG1','ARG2','ARG3','ARG4']:
				label = label.split('-')[0]
			else:
				label = label.rstrip()
				
			complete_label = label.rstrip()
			if label.rstrip() != 'rel':
			#if label.rstrip() != 'rel' and label.rstrip() not in ['ARG-LOC','ARGM-TMP','ARGM-GOL','ARGM-MNR','ARGM-CAU','ARGM-ADV']: # to exclude functional tags
			 nh_pairs = arg.split('-')[0]
			 
			 ###################################
			 # depending on whether to use traces or not
			 #features = find_features(list(nh_pairs),parsed,predicate,target,target_POS,tree_head_dict)
			 if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
				#tree_head_dict = ''
				(t_word,t_word_pos,h_word,h_word_pos,all_words,pt,features) = find_features_without_traces(nh_pairs,parsed,predicate,target,target_POS,tree_head_dict,prop,features)
				if t_word == 0 and t_word_pos == 0 and h_word == 0 and h_word_pos == 0 and all_words == 0 and features == 0:
					idx_2 = idx_2 + 1
					d = d + 1 #!
					continue
				
				if all_words != []:
					first_word = all_words[0]
					last_word = all_words[-1]
				else:
					first_word = 'no-first-word'
					last_word = 'no-last-word'
					
				labels = '-'.join(all_labels)
				############# simplified to traditional conversion
				#print 'before '+t_word
				if simplified_tradictional_dict.has_key(h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore')):
					#print 'yes'
					h_word_trad = simplified_tradictional_dict[h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore')]
				if simplified_tradictional_dict.has_key(t_word):
					t_word_trad = simplified_tradictional_dict[t_word]
					#print 'after '+t_word_trad
				if simplified_tradictional_dict.has_key(first_word):
					first_word_trad = simplified_tradictional_dict[first_word]
				if simplified_tradictional_dict.has_key(last_word):
					last_word_trad = simplified_tradictional_dict[last_word]
				################################
				
				############################### use of ehownet
				'''if h_word != 'no-h-word' and h_word_pos != 'no-h-word-pos': 
					semType_h_word = find_semType(h_word,h_word_pos,e_hownet,word2semType_dict)
					if semType_h_word != 'no-type':
						h_word = semType_h_word # later should use proper label and replac h_word by semType_h_word
				semType_t_word = find_semType(target,target_POS,e_hownet,word2semType_dict)
				if semType_t_word != 'no-type':
					t_word = semType_t_word # later should use proper label and replac t_word by semType_t_word
				
				if first_word != 'no-first-word':
					semType_first_word = find_semType(first_word,'',e_hownet,word2semType_dict)
					if semType_first_word != 'no-type':
						first_word = semType_first_word # later should use proper label and replac h_word by semType_h_word
				if last_word != 'no-last-word':
					semType_last_word = find_semType(last_word,'',e_hownet,word2semType_dict)
					if semType_last_word != 'no-type':
						last_word = semType_last_word # later should use proper label and replac t_word by semType_t_word
				'''
				if h_word != 'no-h-word' and h_word_pos != 'no-h-word-pos': 
					semType_h_word = find_semType(h_word_trad,h_word_pos,e_hownet,word2semType_dict)
					
				semType_t_word = find_semType(t_word_trad,target_POS,e_hownet,word2semType_dict)
				if first_word != 'no-first-word':
					semType_first_word = find_semType(first_word_trad,'',e_hownet,word2semType_dict)
				if last_word != 'no-last-word':
					semType_last_word = find_semType(last_word_trad,'',e_hownet,word2semType_dict)
			
				######################## this is used for building predicted context lable feature for testing
				
				temp = []
				for b in range(0,len(predicted_label_context_list)):
					if b != idx_2:
						temp.append(predicted_label_context_list[b])
				predicted_label_context = ''.join(temp)		
				###############################
				h_word = h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore') # to make everything into once encoding
				features.append('t_word='+str(t_word))
				features.append('t_word_pls_pt='+str(t_word)+str(pt))
				features.append('t_word_pos='+str(t_word_pos))
				if h_word != 'no-h-word':
					features.append('h_word='+str(h_word))
					features.append('semType_h_word='+str(semType_h_word))
					features.append('t_word_pls_h_word='+t_word+h_word)
				if all_words != []:
					features.append('first_word='+first_word)
					features.append('last_word='+last_word)
					features.append('semType_first_word='+str(semType_first_word))
					features.append('semType_last_word='+str(semType_last_word))
					#features.append('semType_t_word_pls_l_word='semType_t_word+last_word)
					features.append('semType_t_pls_l_word='+str(semType_t_word+semType_last_word))
				features.append('h_word_pos='+str(h_word_pos))
				
				features.append('verbClass='+verb_class)
				features.append('verbClass_pls_pt='+verb_class+pt)
				features.append('verbClass_pls_h_word='+verb_class+h_word)
				features.append('allFrameSets='+str(AllFrameSets))
				features.append('verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets))
				
				features.append('semType_t_word='+str(semType_t_word))
				
				features.append('all_labels=' + labels )
				features.append('label_context='+predicted_label_context) # use this for testing
				#features.append('label_context='+label_context) # use this for training
				
				#print str(args) + ' ' +str(d) + ' ' + str(label_list) + ' ' + label_context
				#print ' '.join(features) + ' ' + label.rstrip()
				print ' '.join(features) + ' ?'
				
				counter = counter + 1
				idx_2 = idx_2 + 1
				d = d + 1 #!
				all_labels.append(complete_label)
				
			 #else:
				#idx_2 = idx_2 + 1
				#d = d + 1 #!
		#print	
		#print counter
		#total = total + counter
		#counter = 0
		d = 0 #!
		idx_2 = 0
	  else:
		continue
	#print total
	
def build_dict(roles_dict,total_dict,all_features,f_c):
	fc = ','.join([all_features[i] for i in f_c]) + ','+all_features[-1]
	fc_t = ','.join([all_features[i] for i in f_c])
	if roles_dict.has_key((fc)):
						roles_dict[(fc)] = roles_dict[(fc)] + 1 
	else:
						roles_dict[(fc)] =  1
	if total_dict.has_key((fc_t)):
						total_dict[(fc_t)] = total_dict[(fc_t)] + 1 
	else:
						total_dict[(fc_t)] =  1
	return (roles_dict,total_dict)
	
def   print_words(node,words):
	if node.word != [] and node.word != None and node.data != '-NONE-':
		words.append(node.word)
	for ch in node.children:
		print_words(ch,words)
	return words
def remove_none_nodes():
	non_stats = open('none-stats.txt').readlines()
	prop_bank_results = open('C:/shafqat/PostDoc/SRL/experiments/SRLTraining/maxent/opennlp-maxent/opennlp-maxent-3.0.0/samples/sports/ch-propbank-results.txt').readlines()
	gold = open('C:/shafqat/PostDoc/SRL/experiments/SRLTraining/maxent/test.txt').readlines()
	new_prop_bank_results = open('C:/shafqat/PostDoc/SRL/experiments/SRLTraining/maxent/opennlp-maxent/opennlp-maxent-3.0.0/samples/sports/new-ch-propbank-results.txt','w')
	new_gold = open('C:/shafqat/PostDoc/SRL/experiments/SRLTraining/maxent/new-test.txt','w')
	
	for (a,b,c) in zip(non_stats,prop_bank_results,gold):
		if a.rstrip() == 'YES':
			new_prop_bank_results.write(b)
			new_gold.write(c)

if __name__ == "__main__":
 import sys
 try:
	simplified_tradictional_dict = build_simplified_traditional_dict()
	tree_head_dict = build_tree_head_dict()
	build(tree_head_dict,simplified_tradictional_dict)
	#remove_none_nodes()
	#for k in roles_25_dict.keys():
	#	print k
	#	print roles_25_dict[k]
	#output_model(roles_25_dict,total_25_dict,roles_24_dict,total_24_dict,roles_23_dict,total_23_dict,roles_22_dict,total_22_dict,roles_21_dict,total_21_dict,roles_20_dict,total_20_dict,roles_19_dict,total_19_dict,roles_18_dict,total_18_dict,roles_17_dict,total_17_dict,roles_16_dict,total_16_dict,roles_15_dict,total_15_dict,roles_14_dict,total_14_dict,roles_13_dict,total_13_dict,roles_12_dict,total_12_dict,roles_11_dict,total_11_dict,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict)
 except:
	print >>sys.stderr, __doc__
	raise