from mpf.core.custom_code import CustomCode

delay = 200 ; int()

class BonusCounter(CustomCode):

    def on_load(self):
        self.info_log("BonusCountdown custom code started successfully.")
        self.machine.events.add_handler('bonus_start', self._start_bonus_countdown)
        self.machine.events.add_handler('bonus_countdown_decrement', self._decrement_bonus, 1)
        self.machine.events.add_handler('flipper_cancel', self._speed_up_bonus)

    def _start_bonus_countdown(self, **kwargs):
        del kwargs
        #global delay
        if self.machine.game.player.bonus_val > 0:
            # delay = 1800/self.machine.game.player.bonus_val
            # if delay > 100:
            #     delay = 100
            self.machine.game.player.bonus_val -= 1
            self.machine.game.player.bonuscountdisplay += 1
            self.machine.events.post('bonus_countdown_decrement')

    def _decrement_bonus(self, **kwargs):
            global delay
            self.machine.delay.add(ms=delay, callback=self._do_decrement)
            # if BonusCounter.delay > 10:
            self.machine.delay.add(ms=delay, callback=self._do_decrement_audio)

    def _do_decrement_audio(self, **kwargs):
        self.machine.events.post('bonus_countdown_decrement_audio')

    def _speed_up_bonus(self, **kwargs):
        BonusCounter.delay = 10

    def _do_decrement(self):
        if self.machine.game.player.bonus_val > 0:
            self.machine.game.player.bonus_val -= 1
            self.machine.game.player.bonuscountdisplay += 1
            self.machine.events.post('bonus_countdown_decrement')
        else:
            self.machine.events.post('finish_up_bonus')