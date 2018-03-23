# printutils
**Various print utils for python3**

## printf
This function prints a string using the standard print function.
Like format strings in python 3.6, variables can be accessed directly:

In python before version 3.6:
```Python
a = 5
# ...
print('{}'.format(a))
```

In python 3.6 or later:
```Python
a = 5
# ...
print(f'{a}')
# 5
```

In python before version 3.6 with printutils:
```Python
from printutils import printf
a = 5
# ...
printf('{a}\n')
# 5
```

The `printf` function has more advantages from python 3.6:
+ `eval` inside fmtstr, wrapped in a julia-like syntax:
```Python
from printutils import printf
a = 5
printf('$(a is 5)\n')
# True
```
+ `exec` inside fmtstr:
```Python
import printutils as p
p.printf('Execution is $("not "*(p.allowExec is False))allowed.\n')
# Execution is not allowed.
p.allowExec = True
p.printf('Execution is $("not "*(p.allowExec is False))allowed.\n')
# Execution is allowed.
p.printf('!(p.allowExec = False)')
p.printf('Execution is $("not "*(p.allowExec is False))allowed.\n')
# Execution is not allowed.
```

# Options
The following options are available:
```Python
import printutils as p
# Default settings:
p.outopt = {'end': ''}
p.allowExec = False
p.warnOnDenial = True
p.returnOnDenial = False
p.warnOnError = True
p.returnFormatted = False
p.outf = print
```
+ **outopt**:
	A dict passed to the output function (**outf**). By default it disables line endings.
	The default setting might change and it's recommended to set it to the desired value after the import.
+ **allowExec**:
	Allow the execution of code with format strings like '!(import os; os.system("rm -rf /"))'. Only enable
	this when you know what you're doing! (The example would erase a linux system installation...)
+ **warnOnDenial**:
	Replace unexecuted substrings like '!(exit())' with '[EXECUTION DENIED]' (True) or an empty string.
	Useful for debugging.
+ **returnOnDenial**:
	When hitting a substring while **allowExec** is set to *False*, the function immediately return *False*.
+ **warnOnError**:
	If the **str.format** fails, replace the part with '[FAILED]' or an empty string. Example:
	```Python
	import printutils as p
	print('This should fail because there are no arguments...: {0!r}\n')
	```
+ **returnFormatted**:
	If the function should return the string it prints. Annoying in ipython3 but useful for debugging:
	```Python
	import printutils as p
	p.returnFormatted = True
	log = open('log.txt', 'a')
	log.write(printf('This is important text that will be written to stdout and to a log file...\n'))
	# ...
	log.close()
	```
+ **outf**:
	The function to call when printing the text. Defaults to the print function. It can be useful to replace
	it with the **sys.stdout.write** function:
	```Python
	import printutils as p
	from sys.stdout import write
	p.outf = write
	```
