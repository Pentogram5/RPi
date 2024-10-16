# Действия, что производятся роборукой
# Каждое действие имеет зону (радиус) R действия и расстояние L от точки радиуса до края гусениц робота

from SC_servo import *
S = ScServo()

import time

def perform_action_capture():
    S.executeTrajectory(S.calcTrajectory(S.catchState))
    time.sleep(0.2)
    S.executeTrajectory(S.calcTrajectory(S.catch))
    time.sleep(0.5)
    S.executeTrajectory(S.calcTrajectory(S.expeditionState))
    return True

def perform_action_report():
    return True
    
def perform_action_throw_to_basket():
    S.executeTrajectory(S.calcTrajectory(S.putState))
    time.sleep(0.2)
    S.executeTrajectory(S.calcTrajectory(S.throw))
    time.sleep(0.5)
    S.executeTrajectory(S.calcTrajectory(S.expeditionState))
    return True