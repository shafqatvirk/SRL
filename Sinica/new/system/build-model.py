from ehownet import *
#from auxiliaryFuns import *
from auxiliaryFunsFullFeatures import *
from parseTree import *

def make_training_data():
	#conll = open("../CoNLL2006-2007/10-fold-data/10-fold-data.txt").readlines()
	exprs = open("../data/sinica-treebank-full-3.2a.txt").readlines()
	traing_trees = []
	#excluded = [e for e in exprs if e not in conll]
	traing_trees = []
	#for expr in excluded:#exprs[:56000]:
	for expr in exprs:
			tre = parseExpr(expr.rstrip())
			traing_trees.append(tre)
	return traing_trees 
	

def build_model(tree,e_hownet,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict,target_pos,idx,prep_pos,word2semType_dict,legal_role_combination,unique_roles,pp,model_maxent_file):
	if tree != None:
	 if tree.children != []:
		(h_word,h_pos) = find_h_word(tree)
		semType_h_word = find_semType(h_word,h_pos,e_hownet,word2semType_dict)
		h_found=1
		legal_roles = []
		for ch in tree.children:
			if ch.semRole != 'Head' and ch.semRole != 'head':
				
				(l_sib_pt,r_sib_pt) = find_left_right_child_pt(tree,ch)
				all_words_semType = find_l_r_w_semType(ch,prep_pos,e_hownet,word2semType_dict,[])
				first_word_semType = all_words_semType[0]
				last_word_semType = all_words_semType[-1]
				#(semType_t_word,t_word_pos) = find_t_w_semType(ch,prep_pos,e_hownet,word2semType_dict)
				pt = ch.pos
				pt_of_parent = tree.pos
				voice = find_voice(ch,pp,'active')
				(subcatAt,subcatStar) = find_subcat(tree,ch)
				path_to_BA = path(ch,pp)
				
				(left_right_child_pos,left_role) = find_left_right_child_pos(tree,ch)
				all_pos_list = find_pos(ch,[])
				all_pos = '-'.join(all_pos_list)
				all_semType = find_all_semType(tree,e_hownet,[],word2semType_dict)
				verb_pos_all = find_verb_pos(ch,[])
				if verb_pos_all != [] and verb_pos_all[0] != '':
					verb_pos = verb_pos_all[0]
				else:
					verb_pos = 'no-verb-pos'
				if h_found == 1:
					position = -1
				else:
					position = 1
				if ch.word == []:
					(t_word,tg_pos) = find_t_word2(ch,prep_pos,'','')
					if ch.pos == 'PP' or ch.pos == 'GP':	
						(t_t_word,tg_t_pos) = find_t_word(ch,prep_pos,'','')
						t_word_pos = tg_pos
						semType_p_w = find_semType(t_word,tg_pos,e_hownet,word2semType_dict)
						t_word = t_t_word
						semType_w = find_semType(t_t_word,tg_t_pos,e_hownet,word2semType_dict)
						semType_t_word = semType_p_w+'...'+semType_w
					else:
						t_word_pos = ch.pos
						semType_t_word = find_semType(t_word,tg_pos,e_hownet,word2semType_dict)
				else:
					
					semType_t_word = find_semType(ch.word,ch.pos,e_hownet,word2semType_dict)
					t_word_pos = ch.pos
				
				model_maxent_file.write('semType_h_word='+semType_h_word+' h_pos='+h_pos+' semType_t_word='+semType_t_word+' t_word_pos='+t_word_pos+' pt='+pt+' pt_of_parent='+pt_of_parent+' position='+str(position)+' l_sib_pt='+l_sib_pt+' r_sib_pt='+r_sib_pt+' voice='+voice+' first_word_semType='+first_word_semType+' last_word_semType='+last_word_semType+' f_w_semType_pls_l_w_semType='+first_word_semType+last_word_semType+' subcatAt='+subcatAt+' subcatStar='+subcatStar+' path_to_BA='+str(path_to_BA)+' '+ch.semRole+'\n')
				
				if ch.semRole not in unique_roles:
					unique_roles.append(ch.semRole)
				# model 10
				if roles_10_dict.has_key((semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType,ch.semRole)):
						roles_10_dict[(semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType,ch.semRole)] = roles_10_dict[(semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType,ch.semRole)] + 1 
				else:
						roles_10_dict[(semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType,ch.semRole)] =  1
				if total_10_dict.has_key((semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType)):
						total_10_dict[(semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType)] = total_10_dict[(semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType)] + 1 
				else:
						total_10_dict[(semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,position,all_pos,voice,left_right_child_pos,all_semType)] =  1
				#model 9 
				if roles_9_dict.has_key((h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice,ch.semRole)):
						roles_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice,ch.semRole)] = roles_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice,ch.semRole)] + 1 
				else:
						roles_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice,ch.semRole)] =  1
				if total_9_dict.has_key((h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice)):
						total_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice)] = total_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice)] + 1 
				else:
						total_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,verb_pos,voice)] =  1
				
				'''if roles_9_dict.has_key((h_pos,semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)):
						roles_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)] = roles_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)] + 1 
				else:
						roles_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)] =  1
				if total_9_dict.has_key((h_pos,semType_t_word,t_word_pos,tree.pos,position,voice)):
						total_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,voice)] = total_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,voice)] + 1 
				else:
						total_9_dict[(h_pos,semType_t_word,t_word_pos,tree.pos,position,voice)] =  1'''
				#model 8 
				if roles_8_dict.has_key((semType_h_word,h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)):
						roles_8_dict[(semType_h_word,h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)] = roles_8_dict[(semType_h_word,h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)] + 1 
				else:
						roles_8_dict[(semType_h_word,h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)] =  1
				if total_8_dict.has_key((semType_h_word,h_pos,t_word_pos,tree.pos,position,voice)):
						total_8_dict[(semType_h_word,h_pos,t_word_pos,tree.pos,position,voice)] = total_8_dict[(semType_h_word,h_pos,t_word_pos,tree.pos,position,voice)] + 1 
				else:
						total_8_dict[(semType_h_word,h_pos,t_word_pos,tree.pos,position,voice)] =  1
				#model 7 
				if roles_7_dict.has_key((semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)):
						roles_7_dict[(semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)] = roles_7_dict[(semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)] + 1 
				else:
						roles_7_dict[(semType_t_word,t_word_pos,tree.pos,position,voice,ch.semRole)] =  1
				if total_7_dict.has_key((semType_t_word,t_word_pos,tree.pos,position,voice)):
						total_7_dict[(semType_t_word,t_word_pos,tree.pos,position,voice)] = total_7_dict[(semType_t_word,t_word_pos,tree.pos,position,voice)] + 1 
				else:
						total_7_dict[(semType_t_word,t_word_pos,tree.pos,position,voice)] =  1
				#model 6 
				if roles_6_dict.has_key((h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)):
						roles_6_dict[(h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)] = roles_6_dict[(h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)] + 1 
				else:
						roles_6_dict[(h_pos,t_word_pos,tree.pos,position,voice,ch.semRole)] =  1
				if total_6_dict.has_key((h_pos,t_word_pos,tree.pos,position,voice)):
						total_6_dict[(h_pos,t_word_pos,tree.pos,position,voice)] = total_6_dict[(h_pos,t_word_pos,tree.pos,position,voice)] + 1 
				else:
						total_6_dict[(h_pos,t_word_pos,tree.pos,position,voice)] =  1
				# model 5
				if roles_5_dict.has_key((semType_h_word,semType_t_word,tree.pos,position,voice,ch.semRole)):
							roles_5_dict[(semType_h_word,semType_t_word,tree.pos,position,voice,ch.semRole)] = roles_5_dict[(semType_h_word,semType_t_word,tree.pos,position,voice,ch.semRole)] + 1 
				else:
							roles_5_dict[(semType_h_word,semType_t_word,tree.pos,position,voice,ch.semRole)] =  1
				if total_5_dict.has_key((semType_h_word,semType_t_word,tree.pos,position,voice)):
							total_5_dict[(semType_h_word,semType_t_word,tree.pos,position,voice)] = total_5_dict[(semType_h_word,semType_t_word,tree.pos,position,voice)] + 1 
				else:
							total_5_dict[(semType_h_word,semType_t_word,tree.pos,position,voice)] =  1
				#model 4 
				if roles_4_dict.has_key((semType_t_word,t_word_pos,tree.pos,voice,ch.semRole)):
						roles_4_dict[(semType_t_word,t_word_pos,tree.pos,voice,ch.semRole)] = roles_4_dict[(semType_t_word,t_word_pos,tree.pos,voice,ch.semRole)] + 1 
				else:
						roles_4_dict[(semType_t_word,t_word_pos,tree.pos,voice,ch.semRole)] =  1
				if total_4_dict.has_key((semType_t_word,t_word_pos,tree.pos,voice)):
						total_4_dict[(semType_t_word,t_word_pos,tree.pos,voice)] = total_4_dict[(semType_t_word,t_word_pos,tree.pos,voice)] + 1 
				else:
						total_4_dict[(semType_t_word,t_word_pos,tree.pos,voice)] =  1
				#model 3
				if roles_3_dict.has_key((semType_t_word,t_word_pos,voice,ch.semRole)):
						roles_3_dict[(semType_t_word,t_word_pos,voice,ch.semRole)] = roles_3_dict[((semType_t_word,t_word_pos,voice,ch.semRole))] + 1
				else:
						roles_3_dict[(semType_t_word,t_word_pos,voice,ch.semRole)] = 1
				if total_3_dict.has_key((semType_t_word,t_word_pos,voice)):
						total_3_dict[(semType_t_word,t_word_pos,voice)] = total_3_dict[(semType_t_word,t_word_pos,voice)] + 1
				else:
						total_3_dict[(semType_t_word,t_word_pos,voice)] = 1
				#model 2
				if roles_2_dict.has_key((t_word_pos,tree.pos,position,voice,ch.semRole)):
						roles_2_dict[(t_word_pos,tree.pos,position,voice,ch.semRole)] = roles_2_dict[((t_word_pos,tree.pos,position,voice,ch.semRole))] + 1
				else:
						roles_2_dict[(t_word_pos,tree.pos,position,voice,ch.semRole)] = 1
				if total_2_dict.has_key((t_word_pos,tree.pos,position,voice)):
						total_2_dict[(t_word_pos,tree.pos,position,voice)] = total_2_dict[(t_word_pos,tree.pos,position,voice)] + 1
				else:
						total_2_dict[(t_word_pos,tree.pos,position,voice)] = 1
				# model 1
				if roles_1_dict.has_key((semType_t_word,ch.semRole)):
							roles_1_dict[((semType_t_word,ch.semRole))] = roles_1_dict[((semType_t_word,ch.semRole))] + 1 
				else:
							roles_1_dict[((semType_t_word,ch.semRole))] =  1
				if total_1_dict.has_key(((semType_t_word))):
							total_1_dict[(semType_t_word)] = total_1_dict[(semType_t_word)] + 1 
				else:
							total_1_dict[(semType_t_word)] =  1
				# legal role combination
				legal_roles.append(ch.semRole)
			else:
				h_found = 0
		legal_r_combination = '-'.join(legal_roles)
		if (tree.pos,legal_r_combination) not in legal_role_combination:
			legal_role_combination.append((tree.pos,legal_r_combination))
				#h_found=0
	for ch in tree.children:
		build_model(ch,e_hownet,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict,target_pos,idx,prep_pos,word2semType_dict,legal_role_combination,unique_roles,pp,model_maxent_file)
	return (roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict,legal_role_combination,unique_roles)


def output_model(roles_10,total_10,roles_9,total_9,roles_8,total_8,roles_7,total_7,roles_6,total_6,roles_5,total_5,roles_4,total_4,roles_3,total_3,roles_2,total_2,roles_1,total_1,legal_role_combination,unique_roles):
	not_found_ehownet = open('not-found-ehownet.txt','w')
	model_10_file = open("../models/model_10.txt",'w')
	model_9_file = open("../models/model_9.txt",'w')
	model_8_file = open("../models/model_8.txt",'w')
	model_7_file = open("../models/model_7.txt",'w')
	model_6_file = open("../models/model_6.txt",'w')
	model_5_file = open("../models/model_5.txt",'w')
	model_4_file = open("../models/model_4.txt",'w')
	model_3_file = open("../models/model_3.txt",'w')
	model_2_file = open("../models/model_2.txt",'w')
	model_1_file = open("../models/model_1.txt",'w')
	legal_roles_file = open("../temp/legal_roles.txt",'w')
	unq_role = open("unique_roles.txt",'w')
	model_temp_dict = {}
	max_count = 0
	for (semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType,role)	in roles_10.keys():
		new_prob = float(roles_10[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType,role)])/total_10[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType)]
		total_no = float(roles_10[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType,role)])
		if model_temp_dict.has_key((semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType)):
			old_roles = model_temp_dict[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType)] = old_roles
		else:
			model_temp_dict[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType)] = [(new_prob,role,total_no)]
	for (semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_h,pos_h,semType_t,pos_t,pt,position,all_pos,voice,left_right_child_pos,all_semType)],reverse=True)])
		model_10_file.write(str(semType_h)+','+str(pos_h)+','+str(semType_t)+','+str(pos_t)+','+str(pt)+','+str(position)+','+all_pos+','+voice+','+left_right_child_pos+','+all_semType+'='+str(all_roles)+'\n')
	
	# model 9
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (pos_h,semType_t,pos_t,pt,position,verb_pos,voice,role)	in roles_9.keys():
		new_prob = float(roles_9[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice,role)])/total_9[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice)]
		total_no = float(roles_9[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice,role)])
		if model_temp_dict.has_key((pos_h,semType_t,pos_t,pt,position,verb_pos,voice)):
			old_roles = model_temp_dict[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice)] = old_roles
		else:
			model_temp_dict[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice)] = [(new_prob,role,total_no)]
	for (pos_h,semType_t,pos_t,pt,position,verb_pos,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(pos_h,semType_t,pos_t,pt,position,verb_pos,voice)],reverse=True)])
		model_9_file.write(str(pos_h)+','+str(semType_t)+','+str(pos_t)+','+str(pt)+','+str(position)+','+verb_pos+','+voice+'='+str(all_roles)+'\n')
	'''
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	
	for (pos_h,semType_t,pos_t,pt,position,voice,role)	in roles_9.keys():
		new_prob = float(roles_9[(pos_h,semType_t,pos_t,pt,position,voice,role)])/total_9[(pos_h,semType_t,pos_t,pt,position,voice)]
		total_no = float(roles_9[(pos_h,semType_t,pos_t,pt,position,voice,role)])
		if model_temp_dict.has_key((pos_h,semType_t,pos_t,pt,position,voice)):
			old_roles = model_temp_dict[(pos_h,semType_t,pos_t,pt,position,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(pos_h,semType_t,pos_t,pt,position,voice)] = old_roles
		else:
			model_temp_dict[(pos_h,semType_t,pos_t,pt,position,voice)] = [(new_prob,role,total_no)]
	for (pos_h,semType_t,pos_t,pt,position,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(pos_h,semType_t,pos_t,pt,position,voice)],reverse=True)])
		model_9_file.write(str(pos_h)+','+str(semType_t)+','+str(pos_t)+','+str(pt)+','+str(position)+','+voice+'='+str(all_roles)+'\n')
	'''
	# model 8
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (semType_h,pos_h,pos_t,pt,position,voice,role)	in roles_8.keys():
		new_prob = float(roles_8[(semType_h,pos_h,pos_t,pt,position,voice,role)])/total_8[(semType_h,pos_h,pos_t,pt,position,voice)]
		total_no = float(roles_8[(semType_h,pos_h,pos_t,pt,position,voice,role)])
		if model_temp_dict.has_key((semType_h,pos_h,pos_t,pt,position,voice)):
			old_roles = model_temp_dict[(semType_h,pos_h,pos_t,pt,position,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_h,pos_h,pos_t,pt,position,voice)] = old_roles
		else:
			model_temp_dict[(semType_h,pos_h,pos_t,pt,position,voice)] = [(new_prob,role,total_no)]
	for (semType_h,pos_h,pos_t,pt,position,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_h,pos_h,pos_t,pt,position,voice)],reverse=True)])
		model_8_file.write(str(semType_h)+','+str(pos_h)+','+str(pos_t)+','+str(pt)+','+str(position)+','+voice+'='+str(all_roles)+'\n')
	# model 7	
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (semType_t,pos_t,pt,position,voice,role)	in roles_7.keys():
		new_prob = float(roles_7[(semType_t,pos_t,pt,position,voice,role)])/total_7[(semType_t,pos_t,pt,position,voice)]
		total_no = float(roles_7[(semType_t,pos_t,pt,position,voice,role)])
		if model_temp_dict.has_key((semType_t,pos_t,pt,position,voice)):
			old_roles = model_temp_dict[(semType_t,pos_t,pt,position,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_t,pos_t,pt,position,voice)] = old_roles
		else:
			model_temp_dict[(semType_t,pos_t,pt,position,voice)] = [(new_prob,role,total_no)]
	for (semType_t,pos_t,pt,position,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_t,pos_t,pt,position,voice)],reverse=True)])
		model_7_file.write(str(semType_t)+','+str(pos_t)+','+str(pt)+','+str(position)+','+voice+'='+str(all_roles)+'\n')
	# model 6	
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (h_pos,pos_t,pt,position,voice,role)	in roles_6.keys():
		new_prob = float(roles_6[(h_pos,pos_t,pt,position,voice,role)])/total_6[(h_pos,pos_t,pt,position,voice)]
		total_no = float(roles_6[(h_pos,pos_t,pt,position,voice,role)])
		if model_temp_dict.has_key((h_pos,pos_t,pt,position,voice)):
			old_roles = model_temp_dict[(h_pos,pos_t,pt,position,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(h_pos,pos_t,pt,position,voice)] = old_roles
		else:
			model_temp_dict[(h_pos,pos_t,pt,position,voice)] = [(new_prob,role,total_no)]
	for (h_pos,pos_t,pt,position,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(h_pos,pos_t,pt,position,voice)],reverse=True)])
		model_6_file.write(str(h_pos)+','+str(pos_t)+','+str(pt)+','+str(position)+','+voice+'='+str(all_roles )+'\n')
	
	# 5
	model_temp_dict = {}
	for (semType_h_word,semType_t_word,pt,position,voice,role)	in roles_5.keys():
		new_prob = float(roles_5[(semType_h_word,semType_t_word,pt,position,voice,role)])/total_5[(semType_h_word,semType_t_word,pt,position,voice)]
		total_no = float(roles_5[(semType_h_word,semType_t_word,pt,position,voice,role)])
		if model_temp_dict.has_key((semType_h_word,semType_t_word,pt,position,voice)):
			old_roles = model_temp_dict[(semType_h_word,semType_t_word,pt,position,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_h_word,semType_t_word,pt,position,voice)] = old_roles
		else:
			model_temp_dict[(semType_h_word,semType_t_word,pt,position,voice)] = [(new_prob,role,total_no)]
	for (semType_h_word,semType_t_word,pt,position,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_h_word,semType_t_word,pt,position,voice)],reverse=True)])
		model_5_file.write(str(semType_h_word)+','+str(semType_t_word)+','+pt+','+str(position)+','+voice+'='+str(all_roles)+'\n')
	
	# model 4	
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (semType_t,pos_t,pt,voice,role)	in roles_4.keys():
		new_prob = float(roles_4[(semType_t,pos_t,pt,voice,role)])/total_4[(semType_t,pos_t,pt,voice)]
		total_no = float(roles_4[(semType_t,pos_t,pt,voice,role)])
		if model_temp_dict.has_key((semType_t,pos_t,pt,voice)):
			old_roles = model_temp_dict[(semType_t,pos_t,pt,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_t,pos_t,pt,voice)] = old_roles
		else:
			model_temp_dict[(semType_t,pos_t,pt,voice)] = [(new_prob,role,total_no)]
	for (semType_t,pos_t,pt,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_t,pos_t,pt,voice)],reverse=True)])
		model_4_file.write(str(semType_t)+','+str(pos_t)+','+str(pt)+','+voice+'='+str(all_roles)+'\n')
	
	#model 3	
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (semType_t,pos_t,voice,role)	in roles_3.keys():
		new_prob = float(roles_3[(semType_t,pos_t,voice,role)])/total_3[(semType_t,pos_t,voice)]
		total_no = float(roles_3[(semType_t,pos_t,voice,role)])
		if model_temp_dict.has_key((semType_t,pos_t,voice)):
			old_roles = model_temp_dict[(semType_t,pos_t,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_t,pos_t,voice)] = old_roles
		else:
			model_temp_dict[(semType_t,pos_t,voice)] = [(new_prob,role,total_no)]
	for (semType_t,pos_t,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_t,pos_t,voice)],reverse=True)])
		model_3_file.write(str(semType_t)+','+str(pos_t)+','+voice+'='+str(all_roles)+'\n')
	#model 2	
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (pos_t,pt,position,voice,role)	in roles_2.keys():
		new_prob = float(roles_2[(pos_t,pt,position,voice,role)])/total_2[(pos_t,pt,position,voice)]
		total_no = float(roles_2[(pos_t,pt,position,voice,role)])
		if model_temp_dict.has_key((pos_t,pt,position,voice)):
			old_roles = model_temp_dict[(pos_t,pt,position,voice)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(pos_t,pt,position,voice)] = old_roles
		else:
			model_temp_dict[(pos_t,pt,position,voice)] = [(new_prob,role,total_no)]
	for (pos_t,pt,position,voice) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(pos_t,pt,position,voice)],reverse=True)])
		model_2_file.write(str(pos_t)+','+str(pt)+','+str(position)+','+voice+'='+str(all_roles)+'\n')
	
	#model 1	
	model_temp_dict = {}
	total_no = 0
	old_total_no = 0
	for (semType_t_word,role)	in roles_1.keys():
		new_prob = float(roles_1[(semType_t_word,role)])/total_1[(semType_t_word)]
		total_no = float(roles_1[(semType_t_word,role)])
		if model_temp_dict.has_key((semType_t_word)):
			old_roles = model_temp_dict[(semType_t_word)]
			old_roles.append((new_prob,role,total_no))
			model_temp_dict[(semType_t_word)] = old_roles
		else:
			model_temp_dict[(semType_t_word)] = [(new_prob,role,total_no)]
	for (semType_t_word) in model_temp_dict.keys():
		all_roles = '|'.join([str(t) for t in sorted(model_temp_dict[(semType_t_word)],reverse=True)])
		model_1_file.write(str(semType_t_word)+'='+str(all_roles)+'\n')
	
	# legal roles
	for (pt,roles) in legal_role_combination:
		legal_roles_file.write(str(pt)+':'+roles+'\n')
	#unique roles
	for r in unique_roles:
		unq_role.write(str(r)+'\n')

def model():
	training_data = make_training_data()
	e_hownet=EHowNetTree("../data/ehownet_ontology.txt")
	target_pos = get_target_pos()
	pp = get_pp()
	word2semType_dict = word2semType()
	prep_pos = open('../data/tpos.txt').readlines()[2].rstrip().split(',') 
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
	legal_role_combination = []
	unique_roles = []
	model_maxent_file = open("../models/train.dat",'w')
	for tree in training_data:
	 #voice = isPassive(tree,pp,'False')
	 (roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict,legal_role_combination,unique_roles) = build_model(tree,e_hownet,roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict,target_pos,training_data.index(tree),prep_pos,word2semType_dict,legal_role_combination,unique_roles,pp,model_maxent_file) # model 1
	output_model(roles_10_dict,total_10_dict,roles_9_dict,total_9_dict,roles_8_dict,total_8_dict,roles_7_dict,total_7_dict,roles_6_dict,total_6_dict,roles_5_dict,total_5_dict,roles_4_dict,total_4_dict,roles_3_dict,total_3_dict,roles_2_dict,total_2_dict,roles_1_dict,total_1_dict,legal_role_combination,unique_roles)
	
if __name__ == "__main__":
 import sys
 try:
	model()
 except:
	print >>sys.stderr, __doc__
	raise