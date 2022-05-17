import numpy as np
import matplotlib.pyplot as plt
from integration import integrateGraph
import ThrustMassCalculators as phy # phy for physics

# USER DEFINED VARIABLES
dryMass = 0.737
timeInterval = 14 # for graphs

# Engine 1
burnTime = 3.4
totalImpulse = 49.6
propellantMass = 0.06
engineMass = 0.1044
thrustmass_curve_file = 'f15curve.csv'

averageThrust = totalImpulse/burnTime # N
massFlowRate = propellantMass/burnTime # kg/s

# Engine 2
burnTime2 = 3.4
totalImpulse2 = 49.6
propellantMass2 = 0.06
engineMass2 = 0.1044
engine2IgniteTime = 7.59
thrustmass_curve_file2 = 'f15curve.csv'



# PROGRAM DEFINED VARIABLES
totalMass = dryMass + engineMass + engineMass2

averageThrust2 = totalImpulse2/burnTime2 # N
massFlowRate2 = propellantMass2/burnTime2 # kg/s

thrustmass_curve_1 = phy.gen_thrust_curve(thrustmass_curve_file)
thrustmass_curve_2 = phy.gen_thrust_curve(thrustmass_curve_file2)


time = np.linspace(0, timeInterval, timeInterval * 1000, False) # Array of numbers from 0 to 13.9

# make a thrust array, say the rocket burns at average thrust until the burn time is up, then its thrust is 0
# find the index in time where the element == burnTime
indexOfFirstEnd = int((np.where(np.round(time, 3)==burnTime))[0][0])
indexOfSecondIgnite = int((np.where(np.round(time, 3)==engine2IgniteTime))[0][0])
indexOfSecondEnd = int((np.where(np.round(time, 3)==(engine2IgniteTime + burnTime2)))[0][0])

# Thrust of the first engine (engine2IgniteTime - 1 because on engine2IgniteTime, we want to have a thrust value)
thrustOfFirstEngine = np.append(np.repeat(averageThrust, indexOfFirstEnd), np.repeat(0, indexOfSecondIgnite - indexOfFirstEnd))
# adding the thrust of the second engine for total thrust over time
thrustWithSecondEngine = np.append(thrustOfFirstEngine, np.repeat(averageThrust2, indexOfSecondEnd - indexOfSecondIgnite))
# adding the last 0 values where no engines are burning
thrust = np.append(thrustWithSecondEngine, np.repeat(0, len(time) - indexOfSecondEnd))

# add   the total mass - the mass of the burned fuel   +   the latter half of the thrust array where the first motor is out of fuel
massFromFirstEngine = np.append(np.repeat(totalMass, indexOfFirstEnd) - (time[0:indexOfFirstEnd] * massFlowRate),
                                np.repeat(dryMass + engineMass2, indexOfSecondIgnite - indexOfFirstEnd))
# adding the mass change from the second rocket
secondEngineTimeInterval = time[indexOfSecondIgnite:indexOfSecondEnd] - engine2IgniteTime
mass = np.append(massFromFirstEngine, np.append(np.repeat(totalMass, indexOfSecondEnd - indexOfSecondIgnite) - (secondEngineTimeInterval * massFlowRate),
                                                np.repeat(dryMass, len(time) - indexOfSecondEnd)))

# net acceleration, F = ma, a = F/m
acceleration = thrust/mass - 9.81
velocity = integrateGraph(time, acceleration)
position = integrateGraph(time, velocity)

plt.style.use('dark_background')

figure, axis = plt.subplots(1, 3)

axis[0].plot(time, acceleration)
axis[0].set_title("Acceleration")

axis[1].plot(time, velocity)
axis[1].set_title("Velocity")

axis[2].plot(time, position)
axis[2].set_title("Position")
plt.grid(linestyle='-', linewidth=0.2)

plt.show()

