
def build():
		arg_list2 = []
		concepts = open('classifier-output.txt').readlines()
		identifications = open('identifier-output.txt').readlines()
		output = open('output.txt','a')
		for (ident,conc) in zip(identifications,concepts):
			if ident.split(' ')[0] == 'yes':
							arg_str = conc.split(' ')[1]
							pred_lemma = conc.split(' ')[0]
							label = conc.split(' ')[2]
							flat_arg_str = arg_str.replace(' ','_')
							if label.rstrip() == 'ARG0':
									arg_list2.append(flat_arg_str+'_'+pred_lemma)
							elif label.rstrip() == 'ARGM-COM':
									arg_list2.append(pred_lemma+'_{with}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-LOC':
									arg_list2.append(pred_lemma+'_{in}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-DIR':
									arg_list2.append(pred_lemma+'_{in_the_direction}_'+flat_arg_str)
							elif label.rstrip() == 'ARGM-PRP':
									arg_list2.append(pred_lemma+'_{in_order_to}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-CAU':
									arg_list2.append(pred_lemma+'_{because}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-NEG':
									arg_list2.append(pred_lemma+'_{negation}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-GOL':
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-MNR':
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-TMP':
									arg_list2.append(pred_lemma+'_{when}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							elif label.rstrip() == 'ARGM-EXT':
									arg_list2.append(pred_lemma+'_{by}_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
							else:
									arg_list2.append(pred_lemma+'_'+flat_arg_str)
									arg_list2.append(flat_arg_str)
		
		uniq_concepts = list(set(arg_list2)) 
		output.write(str(uniq_concepts)+'\n')
		for concept in uniq_concepts:
			#output.write(concept+'\n')
			print concept
			
def my_flatten(node,flat_list):
	if node.data != None and node.data not in ['IN','TO'] and node.word != None and node.word != []:
		flat_list.append(node.word)
	for ch in node.children:
		my_flatten(ch,flat_list)
	return flat_list
					
if __name__ == "__main__":
 import sys
 try:
	#tree_head_dict = build_tree_head_dict()
	build()
 except:
	print >>sys.stderr, __doc__
	raise