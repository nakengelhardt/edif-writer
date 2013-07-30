from collections import namedtuple

_Port = namedtuple("_Port", "name direction")
_Cell = namedtuple("_Cell", "name ports")
_Property = namedtuple("_Property", "name value")
_Instance = namedtuple("_Instance", "name cell properties")
_NetBranch = namedtuple("_NetBranch", "portname instancename")
  
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

def _write_connections(connections):
	r = ""
	for netname, branches in connections.items():
		r += """
					(net {0}
						(joined""".format(netname)
		for branch in branches:
			r += """
							(portRef {0}{1})""".format(branch.portname, "" if branch.instancename == "" else " (instanceRef {})".format(branch.instancename))
		r += """
						)
					)"""
	return r

def write_edif(cells,ios,instances,connections,cell_library,design_name,part,manufacturer):
	r = """
(edif {0}
	(edifVersion 2 0 0)
	(edifLevel 0)
	(keywordMap (keywordLevel 0))
	(external {1}
		(edifLevel 0)
		(technology (numberDefinition))""".format(design_name,cell_library)
	r += _write_cells(cells)
	r += """
	)
	(library {0}_lib
		(edifLevel 0)
		(technology (numberDefinition))
		(cell {0}
			(cellType GENERIC)
				(view view_1
					(viewType NETLIST)
					(interface""".format(design_name)
	r += _write_io(ios)
	r += """
						(designator "{0}")
					)
					(contents""".format(part)
	r += _write_instantiations(instances, cell_library)
	r += _write_connections(connections)
	r += """
					)
				)
		)
	)
	(design {0}
		(cellRef {0} (libraryRef {0}_lib))
		(property PART (string "{1}") (owner "{2}"))
	)
)""".format(design_name,part,manufacturer)
	
	return r
