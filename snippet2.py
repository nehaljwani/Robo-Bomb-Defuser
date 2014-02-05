class curses_window:
	""" Creates A Window """
	def __init__(self):
		curses.curs_set(0)
		curses.noecho()
		self.win=curses.newwin(LINES-4,COLS-4,2,2)
		self.win.clear()
		self.win.refresh()
		self.win.keypad(1)
