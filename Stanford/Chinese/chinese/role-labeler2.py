from prepareData import *
from buildModelAuxiliaries2 import *
from auxiliaryFuns import *
from ehownet import *
import os

def assign_roles(feature_role_25_dict,feature_role_24_dict,feature_role_23_dict,feature_role_22_dict,feature_role_21_dict,feature_role_20_dict,feature_role_19_dict,feature_role_18_dict,feature_role_17_dict,feature_role_16_dict,feature_role_15_dict,feature_role_14_dict,feature_role_13_dict,feature_role_12_dict,feature_role_11_dict,feature_role_10_dict,feature_role_9_dict,feature_role_8_dict,feature_role_7_dict,feature_role_6_dict,feature_role_5_dict,feature_role_4_dict,feature_role_3_dict,feature_role_2_dict,feature_role_1_dict,tree_head_dict,simplified_tradictional_dict):
	word2semType_dict = word2semType()
	e_hownet=EHowNetTree("ehownet_ontology.txt")
	frameset_file_dict = frameset_dict()
	#prop_bank = open('cpb1.0.txt').readlines()
	prop_bank = open('propbank.test').readlines()
	#for prop in prop_bank[:9351]:
	old_roles = []
	new_roles = []
	f_c = find_best_fc2()
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
		for arg in args:
			label = '-'.join(arg.split('-')[1:])
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
				(t_word,t_word_pos,h_word,h_word_pos,position,pt,gov,all_words,p,path_to_BA,path_to_BEI,voice,subcatStar,subcatAt,l_sib_pt,r_sib_pt,voice_position,layer_cons_focus) = find_features_without_traces(nh_pairs,parsed,predicate,target,target_POS,tree_head_dict,prop)
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
				###############################
				
				
				#print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' '+label.rstrip()
				#print 't_word='+str(t_word)+' t_word_pos='+str(t_word_pos)+' h_word='+str(h_word)+' h_word_pos='+str(h_word_pos)+' position='+str(position)+' pt='+str(pt)+' gov='+str(gov.rstrip())+' t_word_plus_pt='+str(t_word_plus_pt)+ ' t_word_plus_h_word='+str(t_word+h_word)+' first_word='+first_word+ ' last_word='+last_word+' voice='+str(voice)+' subcat='+str(subcat)+' subcatStar='+str(subcatStar)+' subcatAt='+str(subcatAt)+' path='+str(p)+' path_to_BA='+str(path_to_BA)+' path_to_BEI='+str(path_to_BEI)+' verb_calss='+str(verb_class)+' verb_class_plus_pt='+(verb_class+pt)+ ' verb_class_plus_h_word='+str(verb_class+h_word)+' l_sib_pt='+str(l_sib_pt)+ ' r_sib_pt='+str(r_sib_pt)+ ' allFrameSets='+str(AllFrameSets)+ ' verb_class_plus_allFrameSets='+str(verb_class+AllFrameSets)+' ?'
				#print str(t_word)+','+str(t_word_pos)+','+str(h_word)+','+str(h_word_pos)+','+str(position)+','+str(pt)+','+str(gov.rstrip())+','+str(t_word_plus_pt)+ ','+str(t_word+h_word)+','+first_word+ ','+last_word+','+str(voice)+','+str(subcat.rstrip())+','+str(subcatStar.rstrip())+','+str(subcatAt.rstrip())+','+str(p)+','+str(path_to_BA)+','+str(path_to_BEI)+','+str(verb_class)+','+(verb_class+pt)+ ','+str(verb_class+h_word)+','+str(l_sib_pt)+ ','+str(r_sib_pt)+ ','+str(AllFrameSets)+ ','+str(verb_class+AllFrameSets)+','+ str(voice_position) + ',' + label.rstrip()
				all_features = [str(t_word),str(t_word_pos),str(h_word),str(h_word_pos),str(position),str(pt),str(gov.rstrip()),str(t_word_plus_pt),str(t_word+h_word),first_word,last_word,str(voice),str(subcat.rstrip()),str(subcatStar.rstrip()),str(subcatAt.rstrip()),str(p),str(path_to_BA),str(path_to_BEI),str(verb_class),(verb_class+pt),str(verb_class+h_word),str(l_sib_pt),str(r_sib_pt),str(AllFrameSets),str(verb_class+AllFrameSets),label.rstrip()]
				#print str(t_word)+','+str(t_word_pos)+','+str(h_word)+','+str(h_word_pos)+','+str(position)+','+str(pt)+','+str(gov.rstrip())+','+str(t_word_plus_pt)+','+first_word+','+last_word+','+label.rstrip()
				(p,n,sRole,m,roles) = findRole(all_features,f_c,feature_role_25_dict,feature_role_24_dict,feature_role_23_dict,feature_role_22_dict,feature_role_21_dict,feature_role_20_dict,feature_role_19_dict,feature_role_18_dict,feature_role_17_dict,feature_role_16_dict,feature_role_15_dict,feature_role_14_dict,feature_role_13_dict,feature_role_12_dict,feature_role_11_dict,feature_role_10_dict,feature_role_9_dict,feature_role_8_dict,feature_role_7_dict,feature_role_6_dict,feature_role_5_dict,feature_role_4_dict,feature_role_3_dict,feature_role_2_dict,feature_role_1_dict)
				old_roles.append(label.rstrip())
				new_roles.append(sRole)
				#all_roles_of_tree.append((sRole,roles))
				
				#if label.rstrip() != sRole: #== 'ARG1' and sRole == 'ARG0':
					#print str(position) + ' ' + str(voice)
				print label.rstrip() + ' ' +  str(sRole) + ' ' + str(roles)
				###############################
		#validated_roles = validate_roles(all_roles_of_tree)
		#new_roles = new_roles + validated_roles
	return (old_roles,new_roles)
def validate_roles(all_roles):
	role_idx = [all_roles.index((r,rs)) for (r,rs) in all_roles if r == 'ARG1']
	if len(role_idx) > 1:		
			(ch1_role,ch1_all_roles) = all_roles[role_idx[0]]
			(ch2_role,ch2_all_roles) = all_roles[role_idx[1]]
			if len(ch1_all_roles) > 1 and len(ch2_all_roles) == 1:
				(p,n,r) = ch1_all_roles[1]
				all_roles[role_idx[0]] = (r,ch1_all_roles)
			elif len(ch1_all_roles) == 1 and len(ch2_all_roles) > 1:
				(p,n,r) = ch2_all_roles[1]
				all_roles[role_idx[1]] = (r,ch2_all_roles)
			elif len(ch1_all_roles) > 1 and len(ch2_all_roles) > 1:
				(p0,n0,r0) = ch1_all_roles[1]
				(p,n,r) = ch2_all_roles[1]
				if p0 >= p:
					#print r0
					all_roles[role_idx[0]] = (r0,ch1_all_roles)
				else:
					all_roles[role_idx[1]] = (r,ch2_all_roles)
					
			return [r for (r,rs) in all_roles]
	else:
		return [r for (r,rs) in all_roles]
def findRole(all_features,f_c,feature_role_25_dict,feature_role_24_dict,feature_role_23_dict,feature_role_22_dict,feature_role_21_dict,feature_role_20_dict,feature_role_19_dict,feature_role_18_dict,feature_role_17_dict,feature_role_16_dict,feature_role_15_dict,feature_role_14_dict,feature_role_13_dict,feature_role_12_dict,feature_role_11_dict,feature_role_10_dict,feature_role_9_dict,feature_role_8_dict,feature_role_7_dict,feature_role_6_dict,feature_role_5_dict,feature_role_4_dict,feature_role_3_dict,feature_role_2_dict,feature_role_1_dict):
	#print t_word_pos+','+h_word_pos+','+str(position)+','+pt+','+gov
	potential_roles = []
	potential_roles_GA = []
	probs_roles = []
	(p,n,r) = (0,0,0)
	#ws = [1.0,0.95,0.9,0.1,0.8,0.7,0.8,0.8,0.8,0.8,0.8,0.2,0.5,0.1,0.1,0.1,0.1,0.1,0.4,0.7,0.6,0.7,0.6,0.1,0.2]
	#ws = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
	ws = [0.3,0.27,0.21,0.12,0.66,0.15,0.06,0.54,0.63,0.51,0.45,0.33,0.03,0.69,0.72,0.24,0.09,0.36,0.48,0.57,0.6,0.18,0.42,0.39,0.75]
	#ws = [0.15,0.21,0.69,0.33,0.63,0.45,0.09,0.15,0.54,0.06,0.48,0.27,0.72,0.45,0.5,0.51,0.06,0.57,0.39,0.18,0.41,0.46,0.24,0.33,0.55]
	threshold = 0.0
	fc24 = ','.join([all_features[i] for i in f_c[1]])
	fc23 = ','.join([all_features[i] for i in f_c[2]])
	fc22 = ','.join([all_features[i] for i in f_c[3]])
	fc25 = ','.join([all_features[i] for i in f_c[0]])
	fc21 = ','.join([all_features[i] for i in f_c[4]])
	fc20 = ','.join([all_features[i] for i in f_c[5]])
	fc19 = ','.join([all_features[i] for i in f_c[6]])
	fc18 = ','.join([all_features[i] for i in f_c[7]])
	fc17 = ','.join([all_features[i] for i in f_c[8]])
	fc16 = ','.join([all_features[i] for i in f_c[9]])
	fc15 = ','.join([all_features[i] for i in f_c[10]])
	fc14 = ','.join([all_features[i] for i in f_c[11]])
	fc13 = ','.join([all_features[i] for i in f_c[12]])
	fc12 = ','.join([all_features[i] for i in f_c[13]])
	fc11 = ','.join([all_features[i] for i in f_c[14]])
	fc10 = ','.join([all_features[i] for i in f_c[15]])
	fc9 = ','.join([all_features[i] for i in f_c[16]])
	fc8 = ','.join([all_features[i] for i in f_c[17]])
	fc7 = ','.join([all_features[i] for i in f_c[18]])
	fc6 = ','.join([all_features[i] for i in f_c[19]])
	fc5 = ','.join([all_features[i] for i in f_c[20]])
	fc4 = ','.join([all_features[i] for i in f_c[21]])
	fc3 = ','.join([all_features[i] for i in f_c[22]])
	fc2 = ','.join([all_features[i] for i in f_c[23]])
	fc1 = ','.join([all_features[i] for i in f_c[24]])
	
	if feature_role_25_dict.has_key(fc25):
		probs_roles = feature_role_25_dict[fc25]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold: 
			#print n
			potential_roles.append((float(p)*ws[0],n,r,'25',probs_roles)) # 1.0
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc24 = ','.join([all_features[i] for i in f_c[1]])
	if feature_role_24_dict.has_key(fc24):
		probs_roles = feature_role_24_dict[fc24]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[1],n,r,'24',probs_roles))
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc23 = ','.join([all_features[i] for i in f_c[2]])
	if feature_role_23_dict.has_key(fc23):
		probs_roles = feature_role_23_dict[fc23]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[2],n,r,'23',probs_roles))
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc22 = ','.join([all_features[i] for i in f_c[3]])
	if feature_role_22_dict.has_key(fc22):
		probs_roles = feature_role_22_dict[fc22]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[3],n,r,'22',probs_roles))
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc21 = ','.join([all_features[i] for i in f_c[4]])
	if feature_role_21_dict.has_key(fc21):
		probs_roles = feature_role_21_dict[fc21]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[4],n,r,'21',probs_roles))
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc20 = ','.join([all_features[i] for i in f_c[5]])
	if feature_role_20_dict.has_key(fc20):
		probs_roles = feature_role_20_dict[fc20]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[5],n,r,'20',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc19 = ','.join([all_features[i] for i in f_c[6]])
	if feature_role_19_dict.has_key(fc19):
		probs_roles = feature_role_19_dict[fc19]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[6],n,r,'19',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc18 = ','.join([all_features[i] for i in f_c[7]])
	if feature_role_18_dict.has_key(fc18):
		probs_roles = feature_role_18_dict[fc18]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[7],n,r,'18',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc17 = ','.join([all_features[i] for i in f_c[8]])
	if feature_role_17_dict.has_key(fc17):
		probs_roles = feature_role_17_dict[fc17]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[8],n,r,'17',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc16 = ','.join([all_features[i] for i in f_c[9]])
	if feature_role_16_dict.has_key(fc16):
		probs_roles = feature_role_16_dict[fc16]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[9],n,r,'16',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc15 = ','.join([all_features[i] for i in f_c[10]])
	if feature_role_15_dict.has_key(fc15):
		probs_roles = feature_role_15_dict[fc15]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[10],n,r,'15',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc14 = ','.join([all_features[i] for i in f_c[11]])
	if feature_role_14_dict.has_key(fc14):
		probs_roles = feature_role_14_dict[fc14]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[11],n,r,'14',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc13 = ','.join([all_features[i] for i in f_c[12]])
	if feature_role_13_dict.has_key(fc13):
		probs_roles = feature_role_13_dict[fc13]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[12],n,r,'13',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc12 = ','.join([all_features[i] for i in f_c[13]])
	if feature_role_12_dict.has_key(fc12):
		probs_roles = feature_role_12_dict[fc12]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[13],n,r,'12',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc11 = ','.join([all_features[i] for i in f_c[14]])
	if feature_role_11_dict.has_key(fc11):
		probs_roles = feature_role_11_dict[fc11]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[14],n,r,'11',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc10 = ','.join([all_features[i] for i in f_c[15]])
	if feature_role_10_dict.has_key(fc10):
		probs_roles = feature_role_10_dict[fc10]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[15],n,r,'10',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc9 = ','.join([all_features[i] for i in f_c[16]])
	if feature_role_9_dict.has_key(fc9):
		probs_roles = feature_role_9_dict[fc9]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[16],n,r,'9',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc8 = ','.join([all_features[i] for i in f_c[17]])
	if feature_role_8_dict.has_key(fc8):
		probs_roles = feature_role_8_dict[fc8]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[17],n,r,'8',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc7 = ','.join([all_features[i] for i in f_c[18]])
	if feature_role_7_dict.has_key(fc7):
		probs_roles = feature_role_7_dict[fc7]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[18],n,r,'7',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc6 = ','.join([all_features[i] for i in f_c[19]])
	if feature_role_6_dict.has_key(fc6):
		probs_roles = feature_role_6_dict[fc6]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[19],n,r,'6',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc5 = ','.join([all_features[i] for i in f_c[20]])
	#print fc5
	if feature_role_5_dict.has_key(fc5):
		probs_roles = feature_role_5_dict[fc5]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[20],n,r,'5',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc4 = ','.join([all_features[i] for i in f_c[21]])
	#print fc5
	if feature_role_4_dict.has_key(fc4):
		probs_roles = feature_role_4_dict[fc4]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[21],n,r,'4',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc3 = ','.join([all_features[i] for i in f_c[22]])
	#print fc5
	if feature_role_3_dict.has_key(fc3):
		probs_roles = feature_role_3_dict[fc3]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[22],n,r,'3',probs_roles))	
	#else:
		#potential_roles_GA.append((0,0,0))
	
	#fc2 = ','.join([all_features[i] for i in f_c[23]])
	#print fc5
	if feature_role_2_dict.has_key(fc2):
		probs_roles = feature_role_2_dict[fc2]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[23],n,r,'2',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#fc1 = ','.join([all_features[i] for i in f_c[24]])
	#print fc5
	if feature_role_1_dict.has_key(fc1):
		probs_roles = feature_role_1_dict[fc1]
		(p,n,r) = probs_roles[0]
		if float(n) > threshold:
			potential_roles.append((float(p)*ws[24],n,r,'1',probs_roles))	
		potential_roles_GA.append((p,n,r))
	#else:
		#potential_roles_GA.append((0,0,0))
	#print '='.join([str(p)+','+str(r) for (p,n,r) in potential_roles_GA])
	if potential_roles != []:
		return sorted(potential_roles,reverse=True)[0]
		#return potential_roles[0]
	else:
		return (0,0,None,0,[])	

	
def read_model():
	model_25_file = open("model_25.txt")
	model_24_file = open("model_24.txt")
	model_23_file = open("model_23.txt")
	model_22_file = open("model_22.txt")
	model_21_file = open("model_21.txt")
	model_20_file = open("model_20.txt")
	model_19_file = open("model_19.txt")
	model_18_file = open("model_18.txt")
	model_17_file = open("model_17.txt")
	model_16_file = open("model_16.txt")
	model_15_file = open("model_15.txt")
	model_14_file = open("model_14.txt")
	model_13_file = open("model_13.txt")
	model_12_file = open("model_12.txt")
	model_11_file = open("model_11.txt")
	model_10_file = open("model_10.txt")
	model_9_file = open("model_9.txt")
	model_8_file = open("model_8.txt")
	model_7_file = open("model_7.txt")
	model_6_file = open("model_6.txt")
	model_5_file = open("model_5.txt")
	model_4_file = open("model_4.txt")
	model_3_file = open("model_3.txt")
	model_2_file = open("model_2.txt")
	model_1_file = open("model_1.txt")
	
	feature_role_25_dict = read_m(model_25_file,25)
	feature_role_24_dict = read_m(model_24_file,24)
	feature_role_23_dict = read_m(model_23_file,23)
	feature_role_22_dict = read_m(model_22_file,22)
	feature_role_21_dict = read_m(model_21_file,21)
	feature_role_20_dict = read_m(model_20_file,20)
	feature_role_19_dict = read_m(model_19_file,19)
	feature_role_18_dict = read_m(model_18_file,18)
	feature_role_17_dict = read_m(model_17_file,17)
	feature_role_16_dict = read_m(model_16_file,16)
	feature_role_15_dict = read_m(model_15_file,15)
	feature_role_14_dict = read_m(model_14_file,14)
	feature_role_13_dict = read_m(model_13_file,13)
	feature_role_12_dict = read_m(model_12_file,12)
	feature_role_11_dict = read_m(model_11_file,11)
	feature_role_10_dict = read_m(model_10_file,10)
	feature_role_9_dict = read_m(model_9_file,9)
	feature_role_8_dict = read_m(model_8_file,8)
	feature_role_7_dict = read_m(model_7_file,7)
	feature_role_6_dict = read_m(model_6_file,6)
	feature_role_5_dict = read_m(model_5_file,5)
	feature_role_4_dict = read_m(model_4_file,4)
	feature_role_3_dict = read_m(model_3_file,3)
	feature_role_2_dict = read_m(model_2_file,2)
	feature_role_1_dict = read_m(model_1_file,1)
		
	return (feature_role_25_dict,feature_role_24_dict,feature_role_23_dict,feature_role_22_dict,feature_role_21_dict,feature_role_20_dict,feature_role_19_dict,feature_role_18_dict,feature_role_17_dict,feature_role_16_dict,feature_role_15_dict,feature_role_14_dict,feature_role_13_dict,feature_role_12_dict,feature_role_11_dict,feature_role_10_dict,feature_role_9_dict,feature_role_8_dict,feature_role_7_dict,feature_role_6_dict,feature_role_5_dict,feature_role_4_dict,feature_role_3_dict,feature_role_2_dict,feature_role_1_dict)	
	
def read_m(model_file,fn):

	features = []
	prob_role = []
	feature_role_dict = {}
	for line in model_file.readlines():
		features = line.rstrip().split('==')[0]
		roles = line.rstrip().split('==')[1]
		role_prob = []
		#print line
		#print roles.split('||')
		for role in roles.split('||'):
			r = role.split(',')[1][2:-1]
			p = float(role.split(',')[0][1:])
			n = role.split(',')[2][:-1]
			role_prob.append((p,n,r))
		#print role_prob
		feature_role_dict[features] = role_prob
	return feature_role_dict
	
def role_labeler():
	tree_head_dict = build_tree_head_dict()
	simplified_tradictional_dict = build_simplified_traditional_dict()
	#print 'reading model.......'
	(feature_role_25_dict,feature_role_24_dict,feature_role_23_dict,feature_role_22_dict,feature_role_21_dict,feature_role_20_dict,feature_role_19_dict,feature_role_18_dict,feature_role_17_dict,feature_role_16_dict,feature_role_15_dict,feature_role_14_dict,feature_role_13_dict,feature_role_12_dict,feature_role_11_dict,feature_role_10_dict,feature_role_9_dict,feature_role_8_dict,feature_role_7_dict,feature_role_6_dict,feature_role_5_dict,feature_role_4_dict,feature_role_3_dict,feature_role_2_dict,feature_role_1_dict) = read_model()
	total = 0
	correct = 0
	#old_semRoles = []
	#new_semRoles = []
	#print 'Assigning roles....'
	(old_semRoles,new_semRoles) = assign_roles(feature_role_25_dict,feature_role_24_dict,feature_role_23_dict,feature_role_22_dict,feature_role_21_dict,feature_role_20_dict,feature_role_19_dict,feature_role_18_dict,feature_role_17_dict,feature_role_16_dict,feature_role_15_dict,feature_role_14_dict,feature_role_13_dict,feature_role_12_dict,feature_role_11_dict,feature_role_10_dict,feature_role_9_dict,feature_role_8_dict,feature_role_7_dict,feature_role_6_dict,feature_role_5_dict,feature_role_4_dict,feature_role_3_dict,feature_role_2_dict,feature_role_1_dict,tree_head_dict,simplified_tradictional_dict)
	#new_semRoles = tree_semRoles(new_tree,new_semRoles)
	#new_trees.append(new_tree)
	#print_tree(tree)
	#print_tree(new_tree)
	#print old_semRoles
	#print new_semRoles
	#print old_semRoles[:10]
	#print new_semRoles[:10]
	for i in range(len(old_semRoles)):
		if str(old_semRoles[i]) == str(new_semRoles[i]):
			correct = correct + 1
	errors = [(x,y) for (x,y) in zip(old_semRoles[0:],new_semRoles[0:]) if str(x) != str(y)]
	#print 'Total assigned roles: ' + str(len(new_semRoles))
	#print 'Errors: ' + str(len(errors))
	#print old_semRoles
	#print new_semRoles
	#grouped = [list(g) for k, g in groupby(sorted(errors))]
	#b = sorted((grouped, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0),reverse=True)
	#b = sorted(grouped, key = len)
	#err_file = open('./errorAnalysis/errors-log.txt','w')
	#for l in b:
	#	err_file.write(str(len(l))+'\t'+str(l[0])+'\n')
	#print b[-2]
	#print len(b[-2])
	#print sorted(errors)
	#print len([(x,y) for (x,y) in errors if x=='predication' or y == 'predication'])
	#print new_semRoles.count('no-role')
	print 'Accuracy: ' + str(float(correct)/len(old_semRoles))
	#print len(old_semRoles)


def tree_semRoles(t,semRoles):
	if t.semRole != 'Head' and t.semRole != 'head':
		semRoles.append(t.semRole)
	for c in t.children:
		tree_semRoles(c,semRoles)
	return semRoles
'''def tree_semRoles(t,semRoles):
	if t.children != []:
		for ch in t.children:
			if ch.semRole != 'Head' and ch.semRole != 'head':
				semRoles.append(ch.semRole)
	for c in t.children:
		tree_semRoles(c,semRoles)
	return semRoles'''
	
def compare_trees(old,new,correct,total):
	#print old.semRole
	#print new.semRole
	if old.semRole == new.semRole:
		correct = correct + 1
	total = total + 1
	#print total
	#print correct
	children = new.children
	for ch in range(0,len(children)):
		compare_trees(old.children[ch],new.children[ch],correct,total)
	return (correct,total)
def compare_our_maxent():
	our = open('test-out-ch.txt').readlines()
	#maxent = open('./ch-pb-srl-full/results/ch-propbank-results.txt').readlines()
	maxent = open('C:\shafqat\PostDoc\SRL\experiments\SRLTraining\maxent\opennlp-maxent\opennlp-maxent-3.0.0\samples\sports\ch-propbank-results.txt').readlines()
	roles = []
	for (o,m) in zip(our,maxent):
		to = o.split(' ')
		tm = m.split(' ')
		'''if tm[0] != to[0]:
			print tm[0]'''
		if to[2].rstrip() == '[]':
			roles.append((to[0],tm[0]))
		else:
			p1 = float(to[2].split(',')[0].split('(')[1])
			p2 = float(tm[1].rstrip())
			'''if p1 < 1.0:
				roles.append((to[0],tm[0]))
			else:
				roles.append((to[0],to[1]))'''
			if p2 < 0.61: # 0.61
				roles.append((to[0],to[1]))
			else:
				roles.append((to[0],tm[0]))
			'''if p1>= p2:
				roles.append((to[0],to[1]))
			else:
				roles.append((to[0],tm[0]))'''
	for (r1,r2) in roles:
			if r1 != r2:
				print (r1,r2)
		#if o.split(' ')[0] == o.split(' ')[1] and o.split(' ')[0] != m.split(' ')[0]:
		#	print o.rstrip() + '||' + m.rstrip()
def maxent_multi_model():
	our = open('test-out.txt').readlines()
	mfull = open('./ch-pb-srl-full/results/ch-propbank-results-full.txt').readlines()
	ml10 = open('./ch-pb-srl-full/results/ch-propbank-results-10.txt').readlines()
	ml9 = open('./ch-pb-srl-full/results/ch-propbank-results-9.txt').readlines()
	ml8 = open('./ch-pb-srl-full/results/ch-propbank-results-8.txt').readlines()
	ml7 = open('./ch-pb-srl-full/results/ch-propbank-results-7.txt').readlines()
	ml6 = open('./ch-pb-srl-full/results/ch-propbank-results-6.txt').readlines()
	ml5 = open('./ch-pb-srl-full/results/ch-propbank-results-5.txt').readlines()
	ml4 = open('./ch-pb-srl-full/results/ch-propbank-results-4.txt').readlines()
	ml3 = open('./ch-pb-srl-full/results/ch-propbank-results-3.txt').readlines()
	ml2 = open('./ch-pb-srl-full/results/ch-propbank-results-2.txt').readlines()
	ml1 = open('./ch-pb-srl-full/results/ch-propbank-results-1.txt').readlines()
	gold = open('./ch-pb-srl-full/results/test.txt').readlines()
	roles = []
	for (o,mf,m10,m9,m8,m7,m6,m5,m4,m3,m2,m1,g) in zip(our,mfull,ml10,ml9,ml8,ml7,ml6,ml5,ml4,ml3,ml2,ml1,gold):
		to = o.split(' ')
		tmfull = mf.split(' ')
		tm10 = m10.split(' ')
		tm9 = m9.split(' ')
		tm8 = m7.split(' ')
		tm7 = m7.split(' ')
		tm6 = m6.split(' ')
		tm5 = m5.split(' ')
		tm4 = m4.split(' ')
		tm3 = m3.split(' ')
		tm2 = m2.split(' ')
		tm1 = m1.split(' ')
		pfull = float(tmfull[1].rstrip())
		p10 = float(tm10[1].rstrip())
		p9 = float(tm9[1].rstrip())
		p8 = float(tm8[1].rstrip())
		p7 = float(tm7[1].rstrip())
		p6 = float(tm6[1].rstrip())
		p5 = float(tm5[1].rstrip())
		p4 = float(tm4[1].rstrip())
		p3 = float(tm3[1].rstrip())
		p2 = float(tm2[1].rstrip())
		p1 = float(tm1[1].rstrip())
		temp_role = []
		if pfull > 0:
			roles.append((tmfull[0],g.rstrip()))
		else:
			#temp_role.append((pfull*1.0,tmfull[0]))
			temp_role.append((p10,tm10[0]))
			#temp_role.append((p9,tm9[0]))
			#temp_role.append((p8,tm8[0]))
			#temp_role.append((p7,tm7[0]))
			#temp_role.append((p6,tm6[0]))
			#temp_role.append((p5,tm5[0]))
			#temp_role.append((p4,tm4[0]))
			#temp_role.append((p3,tm3[0]))
			#temp_role.append((p2,tm2[0]))
			#temp_role.append((p1,tm1[0]))
			(bp,br) = sorted(temp_role,reverse=True)[0]
			roles.append((br,g.rstrip()))
		'''if pfull > 0.64:
				roles.append((tmfull[0],g.rstrip()))
		#else:
		elif p10 > 0.64:
				roles.append((tm10[0],g.rstrip()))
		#elif p9 > 0.64:
		else:
				roles.append((tm9[0],g.rstrip()))'''
		'''elif p8 > 0.64:
				roles.append((tm8[0],g.rstrip()))
		elif p7 > 0.64:
				roles.append((tm7[0],g.rstrip()))
		elif p6 > 0.64:
				roles.append((tm6[0],g.rstrip()))
		elif p5 > 0.64:
				roles.append((tm5[0],g.rstrip()))
		elif p4 > 0.64:
				roles.append((tm4[0],g.rstrip()))
		elif p3 > 0.64:
				roles.append((tm3[0],g.rstrip()))
		elif p2 > 0.64:
				roles.append((tm2[0],g.rstrip()))
		else:
				roles.append((tm1[0],g.rstrip()))'''
			
	for (r1,r2) in roles:
			if r1 != r2:
				print (r1,r2)
def compare_maxent_maxent():
	max1 = open('./ch-pb-srl-full/results/ch-propbank-results-temp.txt').readlines()
	max2 = open('./ch-pb-srl-full/results/ch-propbank-results.txt').readlines()
	gold = open('./ch-pb-srl-full/results/test.txt').readlines()
	roles = []
	for (m1,m2,g) in zip(max1,max2,gold):
		tm1 = m1.split(' ')
		tm2 = m2.split(' ')
	
		p1 = float(tm1[1].rstrip())
		p2 = float(tm2[1].rstrip())
		if p2 > p1:
				roles.append((g.rstrip(),tm2[0]))
		else:
				roles.append((g.rstrip(),tm1[0]))
	for (r1,r2) in roles:
			if r1 != r2:
				print (r1,r2)
def draw_a_tree():
	import nltk
	t_str = '( (S (S-TPC-1 (NP-SBJ (NP (NP (DT A) (NN form) )(PP (IN of) (NP (NN asbestos) )))(RRC (ADVP-TMP (RB once) )(VP (VBN used) (NP (-NONE- *) )(S-CLR (NP-SBJ (-NONE- *) )(VP (TO to) (VP (VB make) (NP (NNP Kent) (NN cigarette) (NNS filters) )))))))(VP (VBZ has) (VP (VBN caused) (NP (NP (DT a) (JJ high) (NN percentage) )(PP (IN of) (NP (NN cancer) (NNS deaths) ))(PP-LOC (IN among) (NP (NP (DT a) (NN group) )(PP (IN of) (NP (NP (NNS workers) )(RRC (VP (VBN exposed) (NP (-NONE- *) )(PP-CLR (TO to) (NP (PRP it) ))(ADVP-TMP (NP (QP (RBR more) (IN than) (CD 30) )(NNS years) )(IN ago) )))))))))))))'
	t = nltk.Tree(t_str)
	t.draw()
if __name__ == "__main__":
 import sys
 try:
 
	#role_labeler()
	compare_our_maxent()
	#compare_maxent_maxent()
	#maxent_multi_model()
	#draw_a_tree()
 except:
	print >>sys.stderr, __doc__
	raise