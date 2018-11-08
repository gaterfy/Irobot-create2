#!/usr/bin/env python
#-*-coding:utf-8-*-

import curses
# import curses.textpad
import locale
import time
import pycreate2
#from sparkline import sparkify


class Window(object):
	def __init__(self, title, w, h, y, x):
		self.win = curses.newwin(h, w, y, x)
		self.win.border(0)
		self.win.addstr(0, 1, title)


class CommandWindow(Window):
	def __init__(self, y, x):
		Window.__init__(self, 'Commands', 15, 6, y, x)

	def refresh(self):
		self.win.border(0)
		self.win.addstr(1, 1, '[{} ] Forward'.format(u'\u21E7'.encode('utf-8')))
		self.win.addstr(2, 1, '[{} ] Reverse'.format(u'\u21E9'.encode('utf-8')))
		self.win.addstr(3, 1, '[{} ] Left'.format(u'\u21E6'.encode('utf-8')))
		self.win.addstr(4, 1, '[{} ] Right'.format(u'\u21E8'.encode('utf-8')))
		self.win.refresh()


class LightBumperWindow(Window):
	def __init__(self, y, x):
		Window.__init__(self, 'Commands', 30, 6, y, x)

	def refresh(self, data):
		self.win.border(0)
		self.win.addstr(1, 1, 'FR {:<8.2f} []'.format(data[0]))
		self.win.addstr(2, 1, 'FF {:<8.2f} []'.format(data[1]))
		self.win.addstr(3, 1, 'FF {:<8.2f} []'.format(data[2]))
		# self.win.addstr(4, 1, 'FL {:<8.2f} []'.format(data[3]))
		#self.win.addstr(4, 1, 'Battery {}'.format(sparkify([1.0, 2.0, 3.0, 2.5, 0.2, 1.0, 2.0, 3.0, 2.5, 0.2]).encode('utf-8')))
		self.win.refresh()


class Dashboard(object):
	ESC_KEY = 27
	SPACE_KEY = 32
	UP_KEY = 65
	DOWN_KEY = 66
	RIGHT_KEY = 67
	LEFT_KEY = 68

	def __init__(self):
		# print('start')
		locale.setlocale(locale.LC_ALL, '')
		self.screen = curses.initscr()  # Initialize curses.
		curses.noecho()
		curses.cbreak()  # don't need to hit enter
		curses.curs_set(0)  # disable mouse cursor
		self.screen.nodelay(True)  # non-blocking on getch - not sure this works
		# pass

		self.windows = {}
		self.windows['commands'] = CommandWindow(4, 1)
		self.windows['light'] = LightBumperWindow(11, 1)

		self.dummy = -100.0

	def __del__(self):
		curses.nocbreak()
		curses.echo()
		curses.endwin()
		# print('done')

	def draw(self, opt):

		# Clear screen and draw default border:
		self.screen.clear()
		self.screen.border(0)
		self.screen.addstr(10, 30, 'Hello world!')  # Row 10, col 30
		self.screen.addstr(11, 30, '[q] Quit')  # Row 10, col 30
		# self.screen.addstr(12, 30, '[{} ] Forward'.format(u'\u21E7'.encode('utf-8')))  # Row 10, row 30
		# self.screen.addstr(20, 30, 'key {}'.format(opt))
		# self.screen.addstr(13, 30, '[{} ] Reverse'.format(u'\u21E9'.encode('utf-8')))
		# self.screen.addstr(14, 30, '[{} ] Left'.format(u'\u21E6'.encode('utf-8')))
		# self.screen.addstr(15, 30, '[{} ] Right'.format(u'\u21E8'.encode('utf-8')))

		self.screen.refresh()      # Redraw screen.

		# for key in self.windows:
		# 	self.windows(key).refresh()
		self.windows['commands'].refresh()

		self.dummy += 0.1
		self.windows['light'].refresh([self.dummy,-2.2222,3333,-4444.44444])
		# win.refresh()
		# opt = screen.getch()  # Wait for user to enter character.
		# curses.endwin()       # End screen (ready to draw new one, but instead we exit)
		time.sleep(0.1)

	def run(self, bot):
		bot.start()
		bot.safe()
		opt = 'x'
		while True:
			self.draw(opt)
			opt = self.screen.getch()
			# curses.flushinp()  # flush input

			# arrow keys seem to send [27, 66], where the first is ESC
			# you really want the second number
			if opt == self.DOWN_KEY:             
				curses.flash()
				bot.drive_straight(-50)
				
				# return
			elif opt == self.UP_KEY:
				curses.flash()
				curses.beep()
				bot.drive_straight(50)
				time.sleep(1)
				# return
			elif opt == self.RIGHT_KEY:
				curses.flash()
				# return
			elif opt == self.LEFT_KEY:
				
				curses.flash()
				#return
			elif opt == self.SPACE_KEY:
				curses.flash()
			# elif opt == self.ESC_KEY or opt == ord('q'):
			elif opt == ord('q'):
				# curses.beep()
				# curses.flash()
				return
			# else:
			# 	curses.flash()
			# else:
			# 	self.screen.addstr(13, 30, 'key {}'.format(opt))
			# time.sleep(1)
			time.sleep(1)
			bot.drive_straight(0)


if __name__ == "__main__":
	port = '/dev/cu.usbserial-DN04GNJ9'
	
	baud = {
		'default': 115200,
		'alt': 19200  # shouldn't need this unless you accidentally set it to this
	}

	bot = pycreate2.Create2(port=port, baud=baud['default'])
	d = Dashboard()
	d.run(bot)
	
	
	
