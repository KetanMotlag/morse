import math
import datetime
import GameLogic

import morse.helpers.middleware

from morse.middleware.pocolibs.sensors.General_Poster import ors_poster


class MorsePocolibsClass(morse.helpers.middleware.MorseMiddlewareClass):
	""" Handle communication between Blender and YARP."""

	def __init__(self, obj, parent=None):
		""" Initialize the network and connect to the yarp server."""
		# Call the constructor of the parent class
		super(self.__class__,self).__init__(obj, parent)

		# Store the id's of created posters, indexed by component name
		self._poster_dict = dict()
		# Dictionary for external posters
		self._poster_in_dict = dict()
		self._imported_modules = dict()


	def __del__(self):
		""" Close all open posters. """
		for component_name, poster_id in self._poster_dict.items():
			print ("Killing poster %d for component %s" % (poster_id, component_name))
			# Call the method to close a poster
			ors_poster.finalize(poster_id)


	def register_component(self, component_name,
			component_instance, mw_data):
		""" Open the pocolibs poster to communicate a specified component.

		The configuration of each type of poster is done in external modules.
		"""
		# Extract the information for this middleware
		# Second parameter is the name of the function to add to the component
		function_name = mw_data[1]
		# Third parameter is the file where the function can be found
		extra_module_name = mw_data[2]

		# Import the configuration of the poster from an extra module
		function = self._add_method(extra_module_name, function_name, component_instance)


	def _compute_date(self):
		""" Compute the current time

		( we only requiere that the date
		increases using a constant step so real time is ok)
		"""
		t = datetime.datetime.now()
		date = int(t.hour * 3600* 1000 + t.minute * 60 * 1000 +
				t.second * 1000 + t.microsecond / 1000)

		return date, t
