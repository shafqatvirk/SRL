import SocketServer
import sys
sys.path.append("../shared")
from prepareData import *
from buildModelAuxiliaries import *
#import nltk
import os
import itertools

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
	
	
    print "Loading..."
	
    tree_head_dict = build_tree_head_dict()
    
    print "Ready!"
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        self.extractor(self.data)
        #print "{} wrote:".format(self.client_address[0])
        # just send back the same data, but upper-cased
        self.request.sendall('Done')
        #print "Successfully served the request!"
    def extractor(self,tree):
		(parsed,r) = parseExpr(str(tree),0,0)
		#print parsed.data
		pred_trees =  find_pred_trees(parsed,[])
		#print pred_trees
		identif_file = open('../temp/identifier-features.txt','w')
		classif_file = open('../temp/classifier-features.txt','w')
		pred_file = open('../temp/pred.test','w')
			
		for (pred,pred_terNo) in pred_trees[:]:
			pruned = pruning(parsed,pred,pred_terNo,[])
			#print 
			t_word = pred.word
			#t_word = str(stemmer.stem(pred.word))
			t_w_pos = pred.data
			pred_parrent = find_pred_parrent(parsed,pred_terNo,None)
			subcat = find_subcat(pred_parrent)
			#print t_word
			#identif_file = open(t_word+str(pred_trees.index((pred,pred_terNo)))+'-ident.txt','w')
			#classif_file = open(t_word+str(pred_trees.index((pred,pred_terNo)))+'-classif.txt','w')
			#print t_w_pos
			for c in pruned:
				path_list = get_path(c,parsed,pred_terNo)
				(h,h_pos) = extract_head(c,self.tree_head_dict)
				path = ''.join(path_list)
				distance = len(path_list)
				pt = c.data.rstrip()
				t_word_pls_pt = str(t_word)+str(pt)
				t_word_pls_h_word = str(t_word)+str(h)
				distance_pls_t_word = str(distance)+str(t_word)
			
				subcatStar = find_subcat(c.parent)
				subcatAt = find_subcat(c)
				flat_argument = '_'.join([w.rstrip() for w in my_flatten(c,[])])
				# features for identification
				identif_file.write('h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' ?\n')
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' distance_pls_t_word='+distance_pls_t_word+ ' ?\n'
				# features for classification
				classif_file.write('h='+str(h)+' h_pos='+str(h_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+ ' ?\n')
				#print 'h='+str(h)+' h_pos='+str(h_pos)+' h_word='+str(h)+' h_word_pos='+str(h_pos)+' path='+str(path)+' t_word_pls_pt='+t_word_pls_pt+' t_word_pls_h_word='+t_word_pls_h_word+' subcat='+str(subcat)+ ' subcatAt='+str(subcatAt)+ ' subcatStar='+str(subcatStar)+ ' ?\n'
				pred_file.write(t_word+' '+flat_argument+'\n')
				#print t_word+' '+flat_argument+'\n'
		identif_file.close()
		classif_file.close()
		pred_file.close()
			
def my_flatten(node,flat_list):
	if node.data != None and node.data not in ['IN','TO'] and node.word != None and node.word != []:
		flat_list.append(node.word)
	for ch in node.children:
		my_flatten(ch,flat_list)
	return flat_list	 

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()