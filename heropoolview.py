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

import types
from PyQt4 import QtGui, QtCore
from datamanager import DataManager
from downloadmanager import DownloadManager
from herobutton import HeroButton

class HeroPoolView(QtGui.QWidget):
	heroes_per_row=16

	def __init__(self, parent=None):
		super(HeroPoolView, self).__init__(parent)

	def load_data_locally(self):
		try:
			self.heroes = DataManager().load_hero_data()
		except IOError:
			info = QtGui.QMessageBox('Datafile not found', 'I couldn\'t load the data locally, do you want me to download it from the website?', QtGui.QMessageBox.Information, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton, self)
			if info.exec_() == QtGui.QMessageBox.Ok:
				self.download_data()
		else:
			self.buttons = []
			layout = QtGui.QGridLayout()
			layout.addWidget(self.create_searchfield(), 0, 13, 1, 3)
			for i, hero in enumerate(self.heroes):
				pb = HeroButton(hero, self)
				pb.left_click.connect(self.parentWidget().parentWidget().hero_selected)
				pb.right_click.connect(self.parentWidget().parentWidget().show_hero_info)
				layout.addWidget(pb, 1+i/HeroPoolView.heroes_per_row, i%HeroPoolView.heroes_per_row)
				self.buttons.append(pb)
			self.setLayout(layout)

	def create_searchfield(self):
		self.search = QtGui.QLineEdit(self)
		self.search.textChanged.connect(self.highlight_heroes)
		return self.search

	def highlight_heroes(self, text):
		for hero_button in self.buttons:
			if text in hero_button.hero.name and hero_button.hero.available:
				hero_button.setEnabled(True)
			else:
				hero_button.setEnabled(False)

	def download_data(self):
		self.parentWidget().parentWidget().switch_to_progressview()

		self.download_manager = DownloadManager()
		self.thread = QtCore.QThread()
		self.download_manager.moveToThread(self.thread)

		self.thread.started.connect(self.download_manager.start)
		self.download_manager.hero_loaded.connect(self.parentWidget().parentWidget().progress.update)
		self.download_manager.job_done.connect(self.thread.quit)
		self.download_manager.job_done.connect(self.data_loaded)

		self.thread.start()

	def data_loaded(self):
		heroes = self.download_manager.heroes
		DataManager().save_hero_data(heroes)
		self.load_data_locally()

	def get_hero_by_name(self, hero_name):
		return next((hero for hero in self.heroes if hero.name == hero_name), None)

	def hero_selected(self, hero):
		hero_button = next(hb for hb in self.buttons if hb.hero.name == hero.name)
		hero_button.setEnabled(False)
		hero_button.hero.available = False
		self.search.setText('')

	def hero_back_to_pool(self, hero):
		hero_button = next(hb for hb in self.buttons if hb.hero.name == hero.name)
		hero_button.setEnabled(True)
		hero_button.hero.available = True
		self.search.setText('')

	def get_available_heroes(self):
		return [hb.hero for hb in self.buttons if hb.hero.available]

	def disconnect_all(self):
		for hero_button in self.buttons:
			hero_button.left_click.disconnect(self.parentWidget().parentWidget().hero_selected)