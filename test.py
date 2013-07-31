from collections import OrderedDict
from migen.fhdl.std import *
from migen.fhdl.namer import Namespace, build_namespace
from migen.fhdl.tools import list_special_ios
from migen.fhdl.specials import SynthesisDirective

import edif



class Test(Module):
	def __init__(self):
		self.s = Signal()
		self.a = Signal()
		self.b = Signal()
		self.a_IBUF = Signal()
		self.b_IBUF = Signal()
		self.s_OBUF = Signal()
		self.specials.s1 = Instance("LUT2", i_I0=self.a_IBUF, i_I1=self.b_IBUF, o_O=self.s_OBUF, p_INIT=8)
		self.specials.a_ibuf = Instance("IBUF", i_I=self.a, o_O=self.a_IBUF)
		self.specials.b_ibuf = Instance("IBUF", i_I=self.b, o_O=self.b_IBUF)
		self.specials.s_obuf = Instance("OBUF", i_I=self.s_OBUF, o_O=self.s)

t = Test()
ios = {t.a, t.b, t.s}
name = "Example"
part = "xc6slx45-fgg484-2"
cell_library = "UNISIMS"
vendor = "Xilinx"
print(edif.convert(t, ios, name, cell_library, part, vendor))
