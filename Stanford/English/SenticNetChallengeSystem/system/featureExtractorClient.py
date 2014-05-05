import socket
import sys

HOST, PORT = "localhost", 9999
if len(sys.argv) == 2:
	data = sys.argv[1]
	
	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		# Connect to server and send data
		sock.connect((HOST, PORT))
		sock.sendall(data + "\n")

		# Receive data from the server and shut down
		received = sock.recv(1024)
	finally:
		sock.close()

	print "Sent:     {}".format(data)
	print "Received: {}".format(received)
#elif len(sys.argv) == 3:
#	input_batch = open(sys.argv[1])
#	output = open(sys.argv[2],'w')
#	for expr in input_batch.readlines():
#		expr_prefix = expr.split(' ')[0]
#		expr_postfix = expr.split('#')[-1]
#		clean_expr = (''.join(expr.split(' ')[1:])).split('#')[0]
		
		# Create a socket (SOCK_STREAM means a TCP socket)
#		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#		try:
			# Connect to server and send data
#			sock.connect((HOST, PORT))
#			sock.sendall(clean_expr.decode('Big5',errors='ignore').encode('utf_8') + "\n")

			# Receive data from the server and shut down
#			received = sock.recv(1024)
#			output.write(expr_prefix+' ' + received.decode('utf_8').encode('Big5',errors='ignore')+'#'+expr_postfix)
#		finally:
#			sock.close()

		
else:
	print "Usage:"
	print '\t 1. SRLClient "tree to be labeled"'
	print "\t 2. SRLClient [path to input file] [path to output file]"