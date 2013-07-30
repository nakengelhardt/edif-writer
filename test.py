from collections import OrderedDict
from migen.fhdl.std import *
from migen.fhdl.namer import Namespace, build_namespace
from migen.fhdl.tools import list_special_ios

from edif import *
from edif import _Cell, _Port, _Property, _Instance, _NetBranch, _write_cells, _write_instantiations, _write_io, _write_connections

def generate_cells(f):
	cell_dict = OrderedDict()
	for special in f.specials:
		if isinstance(special, Instance):
			port_list = []
			for port in special.items:
				if isinstance(port, Instance.Input):
					port_list.append(_Port(port.name, "INPUT"))
				elif isinstance(port, Instance.Output):
					port_list.append(_Port(port.name, "OUTPUT"))
				elif isinstance(port, Instance.Parameter):
					pass
				else:
					raise NotImplementedError("Unsupported instance item")
			if special.of in cell_dict:
				if set(port_list) != set(cell_dict[special.of]):
					raise ValueError("All instance must have the same ports for EDIF conversion")
				else:
					cell_dict[special.of] = port_list
	return [_Cell(k, v) for k, v in cell_dict.items()]

def generate_instances(f,ns):
	instances = []
	for special in f.specials:
		if isinstance(special, Instance):	
			props = []
			for prop in special.items:
				if isinstance(prop, Instance.Input):
					pass
				elif isinstance(prop, Instance.Output):
					pass
				elif isinstance(prop, Instance.Parameter):
					props.append((prop.name, prop.value))
				else:
					raise NotImplementedError("Unsupported instance item")
			instances.append(_Instance(name=ns.get_name(special), cell=special.of, properties=props))
	return instances

def generate_ios(f, ios, ns):
	outs = list_special_ios(f, False, True, False)
	r = []
	for io in ios:
		direction = "OUTPUT" if io in outs else "INPUT"
		r.append(_Port(name=ns.get_name(io), direction=direction))
	return r

def generate_connections(f, ios, ns):
	r = OrderedDict()
	for special in f.specials:
		if isinstance(special, Instance):
			instname = ns.get_name(special)
			for port in special.items:
				if isinstance(port, Instance.Input) or isinstance(port, Instance.Output):
					s = ns.get_name(port.expr)
					if s not in r:
						r[s] = []
					r[s].append(_NetBranch(portname=port.name, instancename=instname))
				elif isinstance(port, Instance.Parameter):
					pass
				else:
					raise NotImplementedError("Unsupported instance item")
	for s in ios:
		io = ns.get_name(s)
		if io not in r:
			r[io] = []
		r[io].append(_NetBranch(portname=io, instancename=""))
	return r

class Test(Module):
	def __init__(self):
		self.s1 = Signal()
		self.s2 = Signal()
		self.s3 = Signal()
		self.specials.foo = Instance("foo", i_X=self.s1, o_Y=self.s2)
		self.specials.bar = Instance("bar", o_A=self.s1, i_B=self.s3)

t = Test()
f = t.get_fragment()
ns = build_namespace(list_special_ios(f, True, True, True))
cells = generate_cells(f)
instances = generate_instances(f, ns)
ios = generate_ios(f, {t.s3, t.s2}, ns)
cell_library = "UNISIMS"
connections = generate_connections(f, {t.s3, t.s2}, ns)
print(_write_cells(cells))
print(_write_instantiations(instances,cell_library))
print(_write_io(ios))
print(_write_connections(connections))
print(write_edif(cells,ios,instances,connections,cell_library,"Test","xc6slx45-fgg484-2","Xilinx"))
