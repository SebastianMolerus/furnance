class pid:
    def __init__(self, target : float, kp : float, ki : float, kd : float):
        self._target = target

        self._kp = kp
        self._ki = ki
        self._kd = kd

        self._sumET = float()

        self._old_current = float()        

    def control(self, current : float) -> float:
        # P part
        difference = round(self._target - current, 3)
        P =  self._kp * difference

        # I part
        self._sumET += difference
        I = self._ki * self._sumET

        # D part
        if self._old_current == 0:
            self._old_current = current

        diff = current - self._old_current 
        D = self._kd * diff
        self._old_current = current

        return P + I + D

