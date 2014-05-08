import string
class Tree(object):
	def __init__(self):
		self.children = []
		self.data = None
		self.pos = None
		self.semRole = None
		self.position = None
		self.word = None
		self.parent = None
		#self.sid = None
def print_tree(tree):
 if tree != None:  
    print str(tree.semRole)+':'+str(tree.pos)+':'+str(tree.word)+ str(len(tree.children))+'('
    for ch in tree.children:
        print_tree(ch)
        print ')'
def parseExpr(expr):
	#print expr
	if expr.find('|')==-1 and expr.find('(')==-1:
		node = Tree()
		node.data = expr.split(':')
		
		if len(node.data)==3:  
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = node.data[2]
		elif len(node.data)==2:
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = []
		elif len(node.data)==1:
			##node.semRole = node.data[0]
			##node.pos = []
			node.pos = node.data[0]
			node.word = []
		elif len(node.data)==4:
			node.semRole = node.data[0]
			node.pos = 'DUMMY'
			node.word = node.data[3]
		else:
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = node.data[2]
		node.children = []
		return node
	else:
		node = Tree()
		node.data = expr[0:expr.find('(')].split(':')
		if len(node.data)==3:  
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = node.data[2]
		elif len(node.data)==2:
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = []
		elif len(node.data)==1:
			##node.semRole = node.data[0]
			##node.pos = []
			node.pos = node.data[0]
			node.word = []
		elif len(node.data)==4:
			node.semRole = node.data[0]
			node.pos = 'DUMMY'
			node.word = node.data[3]
		else:
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = node.data[2]
		#print node.data
		children = findChildren(expr[expr.find('(')+1:-1])
		#print children
		#node.children = [parseExpr(child) for child in children]
		for child in children:
			parsed_child = parseExpr(child)
			parsed_child.parent = node
			node.children.append(parsed_child)
			
		return node


def parseExpr_unannotated(expr):
	#terminal node
	if expr.find('|')==-1 and expr.find('(')==-1:
		node = Tree()
		node.data = expr.split(':')	
		#print 'node data='+node.data
		if len(node.data)==3:  
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = node.data[2]
		elif len(node.data)==2:
			#node.semRole = node.data[0]
			#print '2='+node.data[0]
			node.pos = node.data[0]
			node.word = node.data[1]
		'''elif len(node.data)==4:
			node.semRole = node.data[0]
			node.pos = 'DUMMY'
			node.word = node.data[2]
		else:
			#node.semRole = node.data[0]
			node.pos = node.data[0]
			node.word = node.data[1]'''
		node.children = []
		return node
	else:
		node = Tree()
		node.data = expr[0:expr.find('(')].split(':')
		if len(node.data)==2:  
			node.semRole = node.data[0]
			node.pos = node.data[1]
			node.word = []
		elif len(node.data)==1:
			#node.semRole = node.data[0]
			node.pos = node.data[0]
			node.word = []
		'''elif len(node.data)==3:
			node.semRole = node.data[0]
			node.pos = 'DUMMY'
			node.word = node.data[2]
		else:
			#node.semRole = node.data[0]
			node.pos = node.data[0]
			node.word = node.data[1]'''
		#print node.data
		children = findChildren(expr[expr.find('(')+1:-1])
		#print children
		#node.children = [parseExpr_unannotated(child) for child in children]
		for child in children:
			parsed_child = parseExpr_unannotated(child)
			parsed_child.parent = node
			node.children.append(parsed_child)
		return node			

		
'''def findChildren(expr):
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
	 elif tk == '|' and c == 0:
	  children.append(''.join(buffer))
	  buffer = []
	  continue
	 else:
	  buffer.append(tk)
	children.append(''.join(buffer))
	return children	'''

	
# some Chinese character matches to pipe sign and is creating problems, so a trick to handle that case is to check the token next to pipe sign
def findChildren(expr):
	c = 0
	t = 0
	buffer = []
	children = []
	for tk in expr:
	 if tk == '(':
	  c = c + 1
	  t = t + 1
	  buffer.append(tk)
	 elif tk == ')':
	  c = c - 1
	  t = t + 1
	  buffer.append(tk)
	 elif tk == '|' and c == 0:
	  if t < (len(expr)-1):
	   next = ord(''.join(expr[t+1]))
	   #print ''.join(expr[t+1])
	   #print next
	   if next > 32 and next < 124:
	      children.append(''.join(buffer))
	      buffer = []
	  t = t + 1
	  continue
	 else:
	  t = t + 1
	  buffer.append(tk)
	children.append(''.join(buffer))
	return children	
