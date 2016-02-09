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

class PickListView(QtGui.QScrollArea):
	def __init__(self, parent=None):
		super(PickListView, self).__init__(parent)

		self.view = QtGui.QWidget(self)
		self.setWidget(self.view)
		self.setWidgetResizable(True)

		layout = QtGui.QVBoxLayout()
		self.view.setLayout(layout)

	def new_estimation(self, estimation):
		self.clear_layout()
		for hero, advantage in estimation:
			h_layout = QtGui.QHBoxLayout()
			pb = HeroButton(hero, self)
			pb.left_click.connect(self.parentWidget().hero_selected)
			pb.right_click.connect(self.parentWidget().show_hero_info)
			h_layout.addWidget(pb)
			adv_label = QtGui.QLabel('%.2f' % advantage, self)
			adv_label.setStyleSheet('QLabel { border: 1px solid black; }')
			adv_label.setFixedSize(64, 36)
			h_layout.addWidget(adv_label)
			self.view.layout().addLayout(h_layout)

	def clear_layout(self):
		while self.view.layout().count() > 0:
			h_layout = self.view.layout().takeAt(self.view.layout().count()-1)
			h_layout.takeAt(0).widget().hide()
			h_layout.takeAt(0).widget().hide()