from common import *
from dmi_bfm import DMITestBfm as BFM
from pyuvm import *


class DMIAgent(uvm_agent):
    """
    Seqr <---> Driver <---> Top module
              Monitor <------^
    """

    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "DMI_SEQR", self.seqr)

        self.monitor = DMIMonitor("dmi_monitor", self, "rsp_monitor_q_get")
        self.driver = DMIDriver("dmi_driver", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class DMIDriver(uvm_driver):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap_drv", self)

    def start_of_simulation_phase(self):
        self.bfm = BFM()

    async def run_phase(self):
        self.bfm.start_bfm()

        while True:
            item = await self.seq_item_port.get_next_item()
            await self.bfm.req_driver_q_put(item)
            self.seq_item_port.item_done()


class DMIMonitor(uvm_component):
    def __init__(self, name, parent, method_name):
        super().__init__(name, parent)
        self.method_name = method_name

    def build_phase(self):
        self.ap = uvm_analysis_port("ap_mon", self)
        self.bfm = BFM()
        self.get_method = getattr(self.bfm, self.method_name)

    async def run_phase(self):
        while True:
            datum = await self.get_method()
            self.logger.debug(f"DMI Monitor req: {datum}")
            self.ap.write(datum)
