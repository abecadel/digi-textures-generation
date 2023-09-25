"""
    SAGEMAKER + BLENDER:
        https://medium.com/@Mikulas/blender-rendering-on-aws-p2-61f7fb8405d8
"""

import os
from glob import glob

ROOT_SHAPES_PATH = 'LOCAL-PATH-TO-SHAPES-TO-BE-RENDERED/'
BLENDER_EXEC_PATH = 'LOCAL-PATH-TO-BLENDER-EXEC/'
BLENDER_RENDER_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'generate_rendering.py')

shapes = glob(ROOT_SHAPES_PATH + '*.obj')

for shape in shapes:
    os.system(f"{BLENDER_EXEC_PATH}/blender -b -P {BLENDER_RENDER_SCRIPT_PATH} --shape {shape}") # TODO [Cem] : Implement argument parsing