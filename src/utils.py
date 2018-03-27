import sys as _sys
import os as _os
import signal as _s


def pipimport(name: str):
	try:
		return __import__(name)
	except ImportError:
		print('Error: could not import %r!\nInstall using \'pip install -U %s\'.' % (name, name))


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
