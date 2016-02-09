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

class ProgressView(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ProgressView, self).__init__(parent)

		self.pbar = QtGui.QProgressBar(self)
		self.pbar.setMinimum(0)
		self.pbar.setMaximum(100)
		self.pbar.setValue(0)

		self.log = QtGui.QTableWidget(self)
		self.log.setColumnCount(1)

		self.continue_button = QtGui.QPushButton('continue', self)
		self.continue_button.setEnabled(False)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.pbar, 0)
		layout.addWidget(self.log, 1)
		layout.addWidget(self.continue_button, 0)
		self.setLayout(layout)

		self.continue_button.clicked.connect(parent.data_loaded)

	def update(self, name, count, total):
		self.pbar.setValue(float(count)/float(total)*100.)
		self.log.insertRow(self.log.rowCount())
		self.log.setItem(self.log.rowCount()-1, 0, QtGui.QTableWidgetItem('{0}: ok'.format(name)))

		if count == total:
			self.continue_button.setEnabled(True)