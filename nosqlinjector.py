import socket, sys
from thread import *

def proxy_server(webserver, port, conn, addr, data):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(data)

    while True:
      print 'in cycle'
      reply = s.recv(buffer_size)

      if (len(reply) > 0):
        conn.send(reply)
        dar = float(len(reply))
        dar = float(dar / 1024)
        dar = '%.3s' % (str(dar))
        dar = '%s KB' % (dar)        
        print '[*] Request done: %s => %s <=' % (str(addr[0]), str(dar))
      else:
        break
    s.close()
    conn.close()
  except socket.error, (value, message):
    print '[*] Proxy server error:'
    print '%s %s' % (value, message)
    s.close()
    conn.close()
    sys.exit(2)

def conn_string(conn, data, addr):
  try:
    first_line = data.split('\n')[0]
    url = first_line.split(' ')[1]

    http_pos = url.find('://')
    if (http_pos == -1):
      temp = url
    else:
      temp = url[(http_pos + 3):]
    
    port_pos = temp.find(':')
    webserver_pos = temp.find('/')
    
    if (webserver_pos == -1):
      webserver_pos = len(temp)
    webserver = ''
    port = -1
    if (port_pos == -1 or webserver_pos < port_pos):
      port = 80
      webserver = temp[:webserver_pos]
    else:
      port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
      webserver = temp[:port_pos]
    
    print '[*] Before request'
    print '%s, %s, %s, %s' % (webserver, port, conn, data)
    proxy_server(webserver, port, conn, addr, data)
  except Exception, e:
    print '[*] Exception:'
    print e
    pass

def start():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', listening_port))
    s.listen(max_conn)
    print '[*] Initializing socket - Done'
    print '[*] Socket binded successfully'
    print '[*] Server started successfully on port [%d]\n' % (listening_port)
  except Exception, e:
    print '[*] Error occurred when tried to initialize a socket:'
    print e
    sys.exit(2)

  while True:
    try:
      conn, addr = s.accept()
      data = conn.recv(buffer_size)
      start_new_thread(conn_string, (conn, data, addr))
    except KeyboardInterrupt:
      s.close()
      print '\n[*] Proxy server is shutting down'
      sys.exit(1)
  s.close()

try:
  listening_port = int(raw_input('[*] Enter Listening Port Number: '))
except KeyboardInterrupt:
  print '\n[*] User requested an interrupt'
  print '[*] Application exiting...'
  sys.exit()

max_conn = 10 # Max connection queues to hold
buffer_size = 4096 # Max Socket buffer size
host = '127.0.0.1'

start()