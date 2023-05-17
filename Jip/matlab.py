import control.matlab as ct
import numpy as np


rot_speed: dict[str:float] = {
    "omega_1": 1.56605,
    "omega_2": 1.56605,
    "omega_3": 1.56605,
    "omega_4": 1.56605,
}
mass: float = 1
g: float = 9.81
kf: float = -1
km: float = 1
lx: float = 1
ly: float = 1


def transformation_matrix(theta, psi, phi):
    matrix = np.array(
        [
            [
                np.cos(theta) * np.cos(phi),
                np.sin(psi) * np.sin(theta) * np.cos(phi) - np.cos(psi) * np.sin(phi),
                np.cos(psi) * np.sin(theta) * np.cos(phi) + np.sin(psi) * np.sin(phi),
            ],
            [
                np.cos(theta) * np.sin(phi),
                np.sin(psi) * np.sin(theta) * np.sin(phi) + np.cos(psi) * np.cos(phi),
                np.cos(psi) * np.sin(theta) * np.cos(phi) - np.sin(psi) * np.cos(phi),
            ],
            [-np.sin(theta), np.sin(psi), np.cos(theta), np.cos(psi), np.cos(theta)],
        ]
    )
    return matrix


Fx, Fy = 0, 0
Fz = [mass * g]
Mz = 0
for index, item in enumerate(rot_speed.values()):
    Fz.append(item**2 * kf)
    if item + 1 % 2 == 0:
        Mz += km * item**2
    else:
        Mz += -km * item**2

Mx = -Fz[1] + Fz[3]
Mx = -Fz[2] + Fz[4]

print(Fz)
