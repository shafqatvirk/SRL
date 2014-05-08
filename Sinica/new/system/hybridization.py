from srl import *

def hybrid():
	tree_line = open('../temp/srl-output.txt','r').readline().rstrip()
	maxent_output = open('../temp/classifier-output.txt').readlines()
	new_tree_file = open('output.txt','w')
	tree = parseExpr(tree_line)
	new_tree = change_roles(tree,maxent_output,0)
	new_tree_file.write(''.join(print_tree_line(new_tree,[])))
	new_tree_file.close()
def change_roles(tree,maxent_output,idx):
	if tree != None:
	 if tree.children != []:		
		for ch in tree.children:
			if ch.semRole != 'Head' and ch.semRole != 'head':
				likelihood = float(maxent_output[idx].rstrip().split(' ')[1])
				maxent_role = maxent_output[idx].rstrip().split(' ')[0]
				idx = idx + 1
				if likelihood > 0.61:
					ch.semRole = maxent_role
	for c in tree.children:
		change_roles(c,maxent_output,idx)
	return tree

if __name__ == "__main__":
 import sys
 try:
	hybrid()
 except:
	print >>sys.stderr, __doc__
	raise