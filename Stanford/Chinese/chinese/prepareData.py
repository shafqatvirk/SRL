import string
import re
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
def print_tree(tree):
 if tree != None:  
    print str(tree.terNo)+' ('
    for ch in tree.children:
        print_tree(ch)
        print ')'
def print_tree_file(tree,tree_line):
	if tree != None:  
		if tree.children == []:
			tree_line.append('(' + str(tree.data)+' '+str(tree.word)+')')
			return tree_line
		else:
			tree_line.append('('+str(tree.data)+' ')
			for ch in tree.children:
				tree_line = print_tree_file(ch,tree_line)
			tree_line.append(') ')
		return tree_line
	
def parseExpr(expr,depth,r):
		expr = expr.rstrip()
		expr = ''.join(list(expr)[1:-1]).rstrip(' ')
		#print expr
		if expr.find('(') == -1:
			#print expr
			#print
			node = Tree()
			node.data = ''.join(expr.split(' ')[0])
			node.word = ''.join(expr.split(' ')[1])
			node.terminal = True
			node.depth = depth
			node.terNo = r
			r = r + 1
			node.children = []
			'''print node.data
			print node.word
			print node.depth
			print node.terminal
			print node.terNo
			print'''
			return (node,r)
		else:
			node = Tree()
			node.data = ''.join(expr.split(' ')[0])
			#node.word = ''.join(expr.split(' ')[1])[0:-1]
			node.terminal = False
			#node.terNo = r
			node.depth = depth
			children = findChildren(' '.join(expr.split(' ')[1:]))
			'''print node.data
			print node.word
			print node.depth
			print node.terminal
			print node.terNo
			print'''
			#print len(children)
			#print children
			#print
			for ch in children:
				(n,r) = parseExpr(ch.lstrip('\n').lstrip('\t').lstrip(' '),depth+1,r)
				node.children.append(n)
				n.parent = node
		return (node,r)
			
def findChildren(exp):
	#print exp
	#print
	expr = list(exp.lstrip(' ').lstrip('\t').lstrip('\n').rstrip(' ').rstrip('\t').rstrip('\n'))
	c = 0
	buffer = []
	children = []
	for tk in expr:
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
	 elif tk == '\t' or tk == '\n':
		continue
	 else:
	  buffer.append(tk)
	#children.append(''.join(buffer))
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
		if t_found != None:
			#print t_found.data
			#print t_found.depth
			td = t_found.depth
			#arg = find_arg(ch,td-d,None)
			arg = find_arg(t_found,d)
			#print arg.data
			#print_tree(arg)
			return (arg,t_found.terNo)
			break
	return (0,0)

def find_terminal(ch,n,c):
	if ch.terNo == n:
		c = ch
	for sub_ch in ch.children:
		c = find_terminal(sub_ch,n,c)
	return c
def find_arg(node,d):
	for i in range (0,d):
		node = node.parent
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
			if arg != None:
				while arg.data != 'S' or arg.data != 'VP':
					arg = arg.parent
					if arg != None:
						if arg.data == 'S' or arg.data == 'VP':
							return arg.data
						continue
					else:
						return 'none'
def path(t,n,d,pred):
	for ch in t.children:
		t_found = find_terminal(ch,n,None)
		if t_found != None:
			#print t_found.data
			#print t_found.depth
			td = t_found.depth
			#arg = find_arg(ch,td-d,None)
			arg = find_arg(t_found,d)
			if arg != None:
				full_path = find_full_path(arg,t,n,d,pred)
				(path_to_BA,BA_terNo) = find_path_to_BA(arg,t,n,d,pred,'BA','BA')
				(path_to_BEI,BEI_terNo) = find_path_to_BA(arg,t,n,d,pred,'SB','LB')
				if path_to_BA != [] and 'dBA' in path_to_BA:
					#print path_to_BA
					path_BA = path_to_BA[0:path_to_BA.index('dBA')]
					voice = 'passive'
				else:
					path_BA = 'no-BA'
					voice = 'active'
				if path_to_BEI != []:
					if 'dSB' in path_to_BEI:
						path_BEI = path_to_BEI[0:path_to_BEI.index('dSB')]
						voice = 'passive'
					elif 'dLB' in path_to_BEI:
						path_BEI = path_to_BEI[0:path_to_BEI.index('dLB')]
						voice = 'passive'
					else:
						path_BEI = 'no-BEI'
						voice = 'active'
				else:
					path_BEI = 'no-BEI' 
					voice = 'active'
				return (full_path,''.join(path_BA),''.join(path_BEI),voice,BA_terNo,BEI_terNo)
				'''full_path = [arg.data]
				found = False
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					full_path.append(arg.data)
					(partial_path,found) = find_predicate(arg,invalid_ch,pred,[],found)
				full_path = full_path + partial_path
				
				#path_to_BA = 
				return full_path'''	
def find_full_path(arg,t,n,d,pred):
				full_path = [arg.data]
				found = False
				partial_path = []
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					path_node = 'u'+arg.data.rstrip() # 'u' to denote upward direction
					#full_path.append(arg.data.rstrip())
					full_path.append(path_node)
					(partial_path,found) = find_predicate(arg,invalid_ch,pred,[],found)
				full_path = full_path + partial_path
				
				#path_to_BA = 
				return ''.join(full_path)	
def find_predicate(arg,invalid_ch,pred,p_path,f):
	for ch in arg.children:
		if ch != invalid_ch:
			if ch == pred and ch.terNo == pred.terNo:
				#print ch.data
				#print ch.terNo
				#print n
				f = True
				path_node = 'd'+ch.data.rstrip() # 'd' to denote downward direction
				p_path.append(path_node)
				#p_path.append(ch.data.rstrip())
				break
			else:
				#f = False
				path_node = 'd'+ch.data.rstrip() # 'd' to denote downward direction
				p_path.append(path_node)
				#p_path.append(ch.data.rstrip())
				#print p_path
				(p_path,f) = find_predicate(ch,'',pred,p_path,f)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f)
	
def find_path_to_BA(arg,t,n,d,pred,b1,b2):
				full_path = [arg.data]
				found = False
				while found == False and arg!= None and arg.parent != None:
					partial_path = []
					invalid_ch = arg
					arg = arg.parent
					path_node = 'u'+arg.data.rstrip() # 'u' to denote upward direction
					full_path.append(path_node)
					#full_path.append(arg.data)
					(partial_path,found,BA_terNo) = find_BA(arg,invalid_ch,pred,[],found,b1,b2,0)
				if found != False:
					full_path = full_path + partial_path
					#print partial_path
				else:
					full_path = []
					BA_terNo = 0
				
				#path_to_BA = 
				return (full_path,BA_terNo)	
def find_BA(arg,invalid_ch,pred,p_path,f,b1,b2,BA_terNo):
	for ch in arg.children:
		if ch != invalid_ch:
			if ch.data == b1 or ch.data == b2:
				#print ch.data
				#print ch.terNo
				#print n
				f = True
				BA_terNo = ch.terNo
				path_node = 'd'+ch.data.rstrip() # 'd' to denote upward direction
				p_path.append(path_node)
				#p_path.append(ch.data)
				break
			else:
				#f = False
				#print ch.data
				path_node = 'd'+ch.data.rstrip() # 'd' to denote upward direction
				p_path.append(path_node)
				#p_path.append(ch.data)
				#print p_path
				(p_path,f,BA_terNo) = find_BA(ch,'',pred,p_path,f,b1,b2,BA_terNo)
		else:
			continue
		if f == False:
			p_path = p_path[0:-1]
	return (p_path,f,BA_terNo)
			
'''def convert_trees(file_id):
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
'''
def convert_trees(file_id):
 penn_tree_file = open(file_id,"r")
 penn_trees = penn_tree_file.read()
 #m=re.compile('<S ID=\d+>(.*?)</S>', re.DOTALL).findall(penn_trees)
 m=re.compile('<S ID=\d+[abc]*>(.*?)</S>', re.DOTALL).findall(penn_trees)
 mm = make_tree_list(''.join(m),[])
 return mm
def make_tree_list(str,list_trees):
	expr = list(str)
	c = 0
	buffer = []
	#children = []
	for tk in expr:
	 if tk == '(':
	  c = c + 1
	  buffer.append(tk)
	 elif tk == ')':
	  c = c - 1
	  buffer.append(tk)
	  if c == 0:
		list_trees.append((''.join(buffer)).lstrip())
		buffer = []
		continue
	 elif tk == '\t' or tk == '\n':
		continue
	 else:
	  buffer.append(tk)
	#list_trees.append(''.join(buffer))
	return list_trees 
def make_train_test():
	data = open('cpb1.0.txt')
	for t in data.readlines():
			file_no = t.split(' ')[0].split('/')[-1].split('_')[1].split('.')[0]
			if int(file_no) > 80 and int(file_no) < 900:
			#if (int(file_no) > 0 and int(file_no) < 41) or (int(file_no) > 899 and int(file_no) < 932):
				print t.rstrip()
def dev_train_test():
	data = open('cpb1.0.txt')
	for t in data.readlines():
			file_no = t.split(' ')[0].split('/')[-1].split('_')[1].split('.')[0]
			#if int(file_no) > 40 and int(file_no) < 71:
			if (int(file_no) > 70 and int(file_no) < 81):
				print t.rstrip()
 

if __name__ == "__main__":
 import sys
 try:
	'''trees = convert_trees('./bracketed/chtb_001.fid')
	for t in trees[0:1]:
		(parsed,r) = parseExpr(t,0,0)
		#traverse_tree(parsed,16)
		traverse_tree_depth(parsed,8,0)
		#print t
		#print parsed
		#print '''
	#make_train_test()
	dev_train_test()
 except:
	print >>sys.stderr, __doc__
	raise