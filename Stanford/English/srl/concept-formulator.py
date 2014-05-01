
def build():
		arg_list2 = []
		classifier = open('../classifier/maxent/output.txt').readlines()
		identifier = open('../identifier/maxent/output.txt').readlines()
		preds = open('preds.txt').readlines()
		
		output_file = open('output_file.txt','w')
		for (classi,identi,pred) in zip(classifier,identifier,preds):
			if identi.split(' ')[0] == 'yes':
								flat_arg_str = pred.split(' ')[1].rstrip()
								pred_lemma = pred.split(' ')[0].rstrip()
								label = classi.split(' ')[0].rstrip()
								#flat_arg_str = arg_str.replace(' ','_')
								if label.rstrip() == 'ARG0':
									arg_list2.append(flat_arg_str+'_'+pred_lemma)
									arg_list2.append(flat_arg_str)
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
									arg_list2.append(pred_lemma+'_{not}_'+flat_arg_str)
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
		for concept in list(set(arg_list2)):
			output_file.write(concept+'\n')
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