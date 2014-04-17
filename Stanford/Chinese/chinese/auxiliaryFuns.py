
def find_all_semType(tree,ehownet,all_semType_list,word2semType_dict):
	if tree.word != []:
		semType = find_semType(tree.word,tree.pos,ehownet,word2semType_dict)
		all_semType_list.append(semType)
	for ch in tree.children:
		find_all_semType(ch,ehownet,all_semType_list,word2semType_dict)
	return '-'.join(all_semType_list)
def word2semType():
	semType_dict = {}
	semType_file = open('./missingWords/result.txt')
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

def find_semType(w,pos,e_hownet,word2semType_dict):
	semType_word = ''
	if w != []:
			#list_word = e_hownet.searchWord(w.decode('Big5',errors='ignore').encode('utf_8'))
			list_word = e_hownet.searchWord(w)
			if list_word ==[]:
				# if word is not found in ehownet try to predict
				#print word+','+pos
				#if word2semType_dict.has_key(w.decode('Big5',errors='ignore').encode('utf_8')):
					#semType_word = word2semType_dict[w.decode('Big5',errors='ignore').encode('utf_8')]
				if word2semType_dict.has_key(w):
					semType_word = word2semType_dict[w]
					 
				else:
					#semType_word = 'no-type'
					semType_word = w # if semantic type is not found then use the word
				
			else:
				#this is valid but it increases the error
				'''for node in list_word:
					if node.pos[0] == pos:	
						semType_word = str(node.getParent()).split("'")[1].split('|')[0] #get semantic type
						break
				if semType_word == '':'''
				semType_word = str(list_word[0].getParent()).split("'")[1].split('|')[0] #get semantic type
	else:
			#semType_word='no-type'
			semType_word=w
	return semType_word
		
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
	
def get_target_pos():
	chinese_word = open('tpos.txt')
	return chinese_word.readlines()[3].rstrip().split(',')
def get_pp():
	chinese_word = open('tpos.txt')
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
	return (left+'-'+right,left_role)
		
def duplicates(lst, item):
   return [i for i, x in enumerate(lst) if x == item]	
	