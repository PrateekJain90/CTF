import socket
import time

def pkcs7_pad(s):
  l = len(s)
  needed = 16 - (l % 16)
  return s + (chr(needed) * needed)

def makeString(s):
  temp = 'a'*11
  length = len(s)
  temp = temp + pkcs7_pad(s)
  temp = temp + 'a'*(length+1)
  return temp

def chunks(l, n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]

'''HTTP/1.1 Cookie: flag=congrats_on_your_first_ecb_decryption\r\n'''

string = ""
i = 0
while i<127:

  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  conn.connect(("vuln2014.picoctf.com", 65414))
  time.sleep(0.1)
  response = conn.recv(500)

  randomChar = chr(i)
  string = randomChar+string
  length = len(pkcs7_pad(string).encode('hex'))
  stringToSend = makeString(string)
  dataToSend = stringToSend.encode('hex')
  #print dataToSend

  conn.send(dataToSend)
  response = conn.recv(2048)
  #print response

  if(length<=128):
    responseArray = chunks(response,32);
    if(responseArray[1] in responseArray[2:]):
      i = 0
      print "Found:------->" + string 
    else:
      i = i+1
      print string.encode('hex') + " not correct"	
      string = string[1:]
  else:
    break;
