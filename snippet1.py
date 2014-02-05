class curses_screen:
	""" Creates A Screen """
	def __enter__(self):
		self.stdscr = curses.initscr()
		curses.cbreak()
		self.stdscr.clear()
		curses.noecho()
		self.stdscr.keypad(1)
		self.stdscr.border(0)
		return self.stdscr
	def __exit__(self,a,b,c):
		curses.echo()
		curses.endwin()
		self.stdscr.getch()
		self.stdscr.clear()
		self.stdscr.refresh()
