from mpf.core.custom_code import CustomCode

class DrainToExtraBall(CustomCode):

    def on_load(self):
        self.info_log("DrainToExtraBall custom code started successfully.")
        self.machine.events.add_handler('outlane_eb_ready', self._await_kill_switches)

    async def _await_kill_switches(self, **kwargs):
        del kwargs

        switches = self.machine.switches.items_tagged('eb_kill')
        for switch in switches:
            self.info_log("Kill Switch: " + switch.name)
        future = self.machine.switch_controller.wait_for_any_switch(switches, 1, True, 1)
        result = await future
        self.info_log("Kill Switch Reported: " + result)