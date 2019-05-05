import socket, sys

def proxy_server(webserver, port, conn, addr, data, buffer_size):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(data)

    first_line = data.split('\n')[0]
    url = first_line.split(' ')[1]
    print '[*] Sending request to: %s' % url

    while True:
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