# -*- coding: utf-8 -*-
'''
Various utilities for printing in python3.

Example 1:
==========
1 import printutils as _p
2 printf = _p.printf
3 x = 18
4 printf('The square of $x is $(x**2) which is $(["not", "very"][x>100]) big!\n', 'stdout')
5 printf('[bluefg;whitebg]Info:[reset] Formatting text is now easy!\n', 'stdout')
6 printf('If [greenfg]colors[reset] are not supported, they are not displayed!\n', 'stdout')

Example 2:
==========
1 import printutils as _p
2 printf = _p._out_printf
3 errprintf = _p._err_printf
4 # NOTE: This will suppress any return values!
5 errprintf('[redfg]ERROR:[reset] not enough confusion:\nNo dest argument required anymore!\n')
'''
__all__ = ['printf', 'colorSettings', 'forceColors', 'format', 'CUP', 'SGR']
__author__ = 'ep12'
__email__ = ''
__license__ = 'MIT'
__title__ = 'printutils'
__url__ = 'https://github.com/ep12/printutils'
__version__ = '1.0.2'
__description__ = 'Various print utils for python3'
__keywords__ = 'utils development print output'

from inspect import currentframe, getmro, isclass, isfunction
import regex as _regex
import os as _os
import sys as _sys
import platform as _platform
import time as _time


if _platform.system() is 'Windows':
	import msvcrt as _get
else:
	try:
		import getch as _get
	except ImportError:
		print('\nMake sure that you have getch installed: pip3 install -U getch.')
		system(1)


def _fdconv(fd):
	if isinstance(fd, str):
		if 'stdin' in fd.lower():
			return _sys.stdin
		if 'stdout' in fd.lower():
			return _sys.stdout
		if 'stderr' in fd.lower():
			return _sys.stderr
		else:
			raise ValueError("fd not in ['stdin', 'stdout', 'stderr']!")
	elif fd is _sys.stdin:
		return 'stdin'
	elif fd is _sys.stdout:
		return 'stdout'
	elif fd is _sys.stderr:
		return 'stderr'
	else:
		raise ValueError('fd must be a string or a file descriptor!')


_g = globals()['__builtins__']
# retfmt = [None, '(fmt, ret, errs)']['display' not in globals()['__builtins__']]
_retfmt_dbg = '(fmt, dest, matches, errs, ret)'
retfmt = [None, _retfmt_dbg][hasattr(_sys.stdout, 'isatty') and _sys.stdout.isatty() is False]
outopt = {'end': ''}
allowExec = False
warnOnFail = True

useColors = {'stdout': False, 'stderr': False, 'all': False, 'any': False, 'format': False}


def initColors():
	for fd in [_sys.stdout, _sys.stderr]:
		if (hasattr(fd, 'isatty') and fd.isatty()) or ('TERM' in _os.environ and _os.environ['TERM'] is 'ANSI'):
			if _platform.system() is 'Windows':
				if 'CONEMUANSI' in _os.environ and _os.environ['CONEMUANSI'] == 'ON':
					useColors[_fdconv(fd)] = True
				elif 'TERM' in _os.environ and _os.environ['TERM'] == 'ANSI':
					useColors[_fdconv(fd)] = True
				else:
					useColors[_fdconv(fd)] = False
			else:
				useColors[_fdconv(fd)] = True
		else:
			useColors[_fdconv(fd)] = False

	useColors['all'] = useColors['stdout'] and useColors['stderr']
	useColors['any'] = useColors['stdout'] or useColors['stderr']
	useColors['format'] = useColors['all']


initColors()


def getGlobals():
	return globals()


def colorSettings():
	for x in useColors:
		printf('{x: >6}: Colors are $(["dis", "en"][useColors[x]])abled.\n', 'stdout', x=x)


def forceColors():
	for x in useColors:
		useColors[x] = True


_ansi = {
	'CSI': '\x1b[',        # Control Sequence Introducer
	'CUU': '\x1b[%dA',     # CUrsor Up (n=1)
	'CUD': '\x1b[%dB',     # CUrsor Down (n=1)
	'CUF': '\x1b[%dC',     # CUrsor Foward (n=1)
	'CUB': '\x1b[%dD',     # CUrsor Back (n=1)
	'CNL': '\x1b[%dE',     # Cursor Next Line (n=1)
	'CPL': '\x1b[%dF',     # Cursor Previous Line (n=1)
	'CHA': '\x1b[%dG',     # Cursor Horizontal Absolute (n=1)
	'CUP': '\x1b[%d;%dH',  # CUrsor Position (row=1, column=1)
	'ED': '\x1b[%dJ',      # Erase Display (n=0) (0: CUP-END, 1: BEGIN-CUP, 2: Entire screen, 3: Entire screen + scollback (xterm))
	'EL': '\x1b[%dK',      # Erase Line (n=0) (0: CUP-EOL, 1: SOL-CUP, 2: Entire line)
	'SU': '\x1b[%dS',      # Scroll Up (n=1)
	'SD': '\x1b[%dT',      # Scroll Down (n=1)
	'HVP': '\x1b[%d;%df',  # Horizontal Vertical Position (same as CUP)
	'SGR': '\x1b[%sm',     # Set Graphics Rendition. NOTE: useful for colors!
	'AUX_ON': '\x1b[5i',   # Enable aux port for printer
	'AUX_OFF': '\x1b[6i',  # Disable aux port for print
	'DSR': '\x1b[6n',      # Device Status Report. NOTE: reports CUP as '\x1b[row;colR' through stdin
	'SCP': '\x1b[s',       # Save cursor position
	'RCP': '\x1b[u',       # Restore cursor position
	'CSH': '\x1b[?25h',    # NOTE: SHow Cursor
	'CHD': '\x1b[?25l',    # NOTE: HiDe Cursor
	'EAB': '\x1b[?1049h',  # Enable Alternative screen Buffer
	'DAB': '\x1b[?1049l',  # Disable Alternative screen Buffer
	'EBP': '\x1b[?2004h',  # Enable Bracketed Paste mode
	'DBP': '\x1b[?2004l',  # Disable Bracketed Paste mode
}
_sgr = {
	'normal': 0, 'reset': 0,
	'bold': 1,
	'faint': 2,
	'italic': 3,
	'underline': 4, 'underlined': 4,
	'blink': 5, 'flashing': 5,
	'fastblink': 6,
	'reverse': 7, 'reversed': 7, 'negative': 7,
	'conceal': 8, 'concealed': 8, 'hide': 8,
	'crossed-out': 9,
	'font0': 10, 'font1': 11, 'font2': 12, 'font3': 13, 'font4': 14,
	'font5': 15, 'font6': 16, 'font7': 17, 'font8': 18, 'font9': 19,
	'fraktur': 20,
	'not-bold': 21, 'bold-off': 21, 'underline-double': 21, 'double-underlined': 21,
	'normal-color': 22, 'normal-intensity': 22,
	'not-italic': 23, 'italic-off': 23,
	'not-underlined': 24, 'no-underline': 24, 'underline-off': 24,
	'blink-off': 25,
	'positive': 27,
	'conceal-off': 28, 'show': 28,
	'not-crossed-out': 29,
	'blackfg': 30,
	'redfg': 31,
	'greenfg': 32,
	'orangefg': 33,
	'bluefg': 34,
	'purplefg': 35,
	'cyanfg': 36,
	'greyfg': 37,
	# 38: extended fg colors: 38;2;r;g;b or 38;5;n
	'normalfg': 39,
	'blackbg': 40,
	'redbg': 41,
	'greenbg': 42,
	'orangebg': 43,
	'bluebg': 44,
	'purplebg': 45,
	'cyanbg': 46,
	'greyfg': 47,
	# 48: extended bg colors: 48;2;r;g;b or 48;5;n
	'normalbg': 49,
	'frame': 51, 'framed': 51,
	'encircle': 52, 'encircled': 52,
	'overline': 53, 'overlined': 53,
	'frame-off': 54, 'not-framed': 54,
	'overline-off': 55, 'not-overlined': 55,
	'dgreyfg': 90,
	'lredfg': 91,
	'lgreenfg': 92,
	'yellowfg': 93,
	'lbluefg': 94,
	'lpurplefg': 95,
	'turquoisefg': 96,
	'whitefg': 97,
	'dgreybg': 100,
	'lredbg': 101,
	'lgreenbg': 102,
	'yellowbg': 103,
	'lbluebg': 104,
	'lpurplebg': 105,
	'turquoisebg': 106,
	'whitebg': 107
}


def _getCursor():
	_sys.stdout.buffer.write(_ansi['DSR'].encode())
	_sys.stdout.buffer.flush()
	appendmode = False
	while True:
		x = _get.getch()
		if x is '\x1b':
			tmp = x
			appendmode = True
		elif appendmode:
			tmp += x
		if x is 'R':
			break
	return tmp


def CUP(row=None, col=None):
	'''CUP(row=None, col=None)
		If row and col are None, this function returns a tuple with the cursor position.
		Otherwise any value that is None is set to 1 and the function sets the cursor position.
	'''
	if row is None and col is None:
		return tuple([int(x) for x in _getCursor()[2:-1].split(';')])
	else:
		if row is None:
			row = 1
		if col is None:
			col = 1
		assert isinstance(row, int) and row > 0, 'row must be a positive integer'
		assert isinstance(col, int) and col > 0, 'col must be a positive integer'
		_sys.stdout.buffer.write((_ansi['CUP'] % (row, col)).encode())


def _extracolor(i):  # TODO
	if isinstance(i, str):
		if i.isdigit() and int(i) < 256 and int(i) >= 0:
			return '38;5;%s' % i
		elif all([x.lower() in '0123456789abcdef' for x in i]) and len(i) in [3, 6]:
			tup = [int((2 - (len(i) is 6)) * i[x:x + 2 - (len(i) is 3)], 16) for x in range(0, len(i), 2 - (len(i) is 3))]
			return '38;2;{};{};{}'.format(*t)
	elif isinstance(i, int) and i >= 0 and i < 256:
		return '38;5;%d' % i
	elif isinstance(i, bytes) and len(i) is 3:
		return '38;2;{};{};{}'.format(ord(i[0]), ord(i[1]), ord(i[2]))
	return ''


def ANSI(opt: str, dest=None):
	assert isinstance(opt, str)
	# TODO: FULL ANSI SUPPORT inside []
	return SGR(opt, dest)


def SGR(opt: str, dest=None):
	assert isinstance(opt, str)
	if dest is not None and useColors.get(dest, False):
		tmp = []
		fail = []
		for x in opt.split(';'):
			if x in _sgr:
				tmp.append(str(_sgr[x]))
			elif _extracolor(x):
				tmp.append(_extracolor(x))
			else:
				fail.append(x)
		return _ansi['SGR'] % ';'.join(tmp) + ('<FAILED: %s>' % ';'.join(fail)) * (len(fail) > 0)
	else:
		return ''


_eeregex = '(?P<todo>' \
	+ '((^|[^\\\\])(\$|!)((\w+[\w\d=-]*)|(?<rec>\((?:[^()]++|(?&rec))*\))))' \
	+ '|(^|[^\\\\])({[^}]+})' \
	+ '|(^|[^\\\\])(\[[-;\w\d\s]+\])' \
	+ ')'
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


def format(fmt: str, *args, **kwargs) -> str:
	'''format(fmt: str, *args, **kwargs)
		- fmt: str
			A string to format
		? *args
			Arguments to pass to the format function
		? **kwargs
			A dict with values to pass to the format function

		returns:
			The formatted output string.
	'''
	frame = kwargs.pop('_frame_', currentframe().f_back)
	return _format(fmt, 'format', frame, *args, **kwargs)[4]


def _format(fmt: str, dest: str, frame, *args, **kwargs):  # TODO:
	# TODO: update for to while for nested formatting...
	assert isinstance(fmt, str), 'fmt must be a string.'
	# frame = kwargs.pop('_frame_', currentframe().f_back)  # TODO: move to top-level fns:
	# format, printf, oprintf, eprintf
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
	ret = fmt
	errs = []
	matches = [x[0] for x in _regex.findall(_eeregex, ret, flags=_regex.VERBOSE + _regex.MULTILINE)]
	# print('TODO matches:\n%s' % matches)  # DEBUG
	for m in matches:
		if m.startswith('\\'):
			print('ERROR: %r' % m)
		if not (m.startswith('$') or m.startswith('!') or m.startswith('{') or m.startswith('[')):
			m2 = m[1:]
		else:
			if m.startswith('$[') or m.startswith('!['):
				m2 = m[1:]
			else:
				m2 = m
		# print(repr(m), repr(m2))  # DEBUG
		if m2.startswith('!'):
			# print('exec(%r)' % m2)  # DEBUG
			if m2.startswith('!(') and m2.endswith(')'):
				m3 = m2[2:-1]
			else:
				m3 = m2[1:]
			if allowExec:
				try:
					exec(m3, dg, dl)
				except Exception as e:
					errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
				r = ''
			else:
				r = ('[EXECUTION DENIED: %r]' % m3) * warnOnFail
		elif m2.startswith('$'):
			if m2.startswith('$(') and m.endswith(')'):
				m3 = m2[2:-1]
			else:
				m3 = m2[1:]
			# print('eval(%r)' % m3)  # DEBUG
			try:
				r = str(eval(m3, dg, dl))
			except Exception as e:
				errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
				r = ('[FAILED: %r]' % m3) * warnOnFail
		elif m2.startswith('{') and m2.endswith('}'):  # BUG: Will not work on {0!r: <7} etc.
			# print('eval(%r)' % m2[1:-1]) # DEBUG
			m3 = m2[1:-1]
			if bool(_regex.fullmatch(_fmtregex, m3)):
				try:
					r = ('{%s}' % m3).format(*args, **d)
				except Exception as e:
					r = ('[FAILED: %r]' % m3) * warnOnFail
					errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
			else:
				try:
					r = str(eval(m3, dg, dl))
				except Exception as e:
					r = ('[FAILED: %r]' % m3) * warnOnFail
					errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
		elif m2.startswith('[') and m2.endswith(']'):
			m3 = m2[1:-1]
			try:
				r = ANSI(m3, dest)
			except Exception as e:
				r = ('[FAILED: %r]' % m3) * warnOnFail
				errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
		else:
			r = ''
		# print('m2: %r, %r -> %r' % (m2, m, m[0] * (m2 != m) + r))
		ret = ret.replace(m, m[0] * (m2 != m) + r)
	# ret = ret.format(fmt, *args, **d)
	ret = ret.replace('\$', '$').replace('\!', '!').replace('\{', '{')
	return (fmt, dest, matches, errs, ret)


def _printf(fmt: str, dest: str, frame, *args, **kwargs):
	'''_printf(fmt: str, dest: str, *args, **kwargs)
		- fmt: str
			A string to format
		- dest: str
			Whether to write to 'stdout' or 'stderr'.
			If invalid, it won't be printed
		? *args
			Arguments to pass to the format function
		? **kwargs
			A dict with values to pass to the format function

		returns:
			eval(retfmt) if retfmt is not None.
			default for retfmt: '(fmt, ret, errs)' if not using ipython
			fmt: the input string.
			ret: the output string.
			errs: a list of errors and the state of the variables at this time.
			matches: a list of everything that is tried to be replaced.
	'''
	if dest in ['stdout', _sys.stdout]:
		outf = _sys.stdout.write
	elif dest in ['stderr', _sys.stderr]:
		outf = _sys.stderr.write
	else:
		outf = (lambda x: x)  # adding brackets bypasses flake E371 LOL
	fmt, dest, matches, errs, ret = _format(fmt, dest, frame, *args, **kwargs)
	outf(ret)
	if retfmt is not None:
		try:
			return eval(retfmt)
		except Exception as e:
			return e


def oprintf(fmt: str, *args, **kwargs):
	frame = kwargs.pop('_frame_', currentframe().f_back)
	_printf(fmt, 'stdout', frame, *args, **kwargs)


def eprintf(fmt: str, *args, **kwargs):
	frame = kwargs.pop('_frame_', currentframe().f_back)
	_printf(fmt, 'stderr', frame, *args, **kwargs)


def hook(sysobj):
	'''hook(sysobj)
	adds the printf function to sysobj.stdout and sysobj.stderr
	'''
	assert sysobj is _sys, 'sysobj must me the sys module.'
	sysobj.stdout.__dict__.update([('printf', oprintf)])
	sysobj.stderr.__dict__.update([('printf', eprintf)])
