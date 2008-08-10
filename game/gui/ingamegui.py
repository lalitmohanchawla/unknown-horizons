# ###################################################
# Copyright (C) 2008 The OpenAnno Team
# team@openanno.org
# This file is part of OpenAnno.
#
# OpenAnno is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from buildingtool import BuildingTool
import game.main
import fife
from game.util import livingObject
from messagewidget import MessageWidget
from tabwidget import TabWidget

class IngameGui(livingObject):
	"""Class handling all the ingame gui events."""
	def begin(self):
		super(IngameGui, self).begin()
		self.gui = {}
		self.tabwidgets = {}
		self.settlement = None
		self._old_menu = None

		self.gui['encyclopedia'] = game.main.fife.pychan.loadXML('content/gui/encyclopedia_button.xml')
		self.gui['encyclopedia'].show()

		self.gui['topmain'] = game.main.fife.pychan.loadXML('content/gui/top_main.xml')
		self.gui['topmain'].position = (
			game.main.fife.settings.getScreenWidth()/2 - self.gui['topmain'].size[0]/2,
			5
		)
		self.message_widget = MessageWidget(self.gui['topmain'].position[0] + self.gui['topmain'].size[0], 5)
		self.gui['gamemenu'] = game.main.fife.pychan.loadXML('content/gui/gamemenu_button.xml')
		self.gui['gamemenu'].position = (
			game.main.fife.settings.getScreenWidth() - self.gui['gamemenu'].size[0] - 5,
			5
		)
		self.gui['gamemenu'].mapEvents({
			'gameMenuButton' : game.main.showPause
		})
		self.gui['gamemenu'].show()

		self.gui['minimap_toggle'] = game.main.fife.pychan.loadXML('content/gui/minimap_toggle_button.xml')
		self.gui['minimap_toggle'].position = (
			game.main.fife.settings.getScreenWidth() - self.gui['minimap_toggle'].size[0] - 15,
			game.main.fife.settings.getScreenHeight() - self.gui['minimap_toggle'].size[1] -15,
		)
		self.gui['minimap_toggle'].show()
		self.gui['minimap_toggle'].mapEvents({
			'minimapToggle' : self.toggle_minmap
		})

		self.gui['minimap'] = game.main.fife.pychan.loadXML('content/gui/minimap.xml')
		self.gui['minimap'].position = (
				game.main.fife.settings.getScreenWidth() - self.gui['minimap'].size[0] - self.gui['minimap_toggle'].size[0],
				game.main.fife.settings.getScreenHeight() - self.gui['minimap'].size[1],
		)
		self.gui['minimap'].show()
		self.gui['minimap'].mapEvents({
			'zoomIn' : game.main.session.view.zoom_in,
			'zoomOut' : game.main.session.view.zoom_out,
			'rotateRight' : game.main.session.view.rotate_right,
			'rotateLeft' : game.main.session.view.rotate_left
		})

		self.gui['camTools'] = game.main.fife.pychan.loadXML('content/gui/cam_tools.xml')
		self.gui['camTools'].position = (
				game.main.fife.settings.getScreenWidth() - self.gui['camTools'].size[0] - self.gui['minimap_toggle'].size[0] -15,
				game.main.fife.settings.getScreenHeight() - self.gui['camTools'].size[1] -15,
		)
		self.gui['camTools'].mapEvents({
			'zoomIn' : game.main.session.view.zoom_in,
			'zoomOut' : game.main.session.view.zoom_out,
			'rotateRight' : game.main.session.view.rotate_right,
			'rotateLeft' : game.main.session.view.rotate_left
		})

		self.gui['leftPanel'] = game.main.fife.pychan.loadXML('content/gui/left_panel.xml')
		self.gui['leftPanel'].position = (
			5,
			game.main.fife.settings.getScreenHeight()/2 - self.gui['minimap'].size[1]/2
		)
		self.gui['leftPanel'].show()
		self.gui['leftPanel'].mapEvents({
			'build' : self.show_build_menu
		})

		self.gui['status'] = game.main.fife.pychan.loadXML('content/gui/status.xml')
		self.gui['status'].position = (
			self.gui['topmain'].position[0] - self.gui['status'].size[0],
			5
		)
		self.gui['status_gold'] = game.main.fife.pychan.loadXML('content/gui/status_gold.xml')
		self.gui['status_gold'].position = (
			self.gui['status'].position[0] - 48,
			5
		)
		self.gui['status_gold'].show()


		callbacks_build = {'build1': {
			'store-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 2),
		},
			'build2': {
				'resident-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 3),
		},
			'build3': {
				'tree' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 17),
				'weaver-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 7),
				'lumberjack-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 8),
				'herder-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 10)
		},
			'build5': {
				'street-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 15),
				'bridge-1' : game.main.fife.pychan.tools.callbackWithArguments(self._build, 16)
		}
		}

		self.tabwidgets['build'] = TabWidget(1, callbacks=callbacks_build)
		self.gui['build'] = self.tabwidgets['build'].widget

		self.gui['buildinfo'] = game.main.fife.pychan.loadXML('content/gui/hud_buildinfo.xml')
		self.gui['chat'] = game.main.fife.pychan.loadXML('content/gui/hud_chat.xml')
		self.gui['cityinfo'] = game.main.fife.pychan.loadXML('content/gui/hud_cityinfo.xml')
		self.gui['res'] = game.main.fife.pychan.loadXML('content/gui/hud_res.xml')
		self.gui['fertility'] = game.main.fife.pychan.loadXML('content/gui/hud_fertility.xml')
		self.gui['ship'] = game.main.fife.pychan.loadXML('content/gui/hud_ship.xml')
		self.gui['ship'].position = (
			game.main.fife.settings.getScreenWidth() - self.gui['build'].size[0] - 450,
			game.main.fife.settings.getScreenHeight() - self.gui['build'].size[1] - 35,
		)

	def end(self):
		self.gui['gamemenu'].mapEvents({
			'gameMenuButton' : None
		})

		self.gui['ship'].mapEvents({
			'foundSettelment' : None
		})

		self.gui['minimap'].mapEvents({
			'zoomIn' : None,
			'zoomOut' : None,
			'rotateRight' : None,
			'rotateLeft' : None
		})

		self.gui['minimap_toggle'].mapEvents({
			'minimapToggle' : None
		})

		self.gui['camTools'].mapEvents({
			'zoomIn' : None,
			'zoomOut' : None,
			'rotateRight' : None,
			'rotateLeft' : None
		})
		for w in self.gui.values():
			if w._parent is None:
				w.hide()
		self.message_widget = None
		self.tabwidgets = None
		self.hide_menu()
		super(IngameGui, self).end()

	def update_gold(self):
		self.status_set('gold', str(game.main.session.world.player.inventory.get_value(1)))
		self.set_status_position('gold')

	def status_set(self, label, value):
		"""Sets a value on the status bar.
		@param label: str containing the name of the label to be set.
		@param value: value the Label is to be set to.
		"""
		foundlabel = (self.gui['status_gold'] if label == 'gold' else self.gui['status']).findChild(name=label)
		foundlabel._setText(value)
		foundlabel.resizeToContent()
		if label == 'gold':
			self.gui['status_gold'].resizeToContent()
		else:
			self.gui['status'].resizeToContent()

	def cityinfo_set(self, settlement):
		"""Sets the city name at top center

		Show/Hide is handled automatically
		To hide cityname, set name to ''
		@param settlement: Settlement class providing the information needed
		"""
		if settlement == self.settlement:
			return
		if self.settlement is not None:
			self.settlement.removeChangeListener(self.update_settlement)
		self.settlement = settlement
		if(settlement == None):
			self.gui['topmain'].hide()
			self.gui['status'].hide()
		else:
			self.gui['topmain'].show()
			self.gui['status'].show()
			self.update_settlement()
			settlement.addChangeListener(self.update_settlement)

	def update_settlement(self):
		foundlabel = self.gui['topmain'].findChild(name='city_name')
		foundlabel._setText(self.settlement.name)
		foundlabel.resizeToContent()
		foundlabel = self.gui['topmain'].findChild(name='city_inhabitants')
		foundlabel.text = 'Inhabitants: '+str(self.settlement._inhabitants)
		foundlabel.resizeToContent()
		self.gui['topmain'].resizeToContent()

		self.status_set('wool', str(self.settlement.inventory.get_value(2)))
		self.set_status_position('wool')
		self.status_set('wood', str(self.settlement.inventory.get_value(4)))
		self.set_status_position('wood')
		self.status_set('food', str(self.settlement.inventory.get_value(5)))
		self.set_status_position('food')
		self.status_set('tools', str(self.settlement.inventory.get_value(6)))
		self.set_status_position('tools')
		self.status_set('bricks', str(self.settlement.inventory.get_value(7)))
		self.set_status_position('bricks')

	def ship_build(self, ship):
		"""Calls the Games build_object class."""
		self._build(1, ship)

	def show_ship(self, ship):
		self.gui['ship'].findChild(name='buildingNameLabel').text = ship.name+" (Ship type)"

		size = self.gui['ship'].findChild(name='chargeBar').size
		size = (size[0] - 2, size[1] - 2)
		self.gui['ship'].findChild(name='chargeBarLeft').size = (int(0.5 + 0.75 * size[0]), size[1])
		self.gui['ship'].findChild(name='chargeBarRight').size = (int(0.5 + size[0] - 0.75 * size[0]), size[1])

		pos = self.gui['ship'].findChild(name='chargeBar').position
		pos = (pos[0] + 1, pos[1] + 1)
		self.gui['ship'].findChild(name='chargeBarLeft').position = pos
		self.gui['ship'].findChild(name='chargeBarRight').position = (int(0.5 + pos[0] + 0.75 * size[0]), pos[1])
		self.gui['ship'].mapEvents({
			'foundSettelment' : game.main.fife.pychan.tools.callbackWithArguments(self.ship_build, ship)
		})
		self.show_menu('ship')

	def show_build_menu(self):
		self.deselect_all()
		self.show_menu('build')

	def deselect_all(self):
		for instance in game.main.session.selected_instances:
			instance.deselect()
		self.hide_menu()
		game.main.session.selected_instances = set()

	def _build(self, building_id, unit = None):
		"""Calls the games buildingtool class for the building_id.
		@param building_id: int with the building id that is to be built.
		@param unit: weakref to the unit, that builds (e.g. ship for branch office)"""
		self.hide_menu()
		self.deselect_all()
		cls = game.main.session.entities.buildings[building_id]
		if hasattr(cls, 'show_build_menu'):
			cls.show_build_menu()
		game.main.session.cursor = BuildingTool(cls, None if unit is None else unit())

	def show_menu(self, menu):
		"""Shows a menu
		@param menu: str with the guiname or pychan object.
		"""
		if self._old_menu is not None:
			self._old_menu.hide()
		if isinstance(menu, str):
			self._old_menu = self.gui[menu]
		else:
			self._old_menu = menu
		if self._old_menu is not None:
			self._old_menu.show()

	def hide_menu(self):
		self.show_menu(None)

	def build_load_tab(self, num):
		"""Loads a subcontainer into the build menu and changes the tabs background.
		@param num: number representing the tab to load.
		"""
		tab1 = self.gui['build'].findChild(name=('tab'+str(self.active_build)))
		tab2 = self.gui['build'].findChild(name=('tab'+str(num)))
		activetabimg, nonactiveimg= tab1._getImage(), tab2._getImage()
		tab1._setImage(nonactiveimg)
		tab2._setImage(activetabimg)
		contentarea = self.gui['build'].findChild(name='content')
		contentarea.removeChild(self.gui['build_tab'+str(self.active_build)])
		contentarea.addChild(self.gui['build_tab'+str(num)])
		contentarea.adaptLayout()
		self.active_build = num

	def toggle_minmap(self):
		if self.gui['minimap'].isVisible():
			self.gui['minimap'].hide()
		else:
			self.gui['minimap'].show()

		if self.gui['camTools'].isVisible():
			self.gui['camTools'].hide()
		else:
			self.gui['camTools'].show()

	def set_status_position(self, resource_name):
		icon_name = resource_name + '_icon'
		if resource_name == 'gold':
					self.gui['status_gold'].findChild(name = resource_name).position = (
				self.gui['status_gold'].findChild(name = icon_name).position[0] + 24 - self.gui['status_gold'].findChild(name = resource_name).size[0]/2,
				48
			)
		else:
			self.gui['status'].findChild(name = resource_name).position = (
				self.gui['status'].findChild(name = icon_name).position[0] + 24 - self.gui['status'].findChild(name = resource_name).size[0]/2,
				48
			)
