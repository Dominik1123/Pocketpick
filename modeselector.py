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

class ModeSelector(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ModeSelector, self).__init__(parent)

		self.ranked_all_pick_button = QtGui.QPushButton("All Pick", self)
		self.ranked_captains_mode_button = QtGui.QPushButton("Captains Mode", self)

		layout = QtGui.QVBoxLayout()
		layout.addStretch(1)
		h_layout = QtGui.QHBoxLayout()
		h_layout.addStretch(1)
		h_layout.addWidget(self.ranked_all_pick_button, 0)
		h_layout.addStretch(1)
		layout.addLayout(h_layout, 0)
		h_layout = QtGui.QHBoxLayout()
		h_layout.addStretch(1)
		h_layout.addWidget(self.ranked_captains_mode_button, 0)
		h_layout.addStretch(1)
		layout.addLayout(h_layout, 0)
		layout.addStretch(1)
		self.setLayout(layout)


		self.ranked_all_pick_button.clicked.connect(parent.ranked_all_pick_selected)
		self.ranked_captains_mode_button.clicked.connect(parent.ranked_captains_mode_selected)

		self.ranked_all_pick_button.clicked.connect(parent.switch_to_heropoolview)
		self.ranked_captains_mode_button.clicked.connect(parent.switch_to_heropoolview)