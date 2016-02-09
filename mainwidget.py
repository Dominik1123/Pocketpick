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
from cycles import RankedAllPickCycle, RankedCaptainsModeCycle
from estimators import BasicEstimator as Estimator
from modeselector import ModeSelector
from heropoolview import HeroPoolView
from  heroinfoview import HeroInfoView
from picklistview import PickListView
from progressview import ProgressView
from selectionview import SelectionView

class MainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent)

		self.modeselector = ModeSelector(self)
		self.heropool = HeroPoolView(self)
		self.heroinfo = HeroInfoView(self)
		self.picklist = PickListView(self)
		self.progress = ProgressView(self)

		self.pool_stack = QtGui.QStackedWidget(self)
		self.pool_stack.addWidget(self.heropool)
		self.pool_stack.addWidget(self.modeselector)
		self.pool_stack.addWidget(self.progress)
		self.pool_stack.setCurrentWidget(self.modeselector)

		self.heropool.load_data_locally()

		layout = QtGui.QGridLayout()
		layout.addWidget(self.picklist, 0, 0, 3, 1)
		layout.addWidget(self.pool_stack, 0, 1, 1, 1)
		layout.addWidget(self.heroinfo, 2, 1, 1, 1)
		self.setLayout(layout)

	def data_loaded(self):
		self.pool_stack.setCurrentWidget(self.modeselector)

	def switch_to_heropoolview(self):
		self.pool_stack.setCurrentWidget(self.heropool)

	def switch_to_progressview(self):
		self.pool_stack.setCurrentWidget(self.progress)

	def ranked_all_pick_selected(self):
		self.radiant_pick = SelectionView('Radiant Pick', self)
		self.dire_pick = SelectionView('Dire Pick', self)
		h_layout = QtGui.QHBoxLayout()
		h_layout.addWidget(self.radiant_pick)
		h_layout.addWidget(self.dire_pick)
		self.layout().addLayout(h_layout, 1, 1, 1, 1)

		selections = {
			self.radiant_pick.name: self.radiant_pick,
			self.dire_pick.name: self.dire_pick
		}

		self.cycle = RankedAllPickCycle(selections)
		self.estimator = Estimator(self.cycle, self.heropool)

	def ranked_captains_mode_selected(self):
		self.radiant_pick = SelectionView('Radiant Pick', self)
		self.dire_pick = SelectionView('Dire Pick', self)
		self.radiant_ban = SelectionView('Radiant Ban', self)
		self.dire_ban = SelectionView('Dire Ban', self)
		v_layout = QtGui.QVBoxLayout()

		h_layout = QtGui.QHBoxLayout()
		h_layout.addWidget(self.radiant_ban)
		h_layout.addWidget(self.dire_ban)
		v_layout.addLayout(h_layout)

		h_layout = QtGui.QHBoxLayout()
		h_layout.addWidget(self.radiant_pick)
		h_layout.addWidget(self.dire_pick)
		v_layout.addLayout(h_layout)

		self.layout().addLayout(v_layout, 1, 1, 1, 1)

		selections = {
			self.radiant_pick.name: self.radiant_pick,
			self.dire_pick.name: self.dire_pick,
			self.radiant_ban.name: self.radiant_ban,
			self.dire_ban.name: self.dire_ban
		}

		self.cycle = RankedCaptainsModeCycle(selections)
		self.estimator = Estimator(self.cycle, self.heropool)

	def hero_selected(self, hero_name):
		self.cycle.disconnect_all_selections()
		selection = self.cycle.current_selection()
		selection.add_hero(self.heropool.get_hero_by_name(hero_name))
		self.heropool.hero_selected(self.heropool.get_hero_by_name(hero_name))
		self.heroinfo.reconnect_all()
		try:
			self.cycle.next()
		except StopIteration:  # last hero was selected;
			self.heropool.disconnect_all()
		else:
			self.picklist.new_estimation(self.estimator.estimate_heroes())

	def hero_back_to_pool(self, hero_name):
		self.cycle.previous()
		selection = self.cycle.current_selection()
		selection.remove_hero(self.heropool.get_hero_by_name(hero_name))
		self.heropool.hero_back_to_pool(self.heropool.get_hero_by_name(hero_name))
		self.cycle.connect_last_hero_of_previous_selection()
		self.picklist.new_estimation(self.estimator.estimate_heroes())

	def show_hero_info(self, hero_name):
		self.heroinfo.show(self.heropool.get_hero_by_name(hero_name))