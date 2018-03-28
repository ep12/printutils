OSC_VALID = '0123456789abcdefghijklmnopqrstuvwxyz;-,#"'

ansi = {
	'CSI': '\x1b[',        # Control Sequence Introducer
	'CUU': '\x1b[%sA',     # CUrsor Up (n=1)
	'CUD': '\x1b[%sB',     # CUrsor Down (n=1)
	'CUF': '\x1b[%sC',     # CUrsor Foward (n=1)
	'CUB': '\x1b[%sD',     # CUrsor Back (n=1)
	'CNL': '\x1b[%sE',     # Cursor Next Line (n=1)
	'CPL': '\x1b[%sF',     # Cursor Previous Line (n=1)
	'CHA': '\x1b[%sG',     # Cursor Horizontal Absolute (n=1)
	'CUP': '\x1b[%s;%sH',  # CUrsor Position (row=1, column=1)
	'ED': '\x1b[%sJ',      # Erase Display (n=0) (0: CUP-END, 1: BEGIN-CUP, 2: Entire screen, 3: Entire screen + scollback (xterm))
	'EL': '\x1b[%sK',      # Erase Line (n=0) (0: CUP-EOL, 1: SOL-CUP, 2: Entire line)
	'SU': '\x1b[%sS',      # Scroll Up (n=1)
	'SD': '\x1b[%sT',      # Scroll Down (n=1)
	'HVP': '\x1b[%s;%sf',  # Horizontal Vertical Position (same as CUP)
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
sgr = {
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
