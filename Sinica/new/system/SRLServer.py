import SocketServer
from srl import *

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    print "Loading..."
    e_hownet=EHowNetTree("..\data\ehownet_ontology.txt")
    (feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles) = read_model()
    target_pos = get_target_pos()
    pp = get_pp()
    word2semType_dict = word2semType()
    prep_pos = open('../data/tpos.txt').readlines()[2].rstrip().split(',') 
    dummy = 0
    print "Ready!"
    def handle(self):
        self.feature_file = open('../temp/classifier-feature.txt','w')
        self.srl_file = open('../temp/srl-output.txt','w')
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        annotated_tree = self.srl(self.data)
        #print "{} wrote:".format(self.client_address[0])
        # just send back the same data, but upper-cased
        self.request.sendall(annotated_tree)
        print "Successfully served the request!"
    def srl(self,data):
      clean_expr = data.rstrip()
      print clean_expr
      #tree = parseExpr_unannotated(clean_expr.encode('utf_8'))
      tree = parseExpr_unannotated(clean_expr)
      #tree = parseExpr(clean_expr)
      passive = isPassive(tree,self.pp,'False')
      annotated_tree = assign_roles(tree,self.e_hownet,self.feature_role_dict_10,self.feature_role_dict_9,self.feature_role_dict_8,self.feature_role_dict_7,self.feature_role_dict_6,self.feature_role_dict_5,self.feature_role_dict_4,self.feature_role_dict_3,self.feature_role_dict_2,self.feature_role_dict_1,self.legal_roles,self.target_pos,passive,self.prep_pos,self.dummy,self.word2semType_dict,self.pp,self.feature_file)
      annotated_tree_line = print_tree_line(annotated_tree,[])
      self.feature_file.close()
      self.srl_file.write(''.join(annotated_tree_line))
      self.srl_file.close()
      return ''.join(annotated_tree_line)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()