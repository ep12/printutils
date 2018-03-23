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

returnFormatted = False
outf = print
eeregex = '(?P<todo>((^|[^\\\\])(\$|!)([^() ]+|(?<rec>\((?:[^()]++|(?&rec))*\))))|(^|[^\\\\])({.+}))'
outopt = {'end': ''}
allowExec = False
warnOnDenial = True
returnOnDenial = False


def printf(fmt: str, *args, **kwargs) -> str:
	'''printf(fmt: str, *args, **kwargs)
		+ fmt
	'''
	assert isinstance(fmt, str), 'fmt must be a string.'
	frame = kwargs.pop('_frame_', currentframe().f_back)
	dl = locals()
	dg = globals()
	if kwargs:
		dl.update(**kwargs)
	if frame.f_locals:
		dl.update(**frame.f_locals)
	if frame.f_globals:
		dg.update(**frame.f_globals)
	# print(dl, dg)  # DEBUG
	d = dg.copy()
	d.update(dl)
	tmp = fmt
	matches = [x[0] for x in regex.findall(eeregex, tmp, flags=regex.VERBOSE + regex.MULTILINE)]
	# TODO: {eval} and $eval and !exec
	for m in matches:
		if not (m.startswith('$') or m.startswith('!') or m.startswith('{')):
			m2 = m[1:]
		else:
			m2 = m
		# print(repr(m), repr(m2))  # DEBUG
		if m2.startswith('!'):
			# print('exec(%r)' % m2)  # DEBUG
			if allowExec:
				if m2.startswith('!(') and m2.endswith(')'):
					m3 = m2[2:-1]
				else:
					m3 = m2[1:]
				exec(m3, dg, dl)
				r = ''
			else:
				if returnOnDenial:
					return False
				r = '[EXECUTION DENIED]' * warnOnDenial
		elif m2.startswith('$'):
			if m.startswith('$(') and m.endswith(')'):
				m3 = m2[2:-1]
			else:
				m3 = m2[1:]
			# print('eval(%r)' % m3)  # DEBUG
			r = str(eval(m3, dg, dl))
		elif m2.startswith('{') and m2.endswith('}'):  # BUG: Will not work on {0!r: <7} etc.
			# print('eval(%r)' % m2[1:-1]) # DEBUG
			r = str(eval(m2[1:-1], dg, dl))
		else:
			r = ''
		tmp = tmp.replace(m2, r)
	tmp = tmp.format(fmt, *args, **d)
	outf(tmp, **outopt)
	if returnFormatted:
		return tmp


# Feature requests welcome.

if __name__ == '__main__':
	a = 5
	returnOnDenial = True
	printf('Execution is $("not "*(allowExec is False))allowed.\n')
	printf('!(exit(0xff))\n')
	printf('a=$(chr(123))a$(chr(125))\n')
