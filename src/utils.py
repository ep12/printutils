import sys as _sys
import os as _os
import signal as _s


def pipimport(name: str):
	try:
		return __import__(name)
	except ImportError:
		print('Error: could not import %r!\nInstall using \'pip install -U %s\'.' % (name, name))


def dbg(*args):
	if debug:
		print('DEBUG: ', end='')
		print(*args)


if _sys.platform == 'linux':
	_g = pipimport('getch')
elif _sys.platform is 'win32':
	_g = pipimport('msvcrt')


def getch(timeout: float=-1, visible: bool=False, readf=None):
	if _sys.platform == 'linux':
		if readf is None:
			readf = [_g.getch, _g.getche][visible]
		if timeout > 0:
			if isinstance(timeout, float):
				timeout = int(timeout)
			if timeout is 0:
				timeout = 1

			def alrm(sig: int, frame):
				return ''

			tmpalh = None
			if hasattr(_s, 'Handlers') and 'SIGALRM' in _s.Handlers.__dict__:
				tmpalh = _s.Handlers.__dict__['SIGALRM']
			_s.signal(_s.SIGALRM, alrm)
			_s.alarm(timeout)
		try:
			x = readf()
		except (OverflowError, Exception):
			x = ''
		if timeout > 0.0 and tmpalh is not None:
			_s.Handlers.SIGALRM = tmpalh
		return x
	elif _sys.platform is 'win32':
		if readf is None:
			readf = [_g.getch, _g.getche][visible]
		if timeout > 0.0:
			import threading as t

			class KeybThread(t.Thread):
				def run(self):
					self.timedout = False
					self.x = ''
					while True:
						if self.x or self.timedout:
							break
						if g.kbhit():
							self.x = readf()
			x = ''
			kt = KeybThread()
			kt.start()
			kt.join(timeout)
			kt.timedout = True
			return kt.x
		else:
			x = readf()
		return x


def getBuffer(visible: bool=False):
	tmp = ''
	while True:
		x = getch(0.01, visible)
		if x == '':
			return tmp
		else:
			tmp += x


def fdconv(fd, target=None):
	if target is not None and isinstance(target, str):
		if target.lower() in ['string', 's']:
			if not isinstance(fd, str):
				return _fdconv(fd)
			else:
				return fd
		else:
			if isinstance(fd, str):
				return _fdconv(fd)
			else:
				return fd
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


def initColors():
	'''initColors()
	Tests if colors are supported by the device / terminal and sets the useColors options accordingly.
	'''
	useColors = {'stdout': False, 'stderr': False, 'all': False, 'any': False, 'format': False}
	for fd in [_sys.stdout, _sys.stderr]:
		if (hasattr(fd, 'isatty') and fd.isatty()) or ('TERM' in _os.environ and _os.environ['TERM'] is 'ANSI'):
			if _platform.system() is 'Windows':
				if 'CONEMUANSI' in _os.environ and _os.environ['CONEMUANSI'] == 'ON':
					useColors[_u.fdconv(fd)] = True
				elif 'TERM' in _os.environ and _os.environ['TERM'] == 'ANSI':
					useColors[_u.fdconv(fd)] = True
				else:
					useColors[_u.fdconv(fd)] = False
			else:
				useColors[_u.fdconv(fd)] = True
		else:
			useColors[_u.fdconv(fd)] = False

	useColors['all'] = useColors['stdout'] and useColors['stderr']
	useColors['any'] = useColors['stdout'] or useColors['stderr']
	useColors['format'] = useColors['all']
	return useColors


def _getCursor():
	if _sys.platform == 'win32':
		raise NotImplementedError('Feature not available')
	appendmode = False
	tmp = ''
	_sys.stdout.buffer.write(_ansi['DSR'].encode())
	_sys.stdout.buffer.flush()
	while True:
		try:
			# if _sys.platform is 'win32':
			# 	oprintf('[bluefg;whitebg] INFO [reset] Trying to detect cursor postion. Press enter:\r')
			# 	tmp = _sys.stdin.readline()  # Windows
			# 	oprintf(_ansi['EL'] % 0)
			# 	break
			# else:
			x = getch(0.01)
		except KeyboardInterrupt:
			tmp = x = ''
		if x is '\x1b':
			tmp = x
			appendmode = True
		elif appendmode:
			tmp += x
		if x in ['R', '\n', '']:
			break
	return tmp


def cursorPosition(row=None, col=None):
	'''cursorPosition(row=None, col=None)
		If row and col are None, this function returns a tuple with the cursor position.
		Otherwise any value that is None is set to 1 and the function sets the cursor position.
	'''
	if row is None and col is None:
		try:
			r = _getCursor()
		except NotImplementedError:
			r = ''
		if r:
			return tuple([int(x) for x in r[2:-1].split(';')])
		else:
			return (False, False)
	else:
		if row is None:
			row = 1
		if col is None:
			col = 1
		assert isinstance(row, int) and row > 0, 'row must be a positive integer'
		assert isinstance(col, int) and col > 0, 'col must be a positive integer'
		_sys.stdout.buffer.write((_ansi['CUP'] % (row, col)).encode())


def OSC_color_available(n: int=0) -> (bool, str, tuple):
	assert isinstance(n, int) and n >= 0 and n < 256
	if _sys.platform in ['darwin', 'linux']:
		s = _time.time()
		appendmode = False
		tmp = ''
		_sys.stdout.buffer.write(('\x1b]4;%d;?\a' % n).encode())
		_sys.stdout.buffer.flush()
		while True:
			x = getch(0.1, True)  # BUG: Doesn't work on windows
			# x = ut.getch(-1, True)
			print(repr(x))
			if len(x) is 0:
				break
			if x is '\x1b':
				tmp = x
				appendmode = True
			elif appendmode:
				tmp += x
			if x in ['\a', '\n', '']:
				break
		if tmp not in ['\n', '']:
			print(repr(tmp))
			try:
				m = _re.match('\x1b]4;[\\d]+;rgb:(\d{2})(\d{2})/(\d{2})(\d{2})/(\d{2})(\d{2})\x07', tmp).groups()
				rgb = (int(m[0]) << 4 + int(m[1]), int(m[2]) << 4 + int(m[3]), int(m[4]) << 4 + int(m[5]))
			except Exception:
				rgb = (0x00, 0x00, 0x00)
			return (True, tmp, rgb)
	return (False, None, (0x00, 0x00, 0x00))


def getColorRGB(n: int=0) -> tuple:
	success, dummy, rgb = OSC_color_available(n)
	if success:
		return rgb


def testBuiltinColors() -> int:
	'''testBuiltinColors()
	returns the number of supported colors or -1 if terminal does not support the detection.
	'''
	if not _OSC_available()[0]:
		return -1
	mn, mx = 0, 256
	x = 0
	while x + 1 < mx:
		n = _time.time()
		print('\r' + ((int(4 * n) % 2) * ' ' + '.').ljust(3) + 3 * '\b', end='')
		x = (mn + mx) // 2
		r = OSC_color_available(x)[0]
		if r:
			mn = x
		else:
			mx = x
	print('   \r', end='')
	return x
