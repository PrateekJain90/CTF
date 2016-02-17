#Level4:
This involved changing the PATH environment variable. Initially, the code just executed the default whoami command.

```
 FILE* f = popen("whoami","r");
 fgets(username, sizeof(username), f);
 printf("Welcome %s", username);
```

I made a directory inside the `/tmp` folder named as `myCode`. Inside that I created a whoami executable, which just opened the level5 .pass file and printed its contents.

Next, I changed the `PATH` variable to include the `/tmp/myCode` path at the beginning. In this way, when the system tries to find the `whoami` executable, it will first search in the folder which I just specified. This folder contains `whoami` executable which I had made. `popen()` now executes my version of whoami and the flag is printed.

```export PATH=/tmp/myCode:$PATH```

Flag:  `LOoCy5PbKi63qXTh`