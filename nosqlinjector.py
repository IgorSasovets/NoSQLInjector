import socket, sys
import argparse
from thread import *

sys.path.insert(0, 'lib')
from qs_injector import inject_qs
from proxy_server import proxy_server
from logo import print_logo

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
    
    proxy_server(webserver, port, conn, addr, data, buffer_size)
  except Exception, e:
    print '[*] Exception:'
    print e
    pass

def start():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', listening_port))
    s.listen(max_conn)
    print '\n[*] Initializing socket - Done'
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

def print_options_list():
  print '[*] proxy port: %i' % listening_port
  print '[*] inject payload into query parameters %s' % inject_query_params

# main
try:
  print_logo()
  parser = argparse.ArgumentParser(description='Perform NoSQL injection scan')
  parser.add_argument('-qs', '--injectqs', 
    help='inject malicious payload into query string parameters', type=bool, default=False)
  parser.add_argument('-p', '--port', help='proxy port', type=int, default=8080)
  args = parser.parse_args()
  inject_query_params = args.injectqs 
  listening_port = args.port
  print '\n[*] NoSQLInjector options:'
  print_options_list()
except KeyboardInterrupt:
  print '\n[*] User requested an interrupt'
  print '[*] Application exiting...'
  sys.exit()

max_conn = 10 # Max connection queues to hold
buffer_size = 4096 # Max Socket buffer size
host = '127.0.0.1'

start()