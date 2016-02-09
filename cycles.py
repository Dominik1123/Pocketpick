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

class Cycle:
	def __init__(self, selections):
		self.selections = selections

	def current_selection(self):
		return self.selections[self.current_step]

	def next(self):
		self.current_index += 1
		try:
			self.current_step = self.steps[self.current_index]
		except IndexError:
			raise StopIteration()

	def previous(self):
		self.current_index -= 1
		self.current_step = self.steps[self.current_index]

	def disconnect_all_selections(self):
		for selection in self.selections.itervalues():
			selection.disconnect_all()

	def connect_last_hero_of_previous_selection(self):
		if self.current_index > 0:
			previous_selection = self.selections[self.steps[self.current_index-1]]
			hero_button = previous_selection.layout().itemAt(previous_selection.n_heroes).widget()
			previous_selection.connect_herobutton(hero_button)

class RankedAllPickCycle(Cycle):
	def __init__(self, selections):
		Cycle.__init__(self, selections)

		self.steps = ['Radiant Pick', 'Dire Pick', 'Radiant Pick', 'Dire Pick', 'Radiant Pick', 'Dire Pick', 'Radiant Pick', 'Dire Pick', 'Radiant Pick', 'Dire Pick']
		self.current_index = 0
		self.current_step = self.steps[self.current_index]

class RankedCaptainsModeCycle(Cycle):
	def __init__(self, selections):
		Cycle.__init__(self, selections)

		self.steps = ['Radiant Ban', 'Dire Ban', 'Radiant Ban', 'Dire Ban', 'Radiant Pick', 'Dire Pick', 'Dire Pick', 'Radiant Pick', 'Radiant Ban', 'Dire Ban', 'Radiant Ban', 'Dire Ban', 'Dire Pick', 'Radiant Pick', 'Dire Pick', 'Radiant Pick', 'Dire Ban', 'Radiant Ban', 'Dire Pick', 'Radiant Pick']
		self.current_index = 0
		self.current_step = self.steps[self.current_index]