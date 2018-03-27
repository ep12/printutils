import sys as _sys
import os as _os
import signal as _s


def pipimport(name: str):
	try:
		return __import__(name)
	except ImportError:
		print('Error: could not import %r!\nInstall using \'pip install -U %s\'.' % (name, name))


def getch(timeout: float=-1, visible: bool=False):
	if _sys.platform == 'linux':
		g = pipimport('getch')
		if timeout > 0.0:
			def alrm(sig: int, frame):
				raise Exception('timed out')
			tmpalh = None
			if 'SIGALRM' in _s.Handlers.__dict__:
				tmpalh = _s.Handlers.__dict__['SIGALRM']
			_s.signal(_s.SIGALRM, alrm)
			_s.alarm(timeout)
		try:
			if visible:
				x = g.getche()
			else:
				x = g.getch()
		except Exception:
			x = ''
		if timeout > 0.0 and tmpalh is not None:
			_s.Handlers.SIGALRM = tmpalh
		return x
	elif _sys.platform is 'win32':
		import msvcrt as g
		# TODO
		
		return x


def getBuffer(visible: bool=False):
	tmp = ''
	while True:
		x = getch(0.01, visible)
		if x == '':
			return tmp
		else:
			tmp += x
