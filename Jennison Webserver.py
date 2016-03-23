import sys

# Import socket module
from socket import * 

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM) 

# Assign a port number
serverPort = 1492

# Bind the socket to server address and server port
serverSocket.bind(('192.168.1.110',serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print ('Ready to serve...')
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept() 
	
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receive the request message from the client
		message = connectionSocket.recv(1024)
		sys.stdout.flush()
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		decodedmessage = message.decode('UTF-8')
		decodedmessage = decodedmessage.split()
		print (decodedmessage)
		if 2 < len(decodedmessage):
			filename = decodedmessage[1]
		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character 
			f = open(filename[1:])
		# Store the entire content of the requested file in a temporary buffer
			outputdata = f.read()
		# Send the HTTP response header line to the connection socket
			connectionSocket.send(bytes("\rHTTP/1.1 200 OK\r\n\r\n", 'UTF-8')) 
 
		# Send the content of the requested file to the connection socket
			for i in range(0, len(outputdata)):  
				connectionSocket.send(bytes(outputdata[i], 'UTF-8')); 	
			connectionSocket.send(bytes("\r\n", 'UTF-8'));
		
		# Close the client connection socket
		connectionSocket.close(); 

	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send(bytes("\rHTTP/1.1 404 NOT FOUND\r\n\r\n", 'UTF-8'))
		connectionSocket.send(bytes("<html><head><title>You've Been 404'ed</title></head><body><h1><center>YOU CAN'T JUST MAKE UP URLS AND EXPECT THEM TO BE THERE. TRY \"JENNISON.HTML\". IT'S A GOOD ONE.</center></h1></body></html>\r\n", 'UTF-8'))
		# Close the client connection socket
		connectionSocket.close(); 

#Close the Socket
serverSocket.close()  

