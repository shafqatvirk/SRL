import string
class Tree(object):
	def __init__(self):
		self.children = []
		self.data = None
		self.pos = None
		self.position = None
		self.word = None
		self.depth = 0
		self.terminal = False
		self.terNo = None
		self.parent = None
		#self.sid = None
		self.semRole = None
def print_tree(tree):
 if tree != None:  
    print str(tree.data)+' ('
    for ch in tree.children:
        print_tree(ch)
        print ')'
'''def print_tree_file(tree,tree_line):
	if tree != None:  
		if len(tree.children) > 1:
			tree_line.append('(' + str(tree.data)+' ')
			for ch in tree.children:
				print_tree_file(ch,tree_line)
			tree_line.append(') ')
			return tree_line
		elif len(tree.children) == 1 and len(tree.children[0].children) == 1:
			tree_line.append('('+str(tree.data)+' ')
			for ch in tree.children:
				print_tree_file(ch,tree_line)
			tree_line.append(') ')
			return tree_line
		else:
			tree_line.append('('+str(tree.data)+' ')
			tree_line.append(str(tree.children[0].data))
			tree_line.append(') ')
			return tree_line'''
def print_tree_file(tree,tree_line):
	if tree != None:  
		if tree.word == None:
			tree_line.append('('+ str(tree.data.rstrip())+' ')
		else:
			tree_line.append('('+str(tree.data.rstrip())+' ' + tree.word.rstrip('\n').lstrip())
		for ch in tree.children:
			print_tree_file(ch,tree_line)
		tree_line.append(') ')
		return (tree_line)
def print_tree_srl(tree,tree_line):
	if tree != None:  
		if tree.semRole == None:
			if tree.word == None:
				tree_line.append('('+ str(tree.data.rstrip('\n'))+' ')
			else:
				tree_line.append('('+str(tree.data.rstrip('\n'))+' ' + tree.word.rstrip('\n').lstrip())
		else:
			if tree.word == None:
				tree_line.append(tree.semRole+':'+'('+ str(tree.data.rstrip('\n'))+' ')
			else:
				tree_line.append(tree.semRole+':'+'('+str(tree.data.rstrip('\n'))+' ' + tree.word.rstrip('\n').lstrip())
		for ch in tree.children:
			print_tree_file(ch,tree_line)
		tree_line.append(') ')
		return (tree_line)
def parseExpr(exp,depth,r):
		expr = exp.lstrip()
		node = Tree()
		node.data = ''.join(expr.split(' ')[0][1:])
		children = findChildren(' '.join(expr.split(' ')[1:]))
		if len(children) == 1:
			node.terminal = True
			node.terNo = r
			r = r + 1
			#childNode = Tree()
			#childNode.data = children[0]
			#node.children = [childNode]
			node.word = children[0]
			node.children = []
		else:
			node.terminal = False
		node.depth = depth
		for ch in children[:-1]:
			(n,r) = parseExpr(ch,depth+1,r)
			n.parent = node
			node.children.append(n)
		#node.children = [parseExpr(child,depth+1) for child in children[:-1]]
		return (node,r)
			
def findChildren(exp):
	#print exp
	#print
	expr = list(exp.lstrip())
	c = 0
	buffer = []
	children = []
	for tk in expr[:-1]:
	 if tk == '(':
	  c = c + 1
	  buffer.append(tk)
	 elif tk == ')':
	  c = c - 1
	  buffer.append(tk)
	  if c == 0:
		children.append((''.join(buffer)).lstrip())
		buffer = []
		continue
	 else:
	  buffer.append(tk)
	children.append(''.join(buffer))
	return children

def traverse_tree(t,c):
	if t.terNo == c:
		print t.data
		for chh in t.children:
		  print chh.data
		return t
	for ch in t.children:
		traverse_tree(ch,c)
		
def traverse_tree_depth(t,n,d):
	for ch in t.children:
		t_found = find_terminal(ch,n,None)
		#print t_found.data
		if t_found != None:
			#print t_found.data
			#print t_found.depth
			td = t_found.depth
			#arg = find_arg(ch,td-d,None)
			arg = find_arg(t_found,d)
			#print arg.data
			#print_tree(arg)
			return (arg)
			break

def find_terminal(ch,n,c):
	if ch.terNo == n:
		c = ch
	for sub_ch in ch.children:
		c = find_terminal(sub_ch,n,c)
	return c
def find_arg(node,d):
	for i in range (0,d):
		node = node.parent
	#print node.data
	return node

def find_gov(t,n,d):
	for ch in t.children:
		t_found = find_terminal(ch,n,None)
		if t_found != None:
			#print t_found.data
			#print t_found.depth
			td = t_found.depth
			#arg = find_arg(ch,td-d,None)
			arg = find_arg(t_found,d)
			while arg.data != 'S' or arg.data != 'VP':
				arg = arg.parent
				if arg != None:
					if arg.data == 'S' or arg.data == 'VP':
						return arg.data
					continue
				else:
					return 'none'
				
			
def get_path(arg,tree,pred):
				full_path = find_full_path(arg,tree,pred)
				return full_path
				
def find_full_path(arg,tree,pred):
				full_path = [arg.data.rstrip()]
				found = False
				partial_path = []
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					full_path.append(arg.data.rstrip())
					(partial_path,found) = find_predicate(arg,invalid_ch,pred,[],found)
				full_path = full_path + partial_path
				return full_path
				#return '|'.join(full_path)	
def find_predicate(arg,invalid_ch,pred,p_path,f):
	for ch in arg.children:
		if ch != invalid_ch and f == False:
			if ch.terNo == pred:
				#print ch.terNo
				#print pred
				#print ch.data
				#print ch.terNo
				#print n
				f = True
				p_path.append(ch.data.rstrip())
				break
			else:
				#f = False
				p_path.append(ch.data.rstrip())
				#print p_path
				(p_path,f) = find_predicate(ch,'',pred,p_path,f)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f)			
			
def convert_trees(file_id):
 penn_tree_file = open(file_id,"r")
 penn_trees = penn_tree_file.read()
 tokens = list(penn_trees)
 c = 0
 trees = []
 tree = []
 for t in tokens:
	if t == '(':
		c = c + 1
		tree.append(t)
		#print tree
	elif t == ')':
		c = c - 1
		if c == 0:
			tree.append(t)
			trees.append(''.join(tree[2:-1]))
			tree = []
			continue
		else:
			tree.append(t)
	elif t == '\n':
		continue
	else:
		tree.append(t) 
 return trees

 

if __name__ == "__main__":
 import sys
 try:
	trees = convert_trees()
	for t in trees[0:1]:
		(parsed,r) = parseExpr(t,0,0)
		#traverse_tree(parsed,16)
		traverse_tree_depth(parsed,8,0)
		#print t
		#print parsed
		#print 
 except:
	print >>sys.stderr, __doc__
	raise