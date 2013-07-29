from collections import namedtuple

_Port = namedtuple("_Port", "name direction")
_Cell = namedtuple("_Cell", "name ports")
_Property = namedtuple("_Property", "name value")
_Instance = namedtuple("_Instance", "name cell properties")

  
def _write_cells(cells):
	r = ""
	for cell in cells:
		r += """
	(cell {0.name}
		(cellType GENERIC)
			(view view_1
				(viewType NETLIST)
				(interface""".format(cell)
		for port in cell.ports:
			r += """
					(port {0.name} (direction {0.direction}))""".format(port)
		r += """
				)
			)
	)"""
	return r

def _write_io(ios):
	r = ""
	for s in ios:
		r += """
					(port {0.name} (direction {0.direction}))""".format(s)
	return r

def _write_instantiations(instances, cell_library):
	instantiations = ""
	for instance in instances:
		instantiations += """
					(instance {0.name}
						(viewRef view_1 (cellRef {0.cell} (libraryRef {1})))""".format(instance,cell_library)
		# if param.flavor == "EDIF_FLAVOR_XILINX":
		# 	instantiations += """
		# 				(property XSTLIB (boolean (true)) (owner \"Xilinx\"))"""
		for prop in instance.properties:
			instantiations += """
						(property {0} (string "{1}"))""".format(prop.name,prop.value)
		instantiations += """
					)"""
	return instantiations
