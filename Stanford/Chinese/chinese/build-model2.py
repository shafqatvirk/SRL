from prepareData import *
from buildModelAuxiliaries2 import *
from auxiliaryFuns import *
from ehownet import *
#from jianfan import jtof
import os
def build(tree_head_dict,simplified_tradictional_dict):
	roles_25_dict = {}
	total_25_dict = {}
	roles_24_dict = {}
	total_24_dict = {}
	roles_23_dict = {}
	total_23_dict = {}
	roles_22_dict = {}
	total_22_dict = {}
	roles_21_dict = {}
	total_21_dict = {}
	roles_20_dict = {}
	total_20_dict = {}
	roles_19_dict = {}
	total_19_dict = {}
	roles_18_dict = {}
	total_18_dict = {}
	roles_17_dict = {}
	total_17_dict = {}
	roles_16_dict = {}
	total_16_dict = {}
	roles_15_dict = {}
	total_15_dict = {}
	roles_14_dict = {}
	total_14_dict = {}
	roles_13_dict = {}
	total_13_dict = {}
	roles_12_dict = {}
	total_12_dict = {}
	roles_11_dict = {}
	total_11_dict = {}
	roles_10_dict = {}
	total_10_dict = {}
	roles_9_dict = {}
	total_9_dict = {}
	roles_8_dict = {}
	total_8_dict = {}
	roles_7_dict = {}
	total_7_dict = {}
	roles_6_dict = {}
	total_6_dict = {}
	roles_5_dict = {}
	total_5_dict = {}
	roles_4_dict = {}
	total_4_dict = {}
	roles_3_dict = {}
	total_3_dict = {}
	roles_2_dict = {}
	total_2_dict = {}
	roles_1_dict = {}
	total_1_dict = {}
	f_c = find_best_fc2()
	#f_c = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24]]
	word2semType_dict = word2semType()
	frameset_file_dict = frameset_dict()
	e_hownet=EHowNetTree("ehownet_ontology.txt")
	#prop_bank = open('cpb1.0.txt').readlines()
	prop_bank = open('propbank.test').readlines()
	#prop_bank = open('dev.test').readlines()
	for prop in prop_bank[:]:
	
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
	  #chinese_words = print_words(parsed,[],file_id,tree_no)
	  #for w in list(set(chinese_words)):
		#print w
	  ############
	  #if file_id not in ['chtb_845.fid','chtb_437.fid','chtb_672.fid','chtb_794.fid','chtb_307.fid','chtb_088.fid','chtb_793.fid',
	  #					'chtb_052.fid','chtb_792.fid','chtb_828.fid','chtb_139.fid','chtb_112.fid','chtb_855.fid']:
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
		label_list = ['-'.join(a.split('-')[1:]) for a in args]
		if 'rel\n' in label_list:
			label_list.remove('rel\n')
		for arg in args:
			label = '-'.join(arg.split('-')[1:])
			label_context = ''.join([l.rstrip() for l in label_list if l != label])
			complete_label = label.rstrip()
			if label.split('-')[0] in ['ARG0','ARG1','ARG2','ARG3','ARG4']:
				label = label.split('-')[0]
			else:
				label = label.rstrip()
			if label.rstrip() != 'rel':
			#if label.rstrip() != 'rel' and label.rstrip() not in ['ARG-LOC','ARGM-TMP','ARGM-GOL','ARGM-MNR','ARGM-CAU','ARGM-ADV']: # to exclude functional tags
			 nh_pairs = arg.split('-')[0]
			 #terNo_height_list = sum([b.split(';') for b in sum([a.split(',') for a in nh_pairs.split('*')],[])],[])
			 ###################################
			 # depending on whether to use traces or not
			 #features = find_features(list(nh_pairs),parsed,predicate,target,target_POS,tree_head_dict)
			 if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
				#tree_head_dict = ''
				(t_word,t_word_pos,h_word,h_word_pos,position,pt,gov,all_words,p,path_to_BA,path_to_BEI,voice,subcatStar,subcatAt,l_sib_pt,r_sib_pt,voice_position,layer_cons_focus,pred_parent_pls_arg_parent) = find_features_without_traces(nh_pairs,parsed,predicate,target,target_POS,tree_head_dict,prop)
				if t_word == 0 and t_word_pos == 0 and h_word == 0 and h_word_pos == 0 and position == 0 and pt == 0 and gov == 0:
					continue
				# some phrasetype has = sign which conflits with our models format, just remove it
				#print h_word
				#print t_word_pos
				if pt.find('=') != -1:
					pt = ''.join(pt.split('=')[0])
					
				t_word_plus_pt = t_word + pt
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
			
				###############################
				h_word = h_word.decode('utf-8-sig','ignore').encode('gb2312','ignore') # to make everything into once encoding
				#baseline
				#print 't_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' t_word_plus_pt='+str(t_word_plus_pt)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' voice_position='+str(voice_position)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' '+label.rstrip()
				#print 't_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' t_word_plus_pt='+str(t_word_plus_pt)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' voice_position='+str(voice_position)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' ?'
				# full feature model
				#print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' all_labels=' + labels + ' pred_parent_pls_arg_parent='+pred_parent_pls_arg_parent+' label_context='+label_context+' '+label.rstrip()
				print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' all_labels=' + labels + ' pred_parent_pls_arg_parent='+pred_parent_pls_arg_parent+' label_context='+label_context+' ?'
				#print str(t_word)+' '+str(t_word_pos)+','+str(h_word)+' '+str(h_word_pos)+' '+str(position)+' '+str(pt)+' '+str(gov.rstrip())+' '+str(t_word_plus_pt)+ ' '+str(t_word+h_word)+' '+first_word+ ' '+last_word+' '+str(voice)+' '+str(subcat)+' '+str(subcatStar)+' '+str(subcatAt)+' '+str(p)+' '+str(path_to_BA)+' '+str(path_to_BEI)+' '+str(verb_class)+' '+(verb_class+pt)+ ' '+str(verb_class+h_word)+' '+str(l_sib_pt)+ ' '+str(r_sib_pt)+ ' '+str(AllFrameSets)+ ' '+str(verb_class+AllFrameSets)+' '+label.rstrip()
				all_labels.append(complete_label)
				'''all_features = [str(t_word),str(t_word_pos),str(h_word),str(h_word_pos),str(position),str(pt),str(gov.rstrip()),str(t_word_plus_pt),str(t_word+h_word),first_word,last_word,str(voice),str(subcat.rstrip()),str(subcatStar.rstrip()),str(subcatAt.rstrip()),str(p),str(path_to_BA),str(path_to_BEI),str(verb_class),(verb_class+pt),str(verb_class+h_word),str(l_sib_pt),str(r_sib_pt),str(AllFrameSets),str(verb_class+AllFrameSets),label.rstrip()]
				(roles_25_dict,total_25_dict)= build_dict(roles_25_dict,total_25_dict,all_features,f_c[0])
				(roles_24_dict,total_24_dict)= build_dict(roles_24_dict,total_24_dict,all_features,f_c[1])
				(roles_23_dict,total_23_dict)= build_dict(roles_23_dict,total_23_dict,all_features,f_c[2])
				(roles_22_dict,total_22_dict)= build_dict(roles_22_dict,total_22_dict,all_features,f_c[3])
				(roles_21_dict,total_21_dict)= build_dict(roles_21_dict,total_21_dict,all_features,f_c[4])
				(roles_20_dict,total_20_dict)= build_dict(roles_20_dict,total_20_dict,all_features,f_c[5])
				(roles_19_dict,total_19_dict)= build_dict(roles_19_dict,total_19_dict,all_features,f_c[6])
				(roles_18_dict,total_18_dict)= build_dict(roles_18_dict,total_18_dict,all_features,f_c[7])
				(roles_17_dict,total_17_dict)= build_dict(roles_17_dict,total_17_dict,all_features,f_c[8])
				(roles_16_dict,total_16_dict)= build_dict(roles_16_dict,total_16_dict,all_features,f_c[9])
				(roles_15_dict,total_15_dict)= build_dict(roles_15_dict,total_15_dict,all_features,f_c[10])
				(roles_14_dict,total_14_dict)= build_dict(roles_14_dict,total_14_dict,all_features,f_c[11])
				(roles_13_dict,total_13_dict)= build_dict(roles_13_dict,total_13_dict,all_features,f_c[12])
				(roles_12_dict,total_12_dict)= build_dict(roles_12_dict,total_12_dict,all_features,f_c[13])
				(roles_11_dict,total_11_dict)= build_dict(roles_11_dict,total_11_dict,all_features,f_c[14])
				(roles_10_dict,total_10_dict)= build_dict(roles_10_dict,total_10_dict,all_features,f_c[15])
				(roles_9_dict,total_9_dict)= build_dict(roles_9_dict,total_9_dict,all_features,f_c[16])
				(roles_8_dict,total_8_dict)= build_dict(roles_8_dict,total_8_dict,all_features,f_c[17])
				(roles_7_dict,total_7_dict)= build_dict(roles_7_dict,total_7_dict,all_features,f_c[18])
				(roles_6_dict,total_6_dict)= build_dict(roles_6_dict,total_6_dict,all_features,f_c[19])
				
				
				(roles_5_dict,total_5_dict)= build_dict(roles_5_dict,total_5_dict,all_features,f_c[20])
				(roles_4_dict,total_4_dict)= build_dict(roles_4_dict,total_4_dict,all_features,f_c[21])
				(roles_3_dict,total_3_dict)= build_dict(roles_3_dict,total_3_dict,all_features,f_c[22])
				(roles_2_dict,total_2_dict)= build_dict(roles_2_dict,total_2_dict,all_features,f_c[23])
				(roles_1_dict,total_1_dict)= build_dict(roles_1_dict,total_1_dict,all_features,f_c[24])'''
	  else:
		continue
	return (roles_25_dict,total_25_dict,roles_24_dict,total_24_dict,roles_23_dict,total_23_dict,roles_22_dict,total_22_dict,roles_21_dict,total_21_dict,roles_20_dict,total_20_dict,roles_19_dict,total_19_dict,roles_18_dict,total_18_dict,roles_17_dict,total_17_dict,roles_16_dict,total_16_dict,roles_15_dict,total_15_dict,roles_14_dict,total_14_dict,roles_13_dict,total_13_dict,roles_12_dict,total_12_dict,roles_11_dict,total_11_dict,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict)
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
if __name__ == "__main__":
 import sys
 try:
	simplified_tradictional_dict = build_simplified_traditional_dict()
	tree_head_dict = build_tree_head_dict()
	(roles_25_dict,total_25_dict,roles_24_dict,total_24_dict,roles_23_dict,total_23_dict,roles_22_dict,total_22_dict,roles_21_dict,total_21_dict,roles_20_dict,total_20_dict,roles_19_dict,total_19_dict,roles_18_dict,total_18_dict,roles_17_dict,total_17_dict,roles_16_dict,total_16_dict,roles_15_dict,total_15_dict,roles_14_dict,total_14_dict,roles_13_dict,total_13_dict,roles_12_dict,total_12_dict,roles_11_dict,total_11_dict,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict) = build(tree_head_dict,simplified_tradictional_dict)
	#for k in roles_25_dict.keys():
	#	print k
	#	print roles_25_dict[k]
	#output_model(roles_25_dict,total_25_dict,roles_24_dict,total_24_dict,roles_23_dict,total_23_dict,roles_22_dict,total_22_dict,roles_21_dict,total_21_dict,roles_20_dict,total_20_dict,roles_19_dict,total_19_dict,roles_18_dict,total_18_dict,roles_17_dict,total_17_dict,roles_16_dict,total_16_dict,roles_15_dict,total_15_dict,roles_14_dict,total_14_dict,roles_13_dict,total_13_dict,roles_12_dict,total_12_dict,roles_11_dict,total_11_dict,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict)
 except:
	print >>sys.stderr, __doc__
	raise