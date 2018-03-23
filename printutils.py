# -*- coding: utf-8 -*-
'''
Various utilities for printing in python3.
'''
__all__ = ['printf']
__author__ = 'ep12'
__email__ = ''
__license__ = 'MIT'
__title__ = 'printutils'
__url__ = 'https://github.com/ep12/printutils'
__version__ = '1.0.0'

import sys
from inspect import currentframe, getmro, isclass, isfunction
import regex


allowExec = False
warnOnDenial = True
returnOnDenial = False


def printf(fmt: str, *args, **kwargs) -> str:
	'''printf(fmt: str, *args, **kwargs)
		+ fmt
	'''
	assert isinstance(fmt, str), 'fmt must be a string.'
	frame = kwargs.pop('_frame_', currentframe().f_back)
	d = {}
	if kwargs:
		d.update(**kwargs)
	if frame.f_locals:
		d.update(**frame.f_locals)
	if frame.f_globals:
		d.update(**frame.f_globals)
	tmp = fmt.format(fmt, *args, **d)
	matches = [x[0] for x in regex.findall('((\$|\!)(?<rec>\((?:[^()]++|(?&rec))*\)))', tmp, flags=regex.VERBOSE)]
	for m in matches:
		if m[0] is '!':
			if allowExec:
				exec(m[2:-1])
				r = ''
			else:
				if returnOnDenial:
					return False
				r = '[EXECUTION DENIED]' * warnOnDenial
		else:
			r = str(eval(m[2:-1]))
		tmp = tmp.replace(m, r)
	tmp = tmp.format(fmt, *args, **d)
	print(tmp, end='')
	return tmp


# Feature requests welcome.

if __name__ == '__main__':
	a = 5
	returnOnDenial = True
	printf('Execution is $("not "*(allowExec is False))allowed.\n')
	printf('!(exit(0xff))\n')
	printf('a=$(chr(123))a$(chr(125))\n')
