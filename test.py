import pybullet as p
import pybullet_data
import time

print("Iniciando PyBullet...")

physicsClient = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.81)

robot_id = p.loadURDF(
    "brazo.urdf",
    [0, 0, 0.15],
    useFixedBase=True
)

print("Robot cargado:", robot_id)
print("PyBullet funcionando correctamente")
print("Presiona ESC para salir")

while p.isConnected():

    keys = p.getKeyboardEvents()

    # ESC = 27
    if 27 in keys and keys[27] & p.KEY_WAS_TRIGGERED:
        break

    p.stepSimulation()
    time.sleep(1 / 240)

p.disconnect()

print("PyBullet cerrado")