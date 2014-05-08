from itertools import *
from ehownet import *
from auxiliaryFunsFullFeatures import *
from parseTree import *

def assign_roles(tree,e_hownet,feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles,target_pos,passive,prep_pos,dummy,word2semType_dict,pp,feature_file):
	#print "inside srl" + str(tree.data)
	if tree != None:
	 if tree.children != []:		
		(h_word,h_pos) = find_h_word(tree)
		print h_word
		print h_pos
		semType_h_word = find_semType(h_word,h_pos,e_hownet,word2semType_dict)
		h_found=1
		all_roles = []
		for ch in tree.children:
			if ch.semRole != 'Head' and ch.semRole != 'head':
				#print ch.word
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
				if verb_pos_all != []:
					verb_pos = verb_pos_all[0]
				else:
					verb_pos = 'no-verb-pos'
				if h_found==1:
					position=-1
				else:
					position=1
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
			
				old_role = ch.semRole
				#print 'semType_h_word='+semType_h_word+' h_pos='+h_pos+' semType_t_word='+semType_t_word+' t_word_pos='+t_word_pos+' pt='+pt+' pt_of_parent='+pt_of_parent+' position='+str(position)+' l_sib_pt='+l_sib_pt+' r_sib_pt='+r_sib_pt+' voice='+voice+' first_word_semType='+first_word_semType+' last_word_semType='+last_word_semType+' f_w_semType_pls_l_w_semType='+first_word_semType+last_word_semType+' subcatAt='+subcatAt+' subcatStar='+subcatStar+' path_to_BA='+str(path_to_BA)+' ?'
				feature_file.write('semType_h_word='+semType_h_word+' h_pos='+h_pos+' semType_t_word='+semType_t_word+' t_word_pos='+t_word_pos+' pt='+pt+' pt_of_parent='+pt_of_parent+' position='+str(position)+' l_sib_pt='+l_sib_pt+' r_sib_pt='+r_sib_pt+' voice='+voice+' first_word_semType='+first_word_semType+' last_word_semType='+last_word_semType+' f_w_semType_pls_l_w_semType='+first_word_semType+last_word_semType+' subcatAt='+subcatAt+' subcatStar='+subcatStar+' path_to_BA='+str(path_to_BA)+' ?'+'\n')
				(p,n,sRole,m,roles) = findRole((semType_h_word,h_pos,semType_t_word,t_word_pos,tree.pos,str(position),all_pos,verb_pos,passive,left_right_child_pos,all_semType),feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,target_pos,prep_pos)	
				# to correct some of mistakes made by statistical models
				if sRole == 'DUMMY2' and dummy == 0:
						sRole = 'DUMMY1'
						dummy = dummy + 1
				elif sRole == 'DUMMY1' and dummy == 1:
						sRole = 'DUMMY2'
						dummy = dummy + 1
				elif sRole in ['DUMMY','DUMMy','DUMMY1','DUMMY2']:
						dummy = dummy + 1
				if sRole == 'property' and (m == '4b' or m == '5b' or m == 'baseline2') and p < 0.62:
						if semType_t_word in ['human','speaker','husband','self','3rdPerson','private']:
							if len(roles) > 1:
								(next_p,next_n,next_r) = roles[1]
								sRole = next_r
				elif sRole == 'possessor' and semType_t_word in ['human','speaker','husband','self','3rdPerson','private'] and (m == '5') and p == 0.5:
						if ch.pos == prep_pos[4]:
							if len(roles) > 1:
								(next_p,next_n,next_r) = roles[1]
								sRole = next_r
				elif sRole == 'goal' and (m == '4b' or m == '5b' or m == 'baseline2' or m == '5' or m == '3' or m == 'baseline' or m == 'baseline3') and p < 0.6:
						if semType_t_word in ['human','speaker','husband','self','3rdPerson','private','humanized','NameValue']:
							if len(roles) > 1:
								(next_p,next_n,next_r) = roles[1]
								sRole = next_r
				elif sRole == 'theme' and (m == '4b' or m == '5b' or m == 'baseline2' or m == '5' or m == '3' or m == 'baseline' or m == 'baseline3') and p < 0.62:
						if semType_t_word in ['human','speaker','husband','self','3rdPerson','private','humanized','NameValue','organization','machine','community']:
							if len(roles) > 1:
								(next_p,next_n,next_r) = roles[1]
								sRole = next_r			
				elif sRole == 'experiencer' and (m == '4b' or m == '5b' or m == 'baseline2' or m == '5' or m == '3' or m == 'baseline' or m == 'baseline3') and p < 0.62:
						if semType_t_word in ['human','speaker','husband','self','3rdPerson','private','humanized','NameValue','organization','machine','community']:
							if len(roles) > 1:
								(next_p,next_n,next_r) = roles[1]
								sRole = next_r
				elif ch.pos in prep_pos: 
					(t_t_word,tg_t_pos) = find_t_word(ch,prep_pos,'','')
					if tg_t_pos in ['VH11','VH12','VH13','VH14','VH15','VH16','VH17','VH21','VH22'] and sRole == 'predication':
						sRole = 'property'
				elif sRole in ['time']:
					(t_t_word,tg_t_pos) = find_t_word(ch,prep_pos,'','')
					if tg_t_pos in ['Nca','Ncb','Ncc','Ncda','Ncda','Ncdb','Dg']:
						sRole = 'location'
					elif tg_t_pos in ['Daa','Dab']:
						sRole = 'quantity'
					elif tg_t_pos in ['Dh']:
						sRole = 'manner'
				elif sRole in ['location','agent','quantity','manner']:
					(t_t_word,tg_t_pos) = find_t_word(ch,prep_pos,'','')
					if tg_t_pos in ['Ndaaa','Ndaab','Ndaac','Ndaad','Ndaba','Ndabb','Ndabc','Ndabd','Ndabe','Ndabf','Ndc','Ndca','Ndcb','Ndcc','Dd']:
						sRole = 'time'
				
				ch.semRole = sRole
				all_roles.append((sRole,roles))
							
			else:
				h_found=0		
		roles_combination = str(tree.pos)+':'+'-'.join([r for (r,all) in all_roles if r != None]) # error check why r is None for some trees
		validate_roles2(tree,all_roles,legal_roles,roles_combination)
		#validate_property_possessor(tree,prep_pos)					
	for ch in tree.children:
		dummy = 0
		assign_roles(ch,e_hownet,feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles,target_pos,passive,prep_pos,dummy,word2semType_dict,pp,feature_file)
	return tree

def validate_roles2(tree,all_roles,legal_roles,roles_combination):
	if len(all_roles) > 1:
	  f = 0
	  ch_idx = []
	  for ch in tree.children:
			if ch.semRole != 'Head' and ch.semRole != 'head':
				ch_idx.append(tree.children.index(ch)) 
	  role_idx = []
	  roles = [r for (r,rls) in all_roles]
	  for r in roles:
		role_idx = duplicates(roles,r)
		if len(role_idx) > 1:
		 if roles[role_idx[0]] not in ['predication', 'possessor', 'topic', 'deontics', 'manner', 'aspect', 'alternative', 'result', 'addition', 'negation', 'nominal', 'location', 'evaluation', 'interjection', 'apposition', 'DUMMY', 'degree', 'complement', 'benefactor', 'reason', 'hypothesis', 'quantifier', 'condition', 'property', 'target', 'particle', 'contrast', 'time', 'DUMMY2', 'DUMMY1', 'epistemics', 'quantity']:#['property','time','manner','quantifier','deontics','epistemics','quantity','complement','particle']:
			#print role_idx
			#print roles
			(ch1_role,ch1_all_roles) = all_roles[role_idx[0]]
			(ch2_role,ch2_all_roles) = all_roles[role_idx[1]]
			if len(ch1_all_roles) > 1 and len(ch2_all_roles) == 1:
				(p,n,r) = ch1_all_roles[1]
				tree.children[ch_idx[role_idx[0]]].semRole = r
			elif len(ch1_all_roles) == 1 and len(ch2_all_roles) > 1:
				(p,n,r) = ch2_all_roles[1]
				tree.children[ch_idx[role_idx[1]]].semRole = r
			elif len(ch1_all_roles) > 1 and len(ch2_all_roles) > 1:
				(p0,n0,r0) = ch1_all_roles[1]
				(p,n,r) = ch2_all_roles[1]
				if p0 >= p:
					#print r0
					tree.children[ch_idx[role_idx[0]]].semRole = r0
				else:
					tree.children[ch_idx[role_idx[1]]].semRole = r
	  
   
def findRole((semType_h_word,h_pos,semType_t_word,t_pos,pt,position,all_pos,verb_pos,passive,left_right_child_pos,all_semType),feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,target_pos,prep_pos):

	potential_roles = []
	if feature_role_dict_10.has_key((semType_h_word,h_pos,semType_t_word,t_pos,pt,position,all_pos,passive,left_right_child_pos,all_semType)):
		probs_roles = feature_role_dict_10[(semType_h_word,h_pos,semType_t_word,t_pos,pt,position,all_pos,passive,left_right_child_pos,all_semType)]
		probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
		(p1,n1,r1) = probs_roles[0]
		potential_roles.append((float(p1)*0.9,n1,r1,'8',probs_roles)) # 1.0
	if feature_role_dict_9.has_key((h_pos,semType_t_word,t_pos,pt,position,verb_pos,passive)):
			probs_roles = feature_role_dict_9[(h_pos,semType_t_word,t_pos,pt,position,verb_pos,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p2,n2,r2) = probs_roles[0]	
			potential_roles.append((float(p2)*1.0,n2,r2,'9',probs_roles)) # 0.9
	'''if feature_role_dict_9.has_key((h_pos,semType_t_word,t_pos,pt,position,verb_pos,passive)):
			probs_roles = feature_role_dict_9[(h_pos,semType_t_word,t_pos,pt,position,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p2,n2,r2) = probs_roles[0]	
			potential_roles.append((float(p2)*1.0,n2,r2,'5',probs_roles)) # 0.9'''
	if feature_role_dict_8.has_key((semType_h_word,h_pos,t_pos,pt,position,passive)):
			probs_roles = feature_role_dict_8[(semType_h_word,h_pos,t_pos,pt,position,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p3,n3,r3) = probs_roles[0]
			potential_roles.append((float(p3)*0.9,n3,r3,'5b',probs_roles)) # 0.7
	if feature_role_dict_7.has_key((semType_t_word,t_pos,pt,position,passive)):
			probs_roles = feature_role_dict_7[(semType_t_word,t_pos,pt,position,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p4,n4,r4) = probs_roles[0]
			potential_roles.append((float(p4)*0.7,n4,r4,'4',probs_roles)) # 0.7
	if feature_role_dict_6.has_key((h_pos,t_pos,pt,position,passive)):
			probs_roles = feature_role_dict_6[(h_pos,t_pos,pt,position,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p5,n5,r5) = probs_roles[0]
			potential_roles.append((float(p5)*0.8,n5,r5,'4b',probs_roles)) #0.8
	if feature_role_dict_5.has_key((semType_h_word,semType_t_word,pt,position,passive)):# and t_pos.decode('Big5',errors='ignore').encode('utf_8') == target_pos:
			probs_roles = feature_role_dict_5[(semType_h_word,semType_t_word,pt,position,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p0,n0,r0) = probs_roles[0]
			potential_roles.append((float(p0)*0.4,n0,r0,'4c',probs_roles)) #0.4
	if feature_role_dict_4.has_key((semType_t_word,t_pos,pt,passive)):
			probs_roles = feature_role_dict_4[(semType_t_word,t_pos,pt,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p6,n6,r6) = probs_roles[0]
			potential_roles.append((float(p6)*0.5,n6,r6,'3',probs_roles)) # 0.5
	if feature_role_dict_3.has_key((semType_t_word,t_pos,passive)):
			probs_roles = feature_role_dict_3[(semType_t_word,t_pos,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p7,n7,r7) = probs_roles[0]
			potential_roles.append((float(p7)*0.4,n7,r7,'4',probs_roles)) # 0.4
	if feature_role_dict_2.has_key((t_pos,pt,position,passive)):
			probs_roles = feature_role_dict_2[(t_pos,pt,position,passive)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p8,n8,r8) = probs_roles[0]
			potential_roles.append((float(p8)*0.5,n8,r8,'baseline2',probs_roles)) # 0.5
	if feature_role_dict_1.has_key((semType_t_word)):
			probs_roles = feature_role_dict_1[(semType_t_word)]
			probs_roles =  disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_4,prep_pos)
			(p9,n9,r9) = probs_roles[0]
			potential_roles.append((float(p9)*0.4,n9,r9,'baseline3',probs_roles)) # 0.5
	if potential_roles != []:
		return sorted(potential_roles,reverse=True)[0]
	else:
		return (0,0,None,0,[])



def disambiguate_equals(probs_roles,semType_t_word,t_pos,passive,feature_role_dict_baseline,prep_pos):
	if len(probs_roles) > 1:
				(p1,n1,r1) = probs_roles[0]
				(p2,n2,r2) = probs_roles[1]
				if p1 == p2:
					if r1 == 'property' and r2 == 'predication' and t_pos in prep_pos[0:3]:		
						(p_t,n_t,r_t) = probs_roles[0]
						probs_roles[0] = probs_roles[1]
						probs_roles[1] = (p_t,n_t,r_t)
					elif  feature_role_dict_baseline.has_key((semType_t_word,t_pos,passive)):
						p_r1 = ''
						p_r2 = ''
						for (p_r,n_r,r_r) in  feature_role_dict_baseline[(semType_t_word,t_pos,passive)]:
							if r_r == r1:
								p_r1 = p_r
								break
						for (p_r,n_r,r_r) in  feature_role_dict_baseline[(semType_t_word,t_pos,passive)]:
							if r_r == r2:
								p_r2 = p_r
								break
						if p_r2 > p_r1 and p_r1 != '' and p_r2 != '':
							(p_t,n_t,r_t) = probs_roles[0]
							probs_roles[0] = probs_roles[1]
							probs_roles[1] = (p_t,n_t,r_t)
	return probs_roles
def read_model():
	model_10_file = open("../models/model_10.txt")
	model_9_file = open("../models/model_9.txt")
	model_8_file = open("../models/model_8.txt")
	model_7_file = open("../models/model_7.txt")
	model_6_file = open("../models/model_6.txt")
	model_5_file = open("../models/model_5.txt")
	model_4_file = open("../models/model_4.txt")
	model_3_file = open("../models/model_3.txt")
	model_2_file = open("../models/model_2.txt")
	model_1_file = open("../models/model_1.txt")
	legal_roles_file = open("../temp/legal_roles.txt")
	features = []
	prob_role = []
	feature_role_dict_10 = {}
	for line in model_10_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7],tokens[8],tokens[9])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_10[f] = role_prob
	#model 9
	feature_role_dict_9 = {}
	for line in model_9_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_9[f] = role_prob
	#model 8
	feature_role_dict_8 = {}
	for line in model_8_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_8[f] = role_prob
	#model 7
	feature_role_dict_7 = {}
	for line in model_7_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3],tokens[4])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_7[f] = role_prob
	#model 6
	feature_role_dict_6 = {}
	for line in model_6_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3],tokens[4])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_6[f] = role_prob
	#model 5
	feature_role_dict_5 = {}
	for line in model_5_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3],tokens[4])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_5[f] = role_prob
	#model 4
	feature_role_dict_4 = {}
	for line in model_4_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_4[f] = role_prob
	#3
	feature_role_dict_3 = {}
	for line in model_3_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_3[f] = role_prob
	#2
	feature_role_dict_2 = {}
	for line in model_2_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0],tokens[1],tokens[2],tokens[3])
		role_prob = []
		for role in roles.split('|'):
			#print role
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_2[f] = role_prob
	
	#model 1
	feature_role_dict_1 = {}
	for line in model_1_file.readlines():
		features = line.rstrip().split('=')[0]
		roles = line.rstrip().split('=')[1]
		tokens = features.split(',')
		f = (tokens[0])
		role_prob = []
		for role in roles.split('|'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		feature_role_dict_1[f] = role_prob
	#legal roles
	legal_roles = []
	for line in legal_roles_file.readlines():
		legal_roles.append(line.rstrip())
		
	return (feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles)	
#############
# for already annotates trees
def make_testing_data():
	exprs = open("..//CoNLL2006-2007/10-fold-data/10-fold-data.txt")
	testing_trees = []
	for expr in exprs.readlines():
			tre = parseExpr(expr.rstrip())
			testing_trees.append(tre)
	return testing_trees 
	
def test_data():
	exprs = open("..//CoNLL2006-2007/10-fold-data/10-fold-data.txt")
	return exprs.readlines()
 	
def role_labeler():
	print 'Making test data.....'
	testing_data = make_testing_data()
	test_trees = test_data()
	print 'Loading ehownet.....'
	e_hownet=EHowNetTree("ehownet_ontology.txt")
	#new_trees = []
	#(features,prob_role,features_5,prob_role_5,features_baseline,prob_role_baseline) = read_model()
	print 'reading model.......'
	(feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles) = read_model()
	total = 0
	correct = 0
	old_semRoles = []
	new_semRoles = []
	target_pos = get_target_pos()
	pp = get_pp()
	word2semType_dict = word2semType()
	prep_pos = open('./data/tpos.txt').readlines()[2].rstrip().split(',') 
	print 'Assigning roles....'
	for tree in testing_data:
	 dummy = 0
	 old_semRoles = tree_semRoles(tree,old_semRoles)
	 passive = isPassive(tree,pp,'False')
	 new_tree = assign_roles(tree,e_hownet,feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles,target_pos,testing_data.index(tree),passive,prep_pos,dummy,word2semType_dict,test_trees)
	 new_semRoles = tree_semRoles(new_tree,new_semRoles)
	for i in range(len(old_semRoles)):
		if str(old_semRoles[i]) == str(new_semRoles[i]):
			correct = correct + 1
	errors = [(x,y) for (x,y) in zip(old_semRoles[0:],new_semRoles[0:]) if str(x) != str(y)]
	grouped = [list(g) for k, g in groupby(sorted(errors))]
	b = sorted(grouped, key = len)
	print 'Accuracy: ' + str(float(correct)/len(old_semRoles))
	
def tree_semRoles(t,semRoles):
	if t.semRole != 'Head' and t.semRole != 'head':
		semRoles.append(t.semRole)
	for c in t.children:
		tree_semRoles(c,semRoles)
	return semRoles
	
def compare_trees(old,new,correct,total):
	if old.semRole == new.semRole:
		correct = correct + 1
	total = total + 1
	children = new.children
	for ch in range(0,len(children)):
		compare_trees(old.children[ch],new.children[ch],correct,total)
	return (correct,total)
##################################
# take un-annotated trees from a file './test/in.txt' and store result into a file './test/out.txt'
def srl():
	#output file
	out = open('./test/out.txt','w')
	# make test data
	data = open('./test/in.txt')
	# load e-hownet
	print 'Loading E-HowNet...'
	e_hownet=EHowNetTree("ehownet_ontology.txt")
	#read models and other features
	print 'Reading Models...'
	(feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles) = read_model()
	target_pos = get_target_pos()
	pp = get_pp()
	word2semType_dict = word2semType()
	prep_pos = open('./data/tpos.txt').readlines()[2].rstrip().split(',') 
	print 'Assigning Roles...'
	for expr in data.readlines():
		expr_prefix = expr.split(' ')[0]
		expr_postfix = expr.split('#')[-1]
		clean_expr = (''.join(expr.split(' ')[1:])).split('#')[0]
		tree = parseExpr_unannotated(clean_expr.rstrip())
		#print_tree(tree)
		dummy = 0
		passive = isPassive(tree,pp,'False')
		annotated_tree = assign_roles(tree,e_hownet,feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles,target_pos,passive,prep_pos,dummy,word2semType_dict)
		annotated_tree_line = print_tree_line(annotated_tree,[])
		out.write(expr_prefix+' ' + ''.join(annotated_tree_line)+'#'+expr_postfix)
	print 'Done!'
	
###################################
if __name__ == "__main__":
 import sys
 try:
	#role_labeler()
	srl()
 except:
	print >>sys.stderr, __doc__
	raise