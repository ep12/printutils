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
printf('{a}')
# 5
```

The `printf` function has more advantages from python 3.6:
+ `eval` inside fmtstr, wrapped in a julia-like syntax:
```Python
from printutils import printf
a = 5
printf('$(a is 5)')
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
