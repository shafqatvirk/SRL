from prepareData import *

def find_features_without_traces(nh_pairs,parsed,predicate):
		terNo_height = nh_pairs
		#if nh_pairs.find('*') == -1 and nh_pairs.find(';') == -1 and nh_pairs.find(',') == -1:
		#list_of_features = []
		terNo = int(terNo_height.split(':')[0])
		height = int(terNo_height.split(':')[1])
		(arg) = traverse_tree_depth(parsed,terNo,height)
		# to print every argument tree into a file, which will be used by java program to find heads
		pt = arg.data
		if pt != '-NONE-':
			tree_line = print_tree_file(arg,[])
			#print terNo
			#print height
			#print str(tree_line)
			#pred_line = print_tree_file(predicate,[])
			#pred_tree = ''.join(pred_line)
			arg_tree =  ''.join(tree_line)
			return (arg_tree)
		else:	
			return (0)
def extract_complex_NP_concept(parsed,concepts):
	if parsed.data in ['NP'] and (parsed.children) > 1:
		concepts.append(parsed)
	for ch in parsed.children:
		extract_complex_NP_concept(ch,concepts)
	return concepts
def build_tree_head_dict():
	dict = {}
	trees = open('../headFinder/argument-trees2.txt').readlines()
	heads = open('../headFinder/heads.txt')
	for t in trees:
		dict[t.rstrip()] = heads.readline().rstrip()
		#print t.rstrip()
		#print dict[t.rstrip()]
		#print
	return dict
def pruning(node,pred,predNum,candidates):
	if node.terNo == predNum:
		candidates = find_candidates(node.parent,node,candidates)
		return candidates
	for ch in node.children:
			candidates = pruning(ch,pred,predNum,candidates)
	return candidates

def find_candidates(parrent,node,candidates):
	temp_parent = None
	temp_node = None
	if parrent == None:
		return candidates
	for ch in parrent.children:
		if ch != node:
			if ch.data == 'PP':
				candidates.append(ch)
				for c in ch.children:
					candidates.append(c)
			else:
				candidates.append(ch)
	temp_parrent = parrent.parent
	temp_node = parrent
	candidates = find_candidates(temp_parrent,temp_node,candidates)
	return candidates
def print_all_subtrees(parsed,all):
		tree_line = ''.join(print_tree_file(parsed,[]))
		if tree_line.split(' ')[0] not in ['(-NONE-','(``','(,','(.','(:'] and tree_line.split(')')[0].find('*') == -1 and tree_line.split(' ')[1] != '(-NONE-':
			all.append(tree_line)
		for ch in parsed.children:
			print_all_subtrees(ch,all)
		return all
def extract_head(c,tree_head_dict):
	tree_line = ''.join(print_tree_file(c,[]))
	#print tree_line
	if tree_head_dict.has_key(tree_line.rstrip()):
		#print 'found'
		heads = tree_head_dict[tree_line.rstrip()]
		h_pos = heads.rstrip().split(' ')[0].lstrip('(')
		h = heads.rstrip().split(' ')[1].rstrip(')')
		return (h,h_pos)
	else:
		return ('no-h','no-h-pos')
def find_pred_parrent(node,predWordnum,pred_parrent):
	if node.terNo == predWordnum:
		pred_parrent =  node.parent
	else:
		for ch in node.children:
			pred_parrent = find_pred_parrent(ch,predWordnum,pred_parrent)
			if pred_parrent != None:
				break
	return pred_parrent
def find_subcat(node):
	subcat = []
	subcat.append(node.data.rstrip())
	for ch in node.children:
		subcat.append(ch.data.rstrip())
	return ''.join(subcat)
def find_pred_trees(node,pred_trees):
	if node.data in ['VB','VBZ','VBN','VBD','VBG','VBP']:
		pred_trees.append((node,node.terNo))
	for ch in node.children:
		find_pred_trees(ch,pred_trees)
	return pred_trees
def remove_functional_tags(tree):
	if tree != None:
		if (tree.data).find('-') != -1:
			tree.data = '-'.join((tree.data).split('-')[:-1])
		for ch in tree.children:
			remove_functional_tags(ch)