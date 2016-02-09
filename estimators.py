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

class BasicEstimator:
	def __init__(self, cycle, heropool):
		self.cycle = cycle
		self.heropool = heropool

	def estimate_heroes(self):
		current_selection = self.cycle.current_selection()
		counter_selection = self.cycle.selections[{
			'Radiant Pick': 'Dire Pick',
			'Radiant Ban': 'Radiant Pick',
			'Dire Pick': 'Radiant Pick',
			'Dire Ban': 'Dire Pick'
		}[current_selection.name]]
		counter_heroes = counter_selection.get_heroes()

		heroes = []
		for hero in self.heropool.get_available_heroes():
			advantages = []
			for counter_hero in counter_heroes:
				advantage = []
				try:
					advantage.append(float(hero.related_to[counter_hero.name]))
				except KeyError:
					pass

				try:
					advantage.append(-1.0*float(counter_hero.related_to[hero.name]))
				except KeyError:
					pass

				try:
					advantages.append(sum(advantage)/len(advantage))
				except ZeroDivisionError:
					pass
			try:
				heroes.append((hero, sum(advantages)/len(advantages)))
			except ZeroDivisionError:
				heroes.append((hero, 0.))

		return [h for h in sorted(heroes, key=lambda x: x[1], reverse=True) if h[1] > 0]