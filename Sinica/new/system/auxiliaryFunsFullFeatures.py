def print_tree_line(tree,line):
 if tree != None:
	if tree.children == []:
		open_ter = ''
		close_ter = ''
	else:
		open_ter = '('
		close_ter = ')'
	if tree.semRole != None:
		if tree.word != [] and tree.word != None:
			line.append(str(tree.semRole)+':'+str(tree.pos)+':'+str(tree.word)+open_ter)
		else:
			line.append(str(tree.semRole)+':'+str(tree.pos)+open_ter)
	else:
		if tree.word != [] and tree.word != None:
			line.append(str(tree.pos)+':'+str(tree.word)+open_ter)
		else:
			line.append(str(tree.pos)+open_ter)
	for ch in tree.children:
		print_tree_line(ch,line)
		if tree.children[-1] != ch:
			line.append('|')
	line.append(close_ter)
 return line

'''
def pos2semType():
	pos2semType_dict = {}
	pos2semType_file = open('pos2semType.txt')
	for line in pos2semType_file.readlines():
		for pos in line.split(','):
			if line.split('=')[1].rstrip() != '?':
				pos2semType_dict[pos.split('(')[0]] = line.split('=')[1].rstrip()
	return pos2semType_dict'''
def find_all_semType(tree,ehownet,all_semType_list,word2semType_dict):
	if tree.word != []:
		semType = find_semType(tree.word,tree.pos,ehownet,word2semType_dict)
		all_semType_list.append(semType)
	for ch in tree.children:
		find_all_semType(ch,ehownet,all_semType_list,word2semType_dict)
	return '-'.join(all_semType_list)
def word2semType():
	semType_dict = {}
	semType_file = open('../missingWords/result.txt')
	for line in semType_file.readlines():
		tokens = line.rstrip().split(',')
		#semType_dict[(tokens[0],tokens[1])] = tokens[2].split('|')[0]
		semType_dict[(tokens[0])] = tokens[2].split('|')[0]
	return semType_dict
def find_pos(tree,pos_list):
	pos_list.append(tree.pos)
	for ch in tree.children:
		find_pos(ch,pos_list)
	return pos_list
def find_verb_pos(tree,pos):
	if tree.pos in ['VA11','VA12','VA13','VA2','VA3','VA4','VB11','VB12','VB2','VC1','VC2','VC31','VC32','VC33','VD1','VD2','VE11','VE12','VE2','VF1','VF2','VG1','VG2','VH11','VH12','VH13','VH14', 'VH15','VH16','VH17','VH21','VH22','VI1','VI2','VI3','VJ1','VJ2','VJ3','VK1','VK2','VL1','VL2','VL3','VL4']:
		pos.append(tree.pos)
	for ch in tree.children:
			find_verb_pos(ch,pos)
	return pos
def find_pred(tree):
	pred = None
	for ch in tree.children:
		if ch.pos in ['VA11','VA12','VA13','VA2','VA3','VA4','VB11','VB12','VB2','VC1','VC2','VC31','VC32','VC33','VD1','VD2','VE11','VE12','VE2','VF1','VF2','VG1','VG2','VH11','VH12','VH13','VH14', 'VH15','VH16','VH17','VH21','VH22','VI1','VI2','VI3','VJ1','VJ2','VJ3','VK1','VK2','VL1','VL2','VL3','VL4'] and ch.semRole == 'Head':
			pred = ch 
	return pred
def find_head(ch):
		hword = []
		hpos = []
		for c in ch.children:
			if c.semRole == 'DUMMY' and c.pos == 'NP':
				for cc in c.children:
					if cc.semRole == 'Head':
						(hword,hpos) = (cc.word,cc.pos)
					else:
						continue
			else:
				continue
		print hword
		print hpos
		return (hword,hpos)	

def find_h_word(tree):
		h_word=[]
		h_pos=[]
		#(h_word,h_pos) = find_t_word(tree,prep_pos,'','')
		for ch in tree.children:
			if ch.semRole == 'Head': 
				h_word=ch.word
				h_pos=ch.pos
				break
		if h_word==[] and h_pos == []:
			for ch in tree.children:
				if ch.semRole == 'head':# here is a problem, some trees does not have a Head, confirm head and Head both refers to a head or only Head referes to a head
					h_word=ch.word
					h_pos=ch.pos
					break
		if h_pos==[]:
			h_pos='no-h-pos'
		return (h_word,h_pos)
'''def find_h_word(tree):
		h_word=[]
		h_pos=[]
		#(h_word,h_pos) = find_t_word(tree,prep_pos,'','')	
		for ch in tree.children:
				if ch.semRole == 'Head': 
					if ch.word != []:
						h_word=ch.word
						h_pos=ch.pos
						break
					else:
						(h_word,h_pos) = find_h_word(ch)
						break
		if h_word==[] and h_pos == []:
			for ch in tree.children:
				if ch.semRole == 'head':# here is a problem, some trees does not have a Head, confirm head and Head both refers to a head or only Head refers to a head
					h_word=ch.word
					h_pos=ch.pos
					break
		if h_pos==[]:
			h_pos='no-h-pos'
		return (h_word,h_pos)'''
def find_semType(w,pos,e_hownet,word2semType_dict):
	semType_word = ''
	if w != []:
			list_word = e_hownet.searchWord(w.decode('Big5',errors='ignore').encode('utf_8'))
			#print list_word
			if list_word ==[]:
				# if word is not found in ehownet try to predict
				#print word+','+pos
				if word2semType_dict.has_key(w.decode('Big5',errors='ignore').encode('utf_8')):
					semType_word = word2semType_dict[w.decode('Big5',errors='ignore').encode('utf_8')]
					 
				else:
					semType_word = 'no-type'
				
			else:
				#this is valid but it increases the error
				'''for node in list_word:
					if node.pos[0] == pos:	
						semType_word = str(node.getParent()).split("'")[1].split('|')[0] #get semantic type
						break
				if semType_word == '':'''
				semType_word = str(list_word[0].getParent()).split("'")[1].split('|')[0] #get semantic type
	else:
			semType_word='no-type'
	return semType_word
def find_l_r_w_semType(ch,prep_pos,e_hownet,word2semType_dict,all_words_semType)		:
	if ch.children != []:
		for c in ch.children:
			(semType_t_word,t_word_pos) = find_t_w_semType(c,prep_pos,e_hownet,word2semType_dict)
			all_words_semType.append(semType_t_word)
	else:
		all_words_semType.append('no-l-r-word')
	#print all_words_semType
	return all_words_semType
def find_sub_child_word_list(ch,list):
 for child in ch.children:
	if child.word != []:
		list.append((child.word,child.pos))
	else:
	 find_sub_child_word_list(child,list)
 return list
def isPassive(tree,pp,bool):
	if tree.pos in ['P02','P60','P06','P01','P66','P04','P26'] and tree.word.decode('Big5',errors='ignore').encode('utf_8') in pp:#.decode('Big5',errors='ignore').encode('utf_8')  == pp:
		#print 'yes'
		bool = 'True'
		#print bool
	for ch in tree.children:
			bool = isPassive(ch,pp,bool)
			if bool == 'True':
				break
	#print bool
	return bool
def find_voice(tree,pp,v):
	for ch in tree.children:
			if ch.pos in ['P02','P60','P06','P01','P66','P04','P26'] and ch.word.decode('Big5',errors='ignore').encode('utf_8') in pp:#.decode('Big5',errors='ignore').encode('utf_8')  == pp:
				v = 'passive'
				break
	return v
	#print bool
	return bool	
def get_target_pos():
	chinese_word = open('../data/tpos.txt')
	return chinese_word.readlines()[3].rstrip().split(',')
def get_pp():
	chinese_word = open('../data/tpos.txt')
	#print chinese_word.readlines()[1].rstrip().split(',')
	return [w.decode('Big5',errors='ignore').encode('utf_8') for w in chinese_word.readlines()[1].rstrip().split(',')]
	#return chinese_word.readlines()[1].rstrip().decode('Big5',errors='ignore').encode('utf_8') 
# this will return head word and its part of speech
def find_t_word(ch,prep_pos,t_word,t_pos):
	if ch.pos == 'PP' or ch.pos == 'GP':
		for sub_child in ch.children:
			if sub_child.semRole != 'Head' and (sub_child.pos == 'NP' or sub_child.pos == 'GP'):
				(t_word,t_pos) = find_t_word(sub_child,prep_pos,t_word,t_pos)
				break
	elif ch.pos not in prep_pos:
		for sub_child in ch.children:
			#if sub_child.semRole == 'Head' and sub_child.word != []:
			if sub_child.semRole == 'Head':
				if sub_child.word != []:
							t_word = sub_child.word	
							t_pos = sub_child.pos
							break
				else:
					(t_word,t_pos) = find_t_word(sub_child,prep_pos,t_word,t_pos)
					break
					
	else:
		for sub_child in ch.children:
			if sub_child.semRole == 'head' and sub_child.word != []:
				t_word = sub_child.word
				t_pos = sub_child.pos
				break
			else:
				(t_word,t_pos) = find_t_word(sub_child,prep_pos,t_word,t_pos)
				break
	'''print t_word
	print t_pos
	print'''
	return (t_word,t_pos)
# this will return actual word and its part of speech tag	
def find_t_word2(ch,prep_pos,t_word,t_pos):
	if isConjunction(ch):
				t_word = ch.children[0].word
				t_pos = ch.children[0].pos
	elif ch.pos not in prep_pos:
		for sub_child in ch.children:
			#if sub_child.semRole == 'Head' and sub_child.word != []:
			if sub_child.semRole == 'Head':
				if sub_child.word != []:
							t_word = sub_child.word	
							t_pos = sub_child.pos
							break
				else:
					(t_word,t_pos) = find_t_word(sub_child,prep_pos,t_word,t_pos)
					break
					
	else:
		for sub_child in ch.children:
			if sub_child.semRole == 'head' and sub_child.word != []:
				t_word = sub_child.word
				t_pos = sub_child.pos
				break
			else:
				(t_word,t_pos) = find_t_word(sub_child,prep_pos,t_word,t_pos)
				break
	'''print t_word
	print t_pos
	print'''
	return (t_word,t_pos)
def isConjunction(ch):
	isCon = False
	for c in ch.children:
		if c.pos in ['Caa']:
			isCon = True
			break
	return isCon
	
def find_left_right_child_pt(tree,ch):
	indx = tree.children.index(ch)
	if len(tree.children) == 1:
		right = 'empty'
		left = 'empty'
	elif indx == 0:
		left = 'empty'
		right = tree.children[indx+1].pos
	elif indx == len(tree.children)-1:
		right = 'empty'
		left = tree.children[indx-1].pos
	else:
		left = tree.children[indx-1].pos
		right = tree.children[indx+1].pos
	return (left,right)
		
def duplicates(lst, item):
   return [i for i, x in enumerate(lst) if x == item]	

def find_t_w_semType(ch,prep_pos,e_hownet,word2semType_dict):
	if ch.word == []:
					(t_word,tg_pos) = find_t_word2(ch,prep_pos,'','')
					if ch.pos == 'PP' or ch.pos == 'GP':	
						(t_t_word,tg_t_pos) = find_t_word(ch,prep_pos,'','')
						t_word_pos = tg_pos
						#t_word_pos = tg_t_pos
						semType_p_w = find_semType(t_word,tg_pos,e_hownet,word2semType_dict)
						t_word = t_t_word
						semType_w = find_semType(t_t_word,tg_t_pos,e_hownet,word2semType_dict)
						semType_t_word = semType_p_w+'...'+semType_w
					else:
						#semType_t_word = find_semType(t_word,ch.pos,e_hownet,word2semType_dict)
						t_word_pos = ch.pos
						semType_t_word = find_semType(t_word,tg_pos,e_hownet,word2semType_dict)
						#t_word_pos = tg_pos
	else:
					
					semType_t_word = find_semType(ch.word,ch.pos,e_hownet,word2semType_dict)
					t_word_pos = ch.pos
	return (semType_t_word,t_word_pos)
def find_subcat(tree,ch):
	subcatAt = []
	subcatStar = []
	for c in tree.children:
		subcatStar.append(ch.pos)
	for c in ch.children:
		subcatAt.append(c.pos)
	return(''.join(subcatAt),''.join(subcatStar))
def path(arg,pp):
	path_to_BA = find_path_to_BA(arg,pp)
	if path_to_BA != []:
		if 'P02' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P02')+1])
		elif 'P60' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P60')+1])
		elif 'P06' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P06')+1])
		elif 'P01' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P01')+1])
		elif 'P66' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P66')+1])
		elif 'P04' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P04')+1])
		elif 'P26' in path_to_BA:
			path_BA = ''.join(path_to_BA[0:path_to_BA.index('P26')+1])
		else:
					path_BA = 'no-BA'
	else:
					path_BA = 'no-BA'
	return path_BA
def find_path_to_BA(arg,pp):
				full_path = [arg.pos]
				found = False
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					full_path.append(arg.pos)
					(partial_path,found) = find_BA(arg,invalid_ch,[],found,pp)
				if found != False:
					full_path = full_path + partial_path
					#print partial_path
				else:
					full_path = []
				
				#path_to_BA = 
				return (full_path)	
def find_BA(arg,invalid_ch,p_path,f,pp):
	for ch in arg.children:
		if ch != invalid_ch:
			if ch.pos in ['P02','P60','P06','P01','P66','P04','P26'] and ch.word.decode('Big5',errors='ignore').encode('utf_8') in pp:
				f = True
				#BA_terNo = ch.terNo
				p_path.append(ch.pos)
				break
			else:
				#f = False
				#print ch.data
				p_path.append(ch.pos)
				#print p_path
				(p_path,f) = find_BA(ch,'',p_path,f,pp)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f)
	
def find_full_path(arg,pred):
				full_path = [arg.pos]
				found = False
				partial_path = []
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					full_path.append(arg.pos.rstrip())
					(partial_path,found) = find_predicate(arg,invalid_ch,pred,[],found)
				full_path = full_path + partial_path
				
				#path_to_BA = 
				return ''.join(full_path)	
def find_predicate(arg,invalid_ch,pred,p_path,f):
	for ch in arg.children:
		if ch != invalid_ch:
			if ch == pred:
				#print ch.data
				#print ch.terNo
				#print n
				f = True
				p_path.append(ch.pos.rstrip())
				break
			else:
				#f = False
				p_path.append(ch.pos.rstrip())
				#print p_path
				(p_path,f) = find_predicate(ch,'',pred,p_path,f)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f)

def find_left_right_child_pos(tree,ch):
	indx = tree.children.index(ch)
	if len(tree.children) == 1:
		right = 'empty'
		left = 'empty'
		left_role = 'empty'
	elif indx == 0:
		left = 'empty'
		right = tree.children[indx+1].pos
		left_role = 'empty'
	elif indx == len(tree.children)-1:
		right = 'empty'
		left = tree.children[indx-1].pos
		left_role = tree.children[indx-1].semRole
	else:
		left = tree.children[indx-1].pos
		right = tree.children[indx+1].pos
		left_role = tree.children[indx-1].semRole
	return (str(left)+'-'+str(right),left_role)