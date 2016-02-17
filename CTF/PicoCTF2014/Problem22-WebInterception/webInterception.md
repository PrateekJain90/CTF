#Web Interception
---

***We were able to get some code running in a Daedalus browser. Unfortunately we can't quite get it to send us a cookie for its internal login page ourselves... But we can make it make requests that we can see, and it seems to be encrypting using ECB mode. See here for more details about what we can get. It's running at vuln2014.picoctf.com:65414. Can you get us the cookie?***

*Hint: In ECB mode, the same plaintext block appearing in two different places leads to the same ciphertext block appearing in both places. Can you figure out how to use this, and the encryption oracle that you have, to decrypt the cookies one byte at a time?*

##Solution:

I looked at the code given in the problem to see what exactly the server is doing.

#####The functions of interest were the following:
---

* This code seemed to accept the incoming requests, in the form of hex encoded strings, send this request to an oracle and return the encrypted value back to the client. 
```
class incoming(SocketServer.StreamRequestHandler):
  def handle(self):
    self.request.send("Please send the path you'd like them to visit, hex-encoded.\n")
    data = self.request.recv(4096).strip('\n')
    self.request.send(oracle(data).encode('hex') + '\n')
    self.request.close()
```
* The code below, defines the oracle, which prepends 'GET /' to the path that we send and then appends the secret to it. It then pads the resulting string and encrypts the string using AES.
```
def oracle(s):
  # so, this is simulated. In reality we'd have to run javascript on a target web browser
  # and capture the traffic. That's pretty hard to do in a way that scales, though, so we
  # simulate it instead.
  # This uses ECB mode.
  return AESCipher(key).encrypt(pkcs7_pad('GET /' + s.decode('hex') + secret_data))
```  
  
* Finally, the code which does the padding gives me the information that the blocks are 16 bytes long.
```
def pkcs7_pad(s):
  l = len(s)
  needed = 16 - (l % 16)
  return s + (chr(needed) * needed)
```
   
This means that whatever request path we send to the server, it will add the 'GET /' and the secret to the request. As the blocks are 16 bytes in length, if the last block has a size less than 16, then it will be padded to make its length equal to 16 bytes. If all the blocks are 16 bytes in length, then an additional block of 16 byte will be added which will just be padding. Also, it can be seen the same character will be repeated to pad a block up to 16 bytes.
>eg. |a a a a a a a a a a a a a 03 03 03| 

-

#####Figuring out the length of the secret:
---

So, my task now is to figure out the length of the secret in order to start extracting one byte at a time from it.

* In the first request, I did not enter a path and just pressed enter. I got a response:

**Response:**

`14b196e9ff91f66cf1e1aa651171cf23 10da6873ff3f8526ef7d6aa0a15c40d1 670a6814a9088460fff9b66b793009ef b06727840393f0404517b4fbd01a307d d00ff622ea81109390c0474046129263`

The request string in this case consisted of 5 bytes of 'GET /' and the rest from secret.

* Next, I tried an input with 11 a's to make sure that the secret starts from a fresh block. 'GET /' + 11 a's = 16 bytes.

**Input:** 

`6161616161616161616161`

**Response:**

`0dec3d036d2017f7105cef2542c89a4d 17d4d5622444e2e0472ab5a198c66d82 85441c062fff5636a1cb13ca9dc53f17 5fe0a7961b3b539869a6cd155b9f1cb9 44420595dc651e055bed56136dcc661f`

In this output, the first block contains the input I sent along with the 'GET /'. Second block onwards, the secret starts. Currently it is contained in 4 blocks.

* I tried another input, this time, with 12 a's. This would push the secret forward by 1 byte.

**Input:**  

`616161616161616161616161`

**Response:**

`0dec3d036d2017f7105cef2542c89a4d b54fb8355ebe8a2c7056ca48b4124aef 7bb2c562649b06c08ae178a597ba85d2 c87adffd4197a50cdc4d47384db2b219
8e930fb9cdf30c3a2c914731545f9fb3 695e6035c5752aa0d133f436a7d4475f`

Okay. So increasing the inputs length to 12 causes an extra block to come. This can happen only if the secret was 63 bytes long. An extra 'a', pushed the secret to a 16 byte boundary and an extra block of padding is thus added. 

>|GET /aaaaaaaaaaa| |ssssssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |sssssssssssssssp|

>|GET /aaaaaaaaaaa| |asssssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |pppppppppppppppp|

-

####Extracting the secret 1 byte at a time:
---
Now that I know that the secret is 63 bytes long, I can start extracting the bytes one by one.
This can be done as follows:

If the input last given, is again increased by length of 1, then I will get the last byte of the secret in the last block.

>|GET /aaaaaaaaaaa| |aassssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |sppppppppppppppp|

So now, that I have isolated the last byte of the secret, I need a way to decode it.
This is how it can be done.
I construct my input something like this:

>|GET /aaaaaaaaaaa| |appppppppppppppp| |aassssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |sppppppppppppppp|

I add 11 a's to make the first block to 16 bytes.
Then I add a dummy block with just a single 'a' with padding. (using pkcs7_pad)
I then add the 'aa' to move 1 byte of secret to the last block.

**That's it!**
Because ECB is used, where same plaintext corresponds to the same ciphertext, I will keep on changing the first character of the second block 'a/b/c....' and send repeated requests to the server, till the second and the last block match.
The character in the second block for which this match occurs, will be the last letter of the secret.

This process can then be repeated to find the remaining bytes.

>|GET /aaaaaaaaaaa| |akpppppppppppppp| |aaasssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |ssssssssssssssss| |skppppppppppppppp|

I then wrote a script to calculate this and got the following answer:

`HTTP/1.1 Cookie: flag=congrats_on_your_first_ecb_decryption\r\n`
