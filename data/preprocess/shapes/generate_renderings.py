"""
    SAGEMAKER + BLENDER:
        https://medium.com/@Mikulas/blender-rendering-on-aws-p2-61f7fb8405d8
"""

import os
from glob import glob
from pathlib import Path

ROOT_SHAPES_PATH = 'LOCAL-PATH-TO-SHAPES-TO-BE-RENDERED/'
BLENDER_EXEC_PATH = Path('LOCAL-PATH-TO-BLENDER-EXEC/')
BLENDER_RENDER_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'generate_rendering.py')
FILE_FORMAT = "obj"

shapes = glob(ROOT_SHAPES_PATH + f"*.{FILE_FORMAT}")
print(f"Number of shapes found is : {len(shapes)}")

## TODO [Cem] : Find a way to run Blender inside Docker containers.
# Possible issues with OpenGL installation inside Docker container and memory issues to run into.
# Possible design change to run blender on shapes beforehand to the retexturing pipeline.
print(f"Path for Blender exec exists : {os.path.exists(BLENDER_EXEC_PATH)}")
for shape in shapes:
    os.system(f"{BLENDER_EXEC_PATH}/blender -b -P\
                {BLENDER_RENDER_SCRIPT_PATH}\
                --shape {Path(shape)}\
                --root {Path(ROOT_SHAPES_PATH)}\
                --focal_legth {54}\
                --cam_args {[90, 0]}\
                --sample_count {1024}\
                --render_engine {'CYCLES'}\
                --img_res {1024}\
                --device {'GPU'}")