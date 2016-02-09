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

class HeroInfoView(QtGui.QWidget):
	def __init__(self, parent=None):
		super(HeroInfoView, self).__init__(parent)

		layout = QtGui.QGridLayout()
		layout.addWidget(HeroButton(None, self), 0, 0, 1, 1)
		for i in range(16):
			layout.addWidget(HeroButton(None, self), 1, i, 1, 1)
			adv_label = QtGui.QLabel(self)
			adv_label.setFixedSize(64, 36)
			layout.addWidget(adv_label, 2, i, 1, 1)
		self.setLayout(layout)

	def show(self, hero):
		self.disconnect_all()

		self.layout().itemAtPosition(0, 0).widget().set_hero(hero)

		if self.parentWidget().heropool.get_hero_by_name(hero.name).available:
			self.layout().itemAtPosition(0, 0).widget().left_click.connect(self.parentWidget().hero_selected)
		self.layout().itemAtPosition(0, 0).widget().right_click.connect(self.parentWidget().show_hero_info)

		for i, (hero_name, advantage) in enumerate(sorted(hero.related_to.iteritems(), key=lambda x: float(x[1]), reverse=True)):
			self.layout().itemAtPosition(1, i).widget().set_hero(self.parentWidget().heropool.get_hero_by_name(hero_name))

			if self.parentWidget().heropool.get_hero_by_name(hero_name).available:
				self.layout().itemAtPosition(1, i).widget().left_click.connect(self.parentWidget().hero_selected)
			self.layout().itemAtPosition(1, i).widget().right_click.connect(self.parentWidget().show_hero_info)

			self.layout().itemAtPosition(2, i).widget().setStyleSheet('QLabel { border: 1px solid black; }')
			self.layout().itemAtPosition(2, i).widget().setText('%s' % advantage)

	def disconnect_all(self):
		try:
			self.layout().itemAtPosition(0, 0).widget().left_click.disconnect(self.parentWidget().hero_selected)
			self.layout().itemAtPosition(0, 0).widget().right_click.disconnect(self.parentWidget().show_hero_info)
		except TypeError:  # already disconnected
			pass

		for i in range(16):
			try:
				self.layout().itemAtPosition(1, i).widget().left_click.disconnect(self.parentWidget().hero_selected)
				self.layout().itemAtPosition(1, i).widget().right_click.disconnect(self.parentWidget().show_hero_info)
			except TypeError:  # already disconnected
				pass

	def reconnect_all(self):
		hero = self.layout().itemAtPosition(0, 0).widget().hero
		if hero:
			self.show(hero)