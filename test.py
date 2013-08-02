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
		self.d = Signal()
		self.a_IBUF = Signal()
		self.d_IBUF = Signal()
		self.s_OBUF = Signal()
		self.d_inv = Signal()
		self.N2 = Signal()
		self.specials.Mmux_s11 = Instance("LUT3", i_I0=self.a_IBUF, i_I1=self.N2, i_I2=self.d_IBUF, o_O=self.s_OBUF, p_INIT="A8")
		self.specials.a_ibuf = Instance("IBUF", i_I=self.a, o_O=self.a_IBUF)
		self.specials.d_ibuf = Instance("IBUF", i_I=self.d, o_O=self.d_IBUF)
		self.specials.s_obuf = Instance("OBUF", i_I=self.s_OBUF, o_O=self.s)
		self.specials.b_iobuf = Instance("IOBUF", i_I=self.a_IBUF, i_T=self.d_inv, o_O=self.N2, io_IO=self.b)
		self.specials.d_inv1_INV_0 = Instance("INV", i_I=self.d_IBUF, o_O=self.d_inv)

t = Test()
ios = {t.a, t.b, t.s, t.d}
name = "Example"
part = "xc6slx45-fgg484-2"
cell_library = "UNISIMS"
vendor = "Xilinx"
print(edif.convert(t, ios, name, cell_library, part, vendor))
