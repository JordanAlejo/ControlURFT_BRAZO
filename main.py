import pybullet as p
import pybullet_data
import time


# ============================================================
# CONFIGURACIÓN
# ============================================================

URDF_FILE = "brazo.urdf"

START_POSITION = [0, 0, 0.15]

STEP = 0.02          # cuánto cambia el ángulo por pulsación
MAX_FORCE = 100      # fuerza de los motores
TIME_STEP = 1 / 240  # simulación


# ============================================================
# CONECTAR CON PYBULLET
# ============================================================

print("======================================")
print("   CONTROL DEL BRAZO ROBÓTICO")
print("======================================")

physics_client = p.connect(p.GUI)

if physics_client < 0:
    raise RuntimeError("No se pudo conectar con PyBullet")

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.81)

p.setTimeStep(TIME_STEP)

# Cámara
p.resetDebugVisualizerCamera(
    cameraDistance=1.2,
    cameraYaw=45,
    cameraPitch=-25,
    cameraTargetPosition=[0, 0, 0.4]
)


# ============================================================
# CARGAR ROBOT
# ============================================================

try:

    robot_id = p.loadURDF(
        URDF_FILE,
        START_POSITION,
        useFixedBase=True
    )

except Exception as error:

    print("\nERROR cargando el URDF:")
    print(error)

    p.disconnect()
    raise


print("\nRobot cargado correctamente.")


# ============================================================
# MOSTRAR ARTICULACIONES
# ============================================================

num_joints = p.getNumJoints(robot_id)

print("\n======================================")
print("ARTICULACIONES ENCONTRADAS")
print("======================================")

for i in range(num_joints):

    info = p.getJointInfo(robot_id, i)

    joint_name = info[1].decode("utf-8")
    joint_type = info[2]

    print(
        f"ID: {i:2d} | "
        f"Nombre: {joint_name:20s} | "
        f"Tipo: {joint_type}"
    )


# ============================================================
# POSICIÓN INICIAL DE LAS ARTICULACIONES
# ============================================================

joint_positions = {}

for i in range(num_joints):

    info = p.getJointInfo(robot_id, i)

    joint_type = info[2]

    if joint_type == p.JOINT_REVOLUTE or joint_type == p.JOINT_PRISMATIC:

        joint_positions[i] = p.getJointState(robot_id, i)[0]


# ============================================================
# FUNCIÓN PARA MOVER UNA ARTICULACIÓN
# ============================================================

def move_joint(joint_id, amount):

    if joint_id not in joint_positions:
        return

    joint_positions[joint_id] += amount

    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=joint_id,
        controlMode=p.POSITION_CONTROL,
        targetPosition=joint_positions[joint_id],
        force=MAX_FORCE
    )


# ============================================================
# INFORMACIÓN DE CONTROL
# ============================================================

print("\n======================================")
print("CONTROLES")
print("======================================")

print("Flecha IZQ  → Articulación 0 -")
print("Flecha DER  → Articulación 0 +")

print("Flecha ARR  → Articulación 1 +")
print("Flecha ABA  → Articulación 1 -")

print("Q           → Articulación 2 +")
print("A           → Articulación 2 -")

print("W           → Articulación 3 +")
print("S           → Articulación 3 -")

print("E           → Articulación 4 +")
print("D           → Articulación 4 -")

print("R           → Pinza +")
print("F           → Pinza -")

print("ESC         → Salir")

print("======================================\n")


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

try:

    while p.isConnected():

        keys = p.getKeyboardEvents()


        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        if 27 in keys:

            if keys[27] & p.KEY_WAS_TRIGGERED:

                print("\nCerrando PyBullet...")
                break


        # ----------------------------------------------------
        # ARTICULACIÓN 0
        # FLECHAS IZQUIERDA / DERECHA
        # ----------------------------------------------------

        if p.B3G_LEFT_ARROW in keys:

            if keys[p.B3G_LEFT_ARROW] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(0, -STEP)


        if p.B3G_RIGHT_ARROW in keys:

            if keys[p.B3G_RIGHT_ARROW] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(0, STEP)


        # ----------------------------------------------------
        # ARTICULACIÓN 1
        # FLECHAS ARRIBA / ABAJO
        # ----------------------------------------------------

        if p.B3G_UP_ARROW in keys:

            if keys[p.B3G_UP_ARROW] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(1, STEP)


        if p.B3G_DOWN_ARROW in keys:

            if keys[p.B3G_DOWN_ARROW] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(1, -STEP)


        # ----------------------------------------------------
        # ARTICULACIÓN 2
        # Q / A
        # ----------------------------------------------------

        if ord("q") in keys:

            if keys[ord("q")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(2, STEP)


        if ord("a") in keys:

            if keys[ord("a")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(2, -STEP)


        # ----------------------------------------------------
        # ARTICULACIÓN 3
        # W / S
        # ----------------------------------------------------

        if ord("w") in keys:

            if keys[ord("w")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(3, STEP)


        if ord("s") in keys:

            if keys[ord("s")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(3, -STEP)


        # ----------------------------------------------------
        # ARTICULACIÓN 4
        # E / D
        # ----------------------------------------------------

        if ord("e") in keys:

            if keys[ord("e")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(4, STEP)


        if ord("d") in keys:

            if keys[ord("d")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(4, -STEP)


        # ----------------------------------------------------
        # PINZA
        # R / F
        # ----------------------------------------------------

        if ord("r") in keys:

            if keys[ord("r")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(5, STEP)


        if ord("f") in keys:

            if keys[ord("f")] & (
                p.KEY_IS_DOWN | p.KEY_WAS_TRIGGERED
            ):

                move_joint(5, -STEP)


        # ----------------------------------------------------
        # SIMULACIÓN
        # ----------------------------------------------------

        p.stepSimulation()

        time.sleep(TIME_STEP)


finally:

    if p.isConnected():

        p.disconnect()

    print("\nPyBullet cerrado.")
    print("Programa terminado.")