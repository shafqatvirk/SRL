from prepareData import *
import re
import os
def output_model(roles_25_dict,total_25_dict,roles_24_dict,total_24_dict,roles_23_dict,total_23_dict,roles_22_dict,total_22_dict,roles_21_dict,total_21_dict,roles_20_dict,total_20_dict,roles_19_dict,total_19_dict,roles_18_dict,total_18_dict,roles_17_dict,total_17_dict,roles_16_dict,total_16_dict,roles_15_dict,total_15_dict,roles_14_dict,total_14_dict,roles_13_dict,total_13_dict,roles_12_dict,total_12_dict,roles_11_dict,total_11_dict,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict):
	model_25_file = open("model_25.txt",'w')
	model_24_file = open("model_24.txt",'w')
	model_23_file = open("model_23.txt",'w')
	model_22_file = open("model_22.txt",'w')
	model_21_file = open("model_21.txt",'w')
	model_20_file = open("model_20.txt",'w')
	model_19_file = open("model_19.txt",'w')
	model_18_file = open("model_18.txt",'w')
	model_17_file = open("model_17.txt",'w')
	model_16_file = open("model_16.txt",'w')
	model_15_file = open("model_15.txt",'w')
	model_14_file = open("model_14.txt",'w')
	model_13_file = open("model_13.txt",'w')
	model_12_file = open("model_12.txt",'w')
	model_11_file = open("model_11.txt",'w')
	model_10_file = open("model_10.txt",'w')
	model_9_file = open("model_9.txt",'w')
	model_8_file = open("model_8.txt",'w')
	model_7_file = open("model_7.txt",'w')
	model_6_file = open("model_6.txt",'w')
	model_5_file = open("model_5.txt",'w')
	model_4_file = open("model_4.txt",'w')
	model_3_file = open("model_3.txt",'w')
	model_2_file = open("model_2.txt",'w')
	model_1_file = open("model_1.txt",'w')
	#model_baseline_file = open("model_baseline.txt",'w')
	
	model_temp_dict = build_temp_model(roles_25_dict,total_25_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_25_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_24_dict,total_24_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_24_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_23_dict,total_23_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_23_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_22_dict,total_22_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_22_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_21_dict,total_21_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_21_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_20_dict,total_20_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_20_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_19_dict,total_19_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_19_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_18_dict,total_18_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_18_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_17_dict,total_17_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_17_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_16_dict,total_16_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_16_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_15_dict,total_15_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_15_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_14_dict,total_14_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_14_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_13_dict,total_13_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_13_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_12_dict,total_12_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_12_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_11_dict,total_11_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_11_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_10_dict,total_10_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_10_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_9_dict,total_9_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_9_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_8_dict,total_8_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_8_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_7_dict,total_7_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_7_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_6_dict,total_6_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_6_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_5_dict,total_5_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_5_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_4_dict,total_4_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_4_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_3_dict,total_3_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_3_file.write(k+'=='+str(all_roles)+'\n')
	
	model_temp_dict = build_temp_model(roles_2_dict,total_2_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_2_file.write(k+'=='+str(all_roles)+'\n')
		
	model_temp_dict = build_temp_model(roles_1_dict,total_1_dict)
	for k in model_temp_dict.keys():
		all_roles = '||'.join([str(t) for t in sorted(model_temp_dict[k],reverse=True)])
		model_1_file.write(k+'=='+str(all_roles)+'\n')
	
def build_temp_model(roles_dict,total_dict):
	model_temp_dict = {}
	max_count = 0
	for k in roles_dict.keys():
		k_list = k.split(',')
		t = ','.join(k_list[:-1])
		new_prob = float(roles_dict[k])/total_dict[t]
		total_no = float(roles_dict[k])
		if model_temp_dict.has_key(t):
			old_roles = model_temp_dict[t]
			old_roles.append((new_prob,k_list[-1],total_no))
			model_temp_dict[t] = old_roles
			#print model_temp_dict[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,passive,left_right_child_pos,all_semType)] 
		else:
			model_temp_dict[t] = [(new_prob,k_list[-1],total_no)]
			
	return model_temp_dict
	

def find_features_without_traces(nh_pairs,parsed,predicate,target,target_POS,tree_head_dict,prop,features):
	terNo_height = nh_pairs
	#if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
	#list_of_features = []
	terNo = int(terNo_height.split(':')[0])
	height = int(terNo_height.split(':')[1])
	(arg,trNo) = traverse_tree_depth(parsed,terNo,height)
	#print predicate.terNo
	if arg != 0 and arg != None:
		if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
			return (0,0,0,0,0,0,0)
		##if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
			##print 'None'
		##else:
			##print 'YES'
		gov = find_gov(parsed,terNo,height)
		if gov != None:
			features.append('gov='+gov)
		(p,path_to_BA,path_to_BEI,voice,BA_terNo,BEI_terNo) = path(parsed,terNo,height,predicate)
		if BA_terNo < arg.terNo or BEI_terNo < arg.terNo:
			#voice_position = 'before'
			features.append('voice_position=before')
		else:
			#voice_position = 'after'
			features.append('voice_position=after')
		if arg.parent != None:
			subcatStar = find_subcat(arg.parent)
			(l_sib_pt,r_sib_pt) = find_left_right_child_pt(arg.parent,arg)
			features.append('l_sib_pt='+l_sib_pt)
			features.append('r_sib_pt='+r_sib_pt)
			features.append('subcatStar='+subcatStar)
		#else:
			#subcatStar = 'None'
			#l_sib_pt = 'None'
			#r_sib_pt = 'None'
		subcatAt = find_subcat(arg)
		#print p
		#if path_to_BA != 'no-BA' or path_to_BEI != 'no-BEI': 
			#print path_to_BA
			#print path_to_BEI
		features.append('subcatAt='+subcatAt)
		all_words = find_first_last_word(arg,[])
		#if all_words != []:
					#features.append('first_word='+all_words[0])
					#features.append('last_word='+all_words[-1])
		#if gov == None:
			#gov = 'none'
		pt = arg.data
		################
		# to print every argument tree into a file, which will be used by java program to find heads
		if pt != '-NONE-':
			#if len(arg.children) == 1 and (arg.children[0].data == '-NONE-' or arg.children[0].data == 'PP'):
			#all_words = find_first_last_word(arg,[])
			if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
				
				h_word = 'no-h-word'
				#features.append('h_word_pos='+arg.data)
				h_word_pos=arg.data
				#h_word = 'no-h-word'
				#h_word_pos = 'no-h-word-pos'
			else:
				tree_line = print_tree_file(arg,[])
				arg_tree =  ''.join(tree_line)
				#print arg_tree
				if tree_head_dict.has_key(arg_tree.rstrip()):
					head_word_and_pos = tree_head_dict[arg_tree.rstrip()]
					h_word = head_word_and_pos.split(' ')[1].rstrip(')')
					h_word_pos = head_word_and_pos.split(' ')[0].lstrip('(')
					#features.append('h_word='+head_word_and_pos.split(' ')[1].rstrip(')'))
					#features.append('h_word_pos='+ head_word_and_pos.split(' ')[0].lstrip('('))
				else:
					#print 'not found'
					h_word = 'no-h-word'
					h_word_pos = 'no-h-word-pos'
		else:
				#print 'none'
				h_word = 'no-h-word'
				h_word_pos = 'no-h-word-pos'
		#########################
		#print 'Phrase Type = ' + arg.data
		if predicate.terNo > trNo:
				features.append('position=-1')
		else:
				features.append('position=1')
		#if pt != '-NONE-':
		#list_of_features = [target,target_POS,h_word,h_word_pos,position,pt,gov]#list_of_features+'('+target+','+target_POS+','+h_word+','+h_word_pos+','+str(position)+','+pt+','+gov+')'
		features.append('layer_cons_focus='+ str(p.count('u') - p.count('d')))
		pred_parent = predicate.parent.data
		if arg.parent != None:
			arg_parent = arg.parent.data
		else:
			arg_parent = 'none'
		pred_parent_pls_arg_parent = pred_parent + arg_parent
		features.append('pred_parent_pls_arg_parent='+ pred_parent + arg_parent)
		features.append('pt='+pt)
		features.append('path='+p)
		features.append('path_to_BA='+path_to_BA)
		features.append('path_to_BEI='+path_to_BEI)
		features.append('voice='+voice)
		
		features.append('t_word_plus_pt='+ target + pt)
		
		return (target,target_POS,h_word,h_word_pos,all_words,pt,features)
	#else:
		#continue
		#return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
		#print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' SemType_h_word='+str(semType_h_word)+' semType_t_word='+str(semType_t_word)+' semType_first_word='+str(semType_first_word)+' semType_last_word='+str(semType_last_word)+' semType_t_pls_l_word='+str(semType_t_word+semType_last_word)+' layer_cons_focus='+layer_cons_focus+' all_labels=' + labels + ' pred_parent_pls_arg_parent='+pred_parent_pls_arg_parent+' label_context='+predicted_label_context+' ?'

def find_first_last_word(arg,all_words):
	if arg.word != [] and arg.word != None and arg.data != '-NONE-':
		all_words.append(arg.word)
	for ch in arg.children:
		all_words = find_first_last_word(ch,all_words)
	return all_words

def build_tree_head_dict():
	dict = {}
	trees = open('argument-trees3.txt').readlines()
	heads = open('new-heads-gbk.txt')
	for t in trees:
		dict[t.rstrip()] = heads.readline().rstrip()
		#print t.rstrip() + ',' + dict[t.rstrip()]
		#print t.rstrip()
		#print dict[t.rstrip()]
	
	return dict

def build_simplified_traditional_dict():
	dict = {}
	simplified = open('chinese-words-simplified.txt').readlines()
	traditional = open('chinese-words-traditional.txt')
	for w in simplified:
		dict[w.rstrip()] = traditional.readline().rstrip()
		#print dict[w.rstrip()]
	return dict
def frameset_dict():
	dict = {}
	file = open('./cpb-1.0/data/verbs.txt')
	for l in file.readlines()[1:]:
		tokens = l.rstrip().split('\t')
		dict[tokens[1]] = [tokens[2],tokens[0]]
	return dict
def find_verb_class(frameset,frameset_file_dict):
	frame = frameset.split('.')[0]
	f_name = '-'.join(frameset_file_dict[frame])
	full_file_name = './cpb-1.0/data/frames/' +f_name + '.xml' 
	file = open(full_file_name).read()
	framesets = re.compile('<frameset (.*?)</frameset>', re.DOTALL).findall(file)
	verb_class_list = []
	AllFrameSets = re.compile('<frameset id="(.*?)\"', re.DOTALL).findall(file)
	#print AllFrameSets
	for f in framesets:
		arguments = re.compile('<role (.*?)/>', re.DOTALL).findall(f)
		#frameset_id = re.compile('<frameset id=\"(.*?)\">', re.DOTALL).findall(f)
		#print frameset_id
		#AllFrameSets.append(frameset_id[0])
		verb_class_list.append('C'+str(len(arguments)))
	#print verb_class_list
	return (''.join(verb_class_list),''.join([f.split('"')[0] for f in AllFrameSets]))
def find_subcat(node):
	subcat = []
	subcat.append(node.data.rstrip())
	for ch in node.children:
		subcat.append(ch.data.rstrip())
	return ''.join(subcat)
def find_left_right_child_pt(tree,ch):
	indx = tree.children.index(ch)
	if len(tree.children) == 1:
		right = 'empty'
		left = 'empty'
		#left_role = 'empty'
	elif indx == 0:
		left = 'empty'
		right = tree.children[indx+1].data
		#left_role = 'empty'
	elif indx == len(tree.children)-1:
		right = 'empty'
		left = tree.children[indx-1].data
		#left_role = tree.children[indx-1].semRole
	else:
		left = tree.children[indx-1].data
		right = tree.children[indx+1].data
		#left_role = tree.children[indx-1].semRole
	return (left,right)

def remove_functional_tags(node):
	if node.data.find('-') != -1:
		node.data = node.data.split('-')[0]
	for ch in node.children:
		remove_functional_tags(ch)

def find_best_fc():
	best = []
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	result24 = open('./combinations/results24.txt').readlines()
	all = []
	for l in result24:
			all.append((float(l.rstrip()),result24.index(l)))
	(b,idx) = sorted(all,reverse=True)[0]
	c = open('./combinations/c24.txt').readlines()[idx]
	best.append([int(i) for i in c.rstrip().split(',')])
	
	all = []
	result23 = open('./combinations/results23.txt').readlines()
	for l in result23:
			all.append((float(l.rstrip()),result23.index(l)))
	(b,idx) = sorted(all,reverse=True)[0]
	c = open('./combinations/c23.txt').readlines()[idx]
	best.append([int(i) for i in c.rstrip().split(',')])
	
	all = []
	result22 = open('./combinations/results22.txt').readlines()
	for l in result22:
			all.append((float(l.rstrip()),result22.index(l)))
	(b,idx) = sorted(all,reverse=True)[0]
	c = open('./combinations/c22.txt').readlines()[idx]
	best.append([int(i) for i in c.rstrip().split(',')])
	
	all = []
	result21 = open('./combinations/results21.txt').readlines()
	for l in result21:
			all.append((float(l.rstrip()),result21.index(l)))
	(b,idx) = sorted(all,reverse=True)[0]
	c = open('./combinations/c21.txt').readlines()[idx]
	best.append([int(i) for i in c.rstrip().split(',')])
	
	all = []
	result20 = open('./combinations/results20.txt').readlines()
	for l in result20:
			all.append((float(l.rstrip()),result20.index(l)))
	(b,idx) = sorted(all,reverse=True)[0]
	c = open('./combinations/c20.txt').readlines()[idx]
	best.append([int(i) for i in c.rstrip().split(',')])
	
	
	
	'''
	best.append([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	
	
	best.append([11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([12,13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([13,14,15,16,17,18,19,20,21,22,23,24])
	best.append([14,15,16,17,18,19,20,21,22,23,24])
	
	best.append([0,1,2,3,4,5,6,7,8,9])
	
	best.append([0,1,2,3,4,5,6,7,8])
	best.append([0,1,2,3,4,5,6,7])
	best.append([0,1,2,3,4,5,6])
	best.append([0,1,2,3,4,5])
	
	all = []
	result5 = open('./combinations/results5.txt').readlines()
	for l in result5:
			all.append((float(l.rstrip()),result5.index(l)))
	(b,idx) = sorted(all,reverse=True)[0]
	c = open('./combinations/c5.txt').readlines()[idx]
	best.append([int(i) for i in c.rstrip().split(',')])
	
	best.append([0,1,2,3])
	best.append([0,1,2])
	best.append([0,1])
	best.append([0])'''
	
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
	
	best.append([0,1,2,3,4,5,6,7,8,9])
	best.append([0,1,2,3,4,5,6,7])
	best.append([0,1,2,3,4,5,6])
	best.append([0,1,3,4,5,6])
	best.append([1,2,3,4,5,6])
	best.append([0,1,2,4,5,6])
	best.append([0,2,3,4,5,6])
	best.append([1,3,4,5,6])
	best.append([0,2,4,5,6])
	best.append([1,2,4,5,6])
	best.append([0,3,4,5,6])
	best.append([0,2,5])
	best.append([0,2])
	best.append([0,1,4,5,6])
	
	#print best
	return best

def find_best_fc2():
	best = []
	l = int(0)
	u = int(2)
	best.append([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
	result24 = open('./combinations/results24.txt').readlines()
	all = []
	
	for l in result24:
			all.append((float(l.rstrip()),result24.index(l)))
	top4 = sorted(all,reverse=True)[:u]
	for (b,idx) in top4:
		c = open('./combinations/c24.txt').readlines()[idx]
		best.append([int(i) for i in c.rstrip().split(',')])
	
	all = []
	result23 = open('./combinations/results23.txt').readlines()
	for l in result23:
			all.append((float(l.rstrip()),result23.index(l)))
	top4 = sorted(all,reverse=True)[:u]
	for (b,idx) in top4:
		c = open('./combinations/c23.txt').readlines()[idx]
		best.append([int(i) for i in c.rstrip().split(',')])	
	
	all = []
	result22 = open('./combinations/results22.txt').readlines()
	for l in result22:
			all.append((float(l.rstrip()),result22.index(l)))
	top4 = sorted(all,reverse=True)[:u]
	for (b,idx) in top4:
		c = open('./combinations/c22.txt').readlines()[idx]
		best.append([int(i) for i in c.rstrip().split(',')])

	all = []
	result21 = open('./combinations/results21.txt').readlines()
	for l in result21:
			all.append((float(l.rstrip()),result21.index(l)))
	top4 = sorted(all,reverse=True)[:u]
	for (b,idx) in top4:
		c = open('./combinations/c21.txt').readlines()[idx]
		best.append([int(i) for i in c.rstrip().split(',')])
		
	all = []
	result20 = open('./combinations/results20.txt').readlines()
	for l in result20:
			all.append((float(l.rstrip()),result20.index(l)))
	top4 = sorted(all,reverse=True)[:1]
	for (b,idx) in top4:
		c = open('./combinations/c20.txt').readlines()[idx]
		best.append([int(i) for i in c.rstrip().split(',')])
	
	all = []
	result19 = open('./combinations/results19.txt').readlines()
	for l in result19:
			all.append((float(l.rstrip()),result19.index(l)))
	top4 = sorted(all,reverse=True)[:1]
	for (b,idx) in top4:
		c = open('./combinations/c19.txt').readlines()[idx]
		best.append([int(i) for i in c.rstrip().split(',')])
		
	best.append([0,1,2,3,4,5,6,7,8,9])
	best.append([0,1,2,3,4,5,6,7])
	best.append([0,1,2,3,4,5,6])
	best.append([0,1,3,4,5,6])
	best.append([1,2,3,4,5,6])
	best.append([0,1,2,4,5,6])
	best.append([0,2,3,4,5,6])
	best.append([1,3,4,5,6])
	best.append([0,2,4,5,6])
	best.append([1,2,4,5,6])
	best.append([0,3,4,5,6])
	best.append([0,2,5])
	best.append([0,2])
	best.append([0,1,4,5,6])
	
	'''best.append([1,3,4,5,6])
	best.append([0,2,4,5,6])
	best.append([1,2,4,5,6])
	best.append([0,3,4,5,6])
	#best.append([0,2,5])
	#best.append([0,2])
	best.append([0,1,4,5,6])'''
	return best

def build_context_labels(): # fro training
	context_labels_list = []
	prop_bank = open('propbank.train').readlines()
	idx_1 = 0
	for prop in prop_bank[0:]:
	  label_context = []
	  ids = prop.split(' ')
	  file_id = ids[0].split('/')[2]
	  tree_no = int(ids[1])
	  predicate_no = int(ids[2])
	  frameset = ids[4]
	  args = ids[6:]
	  file_path = os.path.join("./bracketed/", file_id)
	  trees = convert_trees(file_path)
	  
	  expr = ''.join(list(trees[tree_no].rstrip())[1:-1]).rstrip(' ').lstrip(' ')
	  (parsed,r) = parseExpr(expr,0,0)
	  (predicate,pred_terNo) = traverse_tree_depth(parsed,predicate_no,0)
	  if predicate != 0 and predicate.word == ids[4].split('.')[0]:
		for arg in args:
			label = '-'.join(arg.split('-')[1:]).rstrip()
			##if label.split('-')[0] in ['ARG0','ARG1','ARG2','ARG3','ARG4']:
				##label = label.split('-')[0]
			##else:
				##label = label.rstrip()
			if label.rstrip() != 'rel':
			
			 nh_pairs = arg.split('-')[0]
			 if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
				
				#isNoneTer = isNone(parsed,nh_pairs)
				#if isNoneTer == True:
					#continue
				label_context.append(label)
		#print label_context
		context_labels_list.append(label_context)
	return context_labels_list

def isNone(parsed,nh_pairs):
	terNo_height = nh_pairs
	terNo = int(terNo_height.split(':')[0])
	height = int(terNo_height.split(':')[1])
	(arg,trNo) = traverse_tree_depth(parsed,terNo,height)
	if arg != 0 and arg != None:
		if (len(arg.children) == 1 and (arg.children[0].data == '-NONE-')) or arg.data == '-NONE-':
				return True
		pt = arg.data
		if pt != '-NONE-':
			if len(arg.children) == 1 and (arg.children[0].data == '-NONE-'):
				return True
		else:
				#print 'none'
				return True
		#########################
		return False
	else:
		return True

	
def make_context_list(): # for testing
	list = []
	indexs = open('counter-stats.txt').readlines()
	labels = open('ch-propbank-results.txt').readlines()
	labels_list = [lb.split(' ')[0] for lb in labels]
	start = 0
	upto = 0
	for l in indexs:
		upto = start + int(l.rstrip())
		list.append(labels_list[start:upto])
		start = upto
	return list
	