from mpf.core.custom_code import CustomCode
from mpf.devices.light import Light
from mpf.core.device_manager import DeviceCollection

lights = None  # type: DeviceCollection[str, Light]

class BonusLightController(CustomCode):

    def on_load(self):
        global lights
        self.info_log("Bonus Light Controller custom code started successfully.")
        lights = self.machine.lights.items_tagged('bonus_light')
        self.machine.events.add_handler('player_bonus_val', self._handle_bonus_change)
        for light in lights:
            self.info_log(light.tags)

    def _handle_bonus_change(self, **kwargs):
        val = kwargs.get("value")
        change = kwargs.get("change")
        self.info_log("Bonus Light Event --> value: " + str(val) + ", change: " + str(change))

        #If the bonus is increasing...
        if change > 0:
            #If the new value is less than 11, check the change amount and turn on that many lights.
            if val < 11:
                for x in range(change):
                    self._get_bonus_light_by_number(val - x).on(fade_ms=50)

            #If the new value is 11, we need to turn off lights 2-9, and ensure 10 is on.
            #Doesn't matter how we got here, just make it happen.
            elif val == 11:
                for x in range(2,10):
                    self._get_bonus_light_by_number(x).off(fade_ms=50)
                self._get_bonus_light_by_number(10).on(fade_ms=50)

            #If the new value is greater than 11, it's a little more complicated...
            elif val > 11:
                #First, ensure 10 is on.
                self._get_bonus_light_by_number(10).on(fade_ms=50)

                #Now turn off 1-9. Maybe overkill, but it's easier and so fast you won't see it.
                #TODO but if it isn't fast enough, we'll need to revisit this decision.
                for x in range(1,10):
                    self._get_bonus_light_by_number(x).off(fade_ms=50)

                #For the rest, turn on lights for the remainder of the value-10.
                for x in range(1, val-10+1):
                    self._get_bonus_light_by_number(x).on(fade_ms=50)

        #But if the bonus is decreasing (bonus is being tallied at the end of the ball or seismic
        #has been collected). This will only decrement by 1 at a time, so it's a little simpler.
        elif change < 0:
            #If the new value is 10 (coming from 11), turn all lights on.
            if val == 10:
                for x in range(1,11):
                    self._get_bonus_light_by_number(x).on(fade_ms=50)
            #If the new value is greater than 10 (coming from greater than 12), then turn off val -10 +1.
            if val > 10:
                self._get_bonus_light_by_number(val - 10 + 1).off(fade_ms=50)
            #If the new value is less than 10 (coming from less than 10) then turn off val + 1.
            if val < 10:
                self._get_bonus_light_by_number(val + 1).off(fade_ms=50)

    @staticmethod
    def _get_bonus_light_by_number(num: int):
        global lights
        for light in lights:
            if light.tags.__contains__('bonus{}'.format(num)):
                return light