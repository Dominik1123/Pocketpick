#######################################################################################
#
# This program solves the 2D puzzle "Lonpos 101".
# Copyright (C) 2016  Dominik Vilsmeier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################################

from PyQt4 import QtGui, QtCore

class HeroButton(QtGui.QPushButton):
	left_click = QtCore.pyqtSignal('QString')
	right_click = QtCore.pyqtSignal('QString')

	def __init__(self, hero, parent=None):
		super(HeroButton, self).__init__(parent)

		self.setStyleSheet('HeroButton { background-color: white; }')
		self.setFixedSize(64, 36)  # set to image dimensions

		self.set_hero(hero)

	def mousePressEvent(self, event):
		try:
			hero_name = self.hero.name
		except AttributeError:
			hero_name = 'N/A'

		if event.button() == QtCore.Qt.LeftButton:
			self.left_click.emit(hero_name)
		elif event.button() == QtCore.Qt.RightButton:
			self.right_click.emit(hero_name)

	def set_hero(self, hero):
		self.hero = hero
		if hero:
			self.setIcon(QtGui.QIcon(self.hero.img_path))
			self.setToolTip(hero.name)
		else:
			self.setIcon(QtGui.QIcon())
			self.setToolTip('')
		self.setIconSize(QtCore.QSize(64, 36))