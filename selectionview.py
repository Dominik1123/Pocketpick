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
from herobutton import HeroButton

class SelectionView(QtGui.QWidget):
	def __init__(self, name, parent=None):
		super(SelectionView, self).__init__(parent)

		self.name = name

		name_label = QtGui.QLabel(name, self)
		layout = QtGui.QHBoxLayout()
		layout.addWidget(name_label)
		for i in range(5):
			layout.addWidget(HeroButton(None, self))
		self.setLayout(layout)

		self.n_heroes = 0

	def add_hero(self, hero):
		hero_button = self.layout().itemAt(self.n_heroes+1).widget()
		hero_button.set_hero(hero)
		hero_button.left_click.connect(self.parentWidget().hero_back_to_pool)
		hero_button.right_click.connect(self.parentWidget().show_hero_info)
		self.n_heroes += 1

	def remove_hero(self, hero):
		hero_button = next(layout_item.widget() for layout_item in [self.layout().itemAt(i) for i in range(1,self.n_heroes+1)] if layout_item.widget().hero == hero)
		hero_button.set_hero(None)
		hero_button.left_click.disconnect(self.parentWidget().hero_back_to_pool)
		hero_button.right_click.disconnect(self.parentWidget().show_hero_info)
		self.n_heroes -= 1

	def get_heroes(self):
		return [self.layout().itemAt(i).widget().hero for i in range(1,self.n_heroes+1)]

	def connect_herobutton(self, hero_button):
		hero_button.left_click.connect(self.parentWidget().hero_back_to_pool)

	def disconnect_all(self):
		for i in range(1,self.n_heroes+1):
			try:
				self.layout().itemAt(i).widget().left_click.disconnect(self.parentWidget().hero_back_to_pool)
			except TypeError:  # already disconnected
				pass

	def mark(self):
		self.layout().itemAt(self.n_heroes+1).widget().setStyleSheet("HeroButton { background-color: white; border: 3px solid red; }")

	def unmark(self):
		self.layout().itemAt(self.n_heroes+1).widget().setStyleSheet("HeroButton { background-color: white; }")