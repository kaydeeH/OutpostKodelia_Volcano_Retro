from mpf.core.custom_code import CustomCode

matches = 0  # type: int()

class MatchAlerter(CustomCode):

    def on_load(self):
        self.info_log("MatchAlerter custom code started successfully.")
        self.machine.events.add_handler('has_match', self._do_match_alerts)

    def _do_match_alerts(self, **kwargs):
        global matches

        number = kwargs.get('winner_number')
        player_count = self.machine.game.num_players

        for x in range(player_count):
            if number == kwargs.get('match_number' + str(x)):
                matches += 1

        if matches > 0:
            self.machine.delay.add(ms=1, callback=self._do_next_alert)
        else:
            self.machine.events.post('match_alerts_done')

    def _do_next_alert(self, **kwargs):
        global matches

        self.machine.events.post('match_alert')
        matches -= 1
        if matches > 0:
            self.machine.delay.add(ms=500, callback=self._do_next_alert)
        else:
            self.machine.events.post('match_alerts_done')