import os
import subprocess
import numpy as np

ENGINE = r"C:\Progra~2\DHI\MIKE Zero\2022\bin\x64\FemEngine.exe"

def replace_BC_in_setup(u, v, file_in, file_out):
    """replace the strings $$BC2_u$$, $$BC2_v$$"""
    with open(file_in, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace("$$BC2_u$$", str(u))
    filedata = filedata.replace("$$BC2_v$$", str(v))

    with open(file_out, 'w') as file:
        file.write(filedata)

def run_MIKE_setup(setup_file):
    subprocess.run([ENGINE, setup_file])

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

u_vals = np.linspace(-0.1, 0.1, 21)

for j, u in enumerate(u_vals):
    setup = f"HD_2x6_sigma_z_test{j}.m3fm"
    replace_BC_in_setup(u, 0.01, "HD_2x6_sigma_z_template.m3fm", setup)
    run_MIKE_setup(setup)
