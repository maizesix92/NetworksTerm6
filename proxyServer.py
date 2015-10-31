# # 50.012 Networks Lab 2 code skeleton
# Nils, SUTD, 2015
# Based on old code from Kurose & Ross: Computer Networks
# Streamlined, threaded, ported to HTTP/1.1
from socket import *
from thread import *
import sys,os

def clientthread(tcpCliSock):
    message = tcpCliSock.recv(1000) 
    # Extract the parameters from the given message
    # we need to fill "host": the host name in the request
    # we need to fill "resource": the resource requested on the target system
    # we need to fill "filetouse": an escaped valid path to the cache file. could be hash value as well
    host = None
    resource = None
    import re
    m = re.search(r'GET https*://([^/]*)(.*) HTTP/1.1',message)
    if m:
        print "host from first line: "+m.group(1)
        print "resource from first line: "+m.group(2)
        host=m.group(1)
        resource=m.group(2)
    # Extract Host
    m = re.search(r'Host: ([\S]*)\n',message)
    if m:
        print "host from Host:"+m.group(1)
        host=m.group(1)
    if host==None or resource==None:
        print "ERROR: no host found"
        return
    # Extract Accept
    accept=""
    m = re.search(r'Accept: ([\S]*)\n',message)
    if m:
        print "accept: "+m.group(1)
        accept=m.group(1)

    # lets not do connection-alive
    message=message.replace("Connection: keep-alive","Connection: close")
    # generate our cache file name
    import hashlib
    m = hashlib.md5()
    m.update(host+resource)
    filetouse=m.hexdigest()
    fileExist = False

    print "Host: "+host
    print "Resource: "+resource
    try:
        # Check wether the file exist in the cache
        f = open(filetouse, "r")
        outputdata = f.readlines()
        fileExist = True
        # Fill in start.
        # send out the cached file content here
        tcpCliSock.send(outputdata)
        tcpCliSock.flush()
        # Fill in end.
        tcpCliSock.close()
        print 'Read from cache'
	# Error handling for file not found in cache
    except IOError:
        if fileExist == False:
            c = socket(AF_INET, SOCK_STREAM)# Fill in start.	Create a new client socket here	# Fill in end.
            c.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
            os.environ['http_proxy']=''

            # print 'host is '+host+ " resource is"+ resource
            try:
                # Connect to the socket to port 80
                # Fill in start.
                # connect to target on port 80 here
                print "Connecting to 'host'"
                c.connect((host, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile()
                fileobj.write("GET "+ resource + " HTTP/1.1\r\n")
                fileobj.write("Host: "+host+"\r\n")
                if accept:
                    fileobj.write("Accept: "+accept+"\r\n")
                fileobj.write("Connection: close\r\n")
                fileobj.write("\r\n")
                fileobj.flush()
                # Read the response into buffer
                # Fill in start.
                buf=fileobj.readlines()
                # Fill in end.
                fileobj.close()
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                print "received response, saving in "+filetouse
                tmpFile = open("./" + filetouse,"wb")
                # Fill in start.
                # save returned data into cache file
                # also send returned data to original client
                tmpFile.write(buf)
                tcpCliSock.send(buf)
                # Fill in end.
            except gaierror as e:
                print e
            except:
                print "Illegal request"+str(sys.exc_info()[0])
        else:
            # HTTP response message for file not found
            # Fill in start.
            print tcpCliSock.recv(1000)
            # Fill in end.
        # Close the client and the server sockets
        tcpCliSock.close()
        # Fill in start.
        tcpSerSock.close()
        # Fill in end.



# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
# find correct commands to set up the socket here
tcpSerSock.bind(("127.0.0.1", 8080))
# Fill in end.
tcpSerSock.listen(1)
while 1:
    # Start receiving data from the client
    print 'Ready to serve...'
    tcpCliSock, addr = tcpSerSock.accept()
    print 'Received a connection from:', addr
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(tcpCliSock,))
