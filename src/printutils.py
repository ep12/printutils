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
__version__ = '1.0.3'
__description__ = 'Various print utils for python3'
__keywords__ = 'utils development print output'

from inspect import currentframe, getmro, isclass, isfunction
import regex as _regex
import re as _re
import os as _os
import sys as _sys
import platform as _platform
import time as _time
import utils as ut
# import colorama as _colorama
# _get = None


_retfmt_dbg = '(fmt, dest, matches, errs, ret)'
retfmt = [None, _retfmt_dbg][hasattr(_sys.stdout, 'isatty') and _sys.stdout.isatty() is False]
outopt = {'end': ''}
allowExec = False
warnOnFail = True
ut.debug = False
dbg = ut.dbg

useColors = ut.initColors()

_eeregex = '(?P<todo>' \
	+ '((^|[^\\\\])(\$|!)((\w+[\w\d=-]*)|(?<rec>\((?:[^()]++|(?&rec))*\))))' \
	+ '|(^|[^\\\\])({[^}]+})' \
	+ '|(^|[^\\\\])(\[[^\]]+\])' \
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


# def _getInit():
# 	global _get
# 	if _get is None:
# 		if _platform.system() is 'Windows':
# 			_get = __import__('msvcrt')
# 		else:
# 			try:
# 				_get = __import__('getch')
# 			except ImportError:
# 				print('Getch is required to read the cursor position.\nMake sure that you have it installed: pip3 install -U getch.')
# 				system(1)


def colorSettings():
	'Displays the current color settings'
	for x in useColors:
		oprintf('{x: >8}: Colors are $(["dis", "en"][useColors[x]])abled.\n', x=x)


def forceColors():
	for x in useColors:
		useColors[x] = True


# That should be part of themedevtools
# def colorTable():
# 	for i in range(0, 256):
# 		oprintf('{i: >3}: [bg=%d]   [reset]' % i)
# 		oprintf('\n' * (i % 16 is 15))
#
#
# def miniColorTable(number=False):
# 	for i in range(0, 256):
# 		oprintf('[bg=%d]%2x[reset]' % (i, i))
# 		oprintf('\n' * (i % 16 is 15))
#
#
# def themeColors(number=False):
# 	for i in range(0, 32):
# 		oprintf('[bg=%d]%2x[reset]' % (i, i))
# 		oprintf('\n' * (i % 16 is 15))
# 	for i in range(32, 232):
# 		oprintf('[bg=%d]%2x[reset]' % (i, i))
# 		oprintf('\n' * ((i - 32) % 36 is 35))
# 	oprintf('\n')
# 	for i in range(232, 256):
# 		oprintf('[bg=%d]%2x[reset]' % (i, i))
#
#
# def genColors():
# 	c = [(0, 0, 0)] * 256
# 	c[1] = (192, 0, 0)
# 	c[2] = (0, 192, 0)
# 	c[3] = (192, 160, 0)
# 	c[4] = (0, 0, 192)
# 	c[5] = (192, 0, 192)
# 	c[6] = (0, 192, 192)
#
# 	for n in range(16, 232):
# 		y = int(0.2 * ((n - 16) // 36))
# 		z = int(0.2 * ((n - 16) % 36 // 6))
# 		x = int(0.2 * ((n - 16) % 6))
# 		c[n] = (x, y, z)
# 	for n in range(232, 256):
# 		c[n] = int(255 / 25 * (n - 25))


def _extracolor(j):  # TODO!!!!!!!!!!!!!!!
	if isinstance(j, str):
		if j.startswith('bg='):
			dbg('Setting background color')
			target = 1
			i = j[3:]
		elif j.startswith('fg='):
			dbg('Setting foreground color')
			target = 0
			i = j[3:]
		else:
			dbg('Setting foreground color')
			target = 0
			i = j
		if i.isdigit() and int(i) < 256 and int(i) >= 0:
			return '%d;5;%s' % (38 + 10 * target, i)
		elif i.startswith('#') and all([x.lower() in '0123456789abcdef' for x in i[1:]]) and len(i[1:]) in [3, 6]:
			i = i[1:]
			tup = [int((2 - (len(i) is 6)) * i[x:x + 2 - (len(i) is 3)], 16) for x in range(0, len(i), 2 - (len(i) is 3))]
			return '{};2;{};{};{}'.format(38 + 10 * target, *tup)
		elif all([x.lower() in '0123456789abcdef' for x in i]) and len(i) in [3, 6]:
			tup = [int((2 - (len(i) is 6)) * i[x:x + 2 - (len(i) is 3)], 16) for x in range(0, len(i), 2 - (len(i) is 3))]
			return '{};2;{};{};{}'.format(38 + 10 * target, *tup)
	elif isinstance(j, int) and i >= 0 and i < 256:
		return '38;5;%d' % j
	elif isinstance(j, bytes) and len(j) is 3:
		return '38;2;{};{};{}'.format(ord(j[0]), ord(j[1]), ord(j[2]))
	return ''


def ANSI(opt: str, dest=None):
	assert isinstance(opt, str)
	# TODO: FULL ANSI SUPPORT inside []
	dbg(repr(opt))
	if dest is not None and useColors.get(dest, False):
		tmp = ''
		last = None  # 0=sgr, 1=ANSI
		fail = []

		def add(text, sgr):
			nonlocal tmp, last
			if sgr:
				if last is None or last is 1:
					tmp += '\x1b['
					last = 0
				else:
					tmp += ';'
				tmp += text
			else:
				if last is 0:
					tmp += 'm'
					last = 0
				tmp += text

		for x in opt.split(';'):
			dbg(repr(x))
			if x in _sgr:
				add(str(_sgr[x]), True)
			elif len(_extracolor(x)) > 0:
				add(_extracolor(x), True)
			else:
				y = x.split(',')
				if len(y) > 1 and y[0] in _ansi and _ansi[y[0]].count('%') < len(y):
					add(_ansi[y[0]] % tuple(y[1:]), False)
				elif len(y) is 1 and y[0] in _ansi:
					add(_ansi[y[0]], False)
				else:
					fail.append(x)
		if last is 0:
			tmp += 'm'
		return tmp + ('[FAILED: %s]' % ';'.join(fail)) * (len(fail) > 0)
	else:
		return ''


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
	dbg('TODO matches:\n%s' % matches)  # DEBUG
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
		dbg(repr(m), repr(m2))  # DEBUG
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
					dbg(e)
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
				dbg(e)
				r = ('[FAILED: %r]' % m3) * warnOnFail
		elif m2.startswith('{') and m2.endswith('}'):  # BUG: Will not work on {0!r: <7} etc.
			# print('eval(%r)' % m2[1:-1]) # DEBUG
			m3 = m2[1:-1]
			if bool(_regex.fullmatch(_fmtregex, m3)):
				try:
					r = ('{%s}' % m3).format(*args, **d)
				except Exception as e:
					r = ('[FAILED: %r]' % m3) * warnOnFail
					dbg(e)
					errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
			else:
				try:
					r = str(eval(m3, dg, dl))
				except Exception as e:
					r = ('[FAILED: %r]' % m3) * warnOnFail
					dbg(e)
					errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
		elif m2.startswith('[') and m2.endswith(']'):
			m3 = m2[1:-1]
			try:
				r = ANSI(m3, dest)
			except Exception as e:
				r = ('[FAILED: %r]' % m3) * warnOnFail
				dbg(e)
				errs.append([e, {'m': m, 'm2': m2, 'm3': m3, 'ret': ret}])
		else:
			r = ''
		# print('m2: %r, %r -> %r' % (m2, m, m[0] * (m2 != m) + r))
		ret = ret.replace(m, m[0] * (m2 != m) + r)
	# ret = ret.format(fmt, *args, **d)
	ret = ret.replace('\$', '$').replace('\!', '!').replace('\{', '{')
	return (fmt, dest, matches, errs, ret)


def _printf(fmt: str, dest: str, frame, *args, **kwargs):
	if dest in ['stdout', _sys.stdout]:
		outf = _sys.stdout.write
	elif dest in ['stderr', _sys.stderr]:
		outf = _sys.stderr.write
	else:
		outf = (lambda x: x)  # adding brackets bypasses flake E371 LOL
	fmt, dest, matches, errs, ret = _format(fmt, dest, frame, *args, **kwargs)
	outf(ret)
	if outopt.get('end'):
		outf(outopt['end'])
	if retfmt is not None:
		try:
			return eval(retfmt)
		except Exception as e:
			return e


def oprintf(fmt: str, *args, **kwargs):
	'''oprintf(fmt: str, *args, **kwargs)
		Prints a formatted string to stdout.
		- fmt: str
			A string to format
		? *args
			Arguments to pass to the format function
		? **kwargs
			A dict with values to pass to the format function
	'''
	frame = kwargs.pop('_frame_', currentframe().f_back)
	_printf(fmt, 'stdout', frame, *args, **kwargs)


def eprintf(fmt: str, *args, **kwargs):
	'''eprintf(fmt: str, *args, **kwargs)
		Prints a formatted string to stderr.
		- fmt: str
			A string to format
		? *args
			Arguments to pass to the format function
		? **kwargs
			A dict with values to pass to the format function
	'''
	frame = kwargs.pop('_frame_', currentframe().f_back)
	_printf(fmt, 'stderr', frame, *args, **kwargs)


def hook(sysobj):
	'''hook(sysobj)
	adds the printf function to sysobj.stdout and sysobj.stderr
	'''
	assert sysobj is _sys, 'sysobj must me the sys module.'
	sysobj.stdout.__dict__.update([('printf', oprintf)])
	sysobj.stderr.__dict__.update([('printf', eprintf)])
