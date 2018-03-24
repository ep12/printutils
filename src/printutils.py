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
__version__ = '1.0.1'
__description__ = 'Various print utils for python3'
__keywords__ = 'utils development print output'

from inspect import currentframe, getmro, isclass, isfunction
import regex as _regex


returnFormatted = False
warnOnError = True
outf = print
outopt = {'end': ''}
allowExec = False
warnOnDenial = True
returnOnDenial = False


eeregex = '(?P<todo>' \
	+ '((^|[^\\\\])(\$|!)((\w+[\w\d=-]*)|(?<rec>\((?:[^()]++|(?&rec))*\))))' \
	+ '|(^|[^\\\\])({[^}]+}))'
_fmtspec = '((?P<fill>.?)(?P<align>[0<>\\^]))?' \
	+ '(?P<sign>[ +-])?' \
	+ '(?P<altform>[#])?' \
	+ '(?P<width>[\d]+)?' \
	+ ',?(\\.(?P<precision>[\d]+))?' \
	+ '(?P<type>[bcdeEfFgGnosxX])?'
_fmtregex = '(?P<fieldname>[\d\w]+)' \
	+ '(\\.(?P<attrname>\w*)|(\[(?P<elindex>[^\\]]*)\]))?' \
	+ '(!(?P<conv>[rsa]))?' \
	+ '(:' + _fmtspec + ')?'


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
	matches = [x[0] for x in _regex.findall(eeregex, tmp, flags=_regex.VERBOSE + _regex.MULTILINE)]
	# print('TODO matches:\n%s' % matches)  # DEBUG
	for m in matches:
		if m.startswith('\\'):
			print('ERROR: %r' % m)
		if not (m.startswith('$') or m.startswith('!') or m.startswith('{')):
			m2 = m[1:]
		else:
			m2 = m
		# print(repr(m), repr(m2))  # DEBUG
		# print('\n', tmp, m, m2)
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
			if m2.startswith('$(') and m.endswith(')'):
				m3 = m2[2:-1]
			else:
				m3 = m2[1:]
			# print('eval(%r)' % m3)  # DEBUG
			r = str(eval(m3, dg, dl))
		elif m2.startswith('{') and m2.endswith('}'):  # BUG: Will not work on {0!r: <7} etc.
			# print('eval(%r)' % m2[1:-1]) # DEBUG
			m3 = m2[1:-1]
			if bool(_regex.fullmatch(_fmtregex, m3)):
				try:
					r = ('{%s}' % m3).format(*args, **d)
				except IndexError:
					r = '[FAILED]' * warnOnError
			else:
				r = str(eval(m3, dg, dl))
		else:
			r = ''
		# print('m2: %r, %r -> %r' % (m2, m, m[0] * (m2 != m) + r))
		tmp = tmp.replace(m, m[0] * (m2 != m) + r)
	# tmp = tmp.format(fmt, *args, **d)
	tmp = tmp.replace('\$', '$').replace('\!', '!').replace('\{', '{')
	if outopt is None:
		outf(tmp)
	else:
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
