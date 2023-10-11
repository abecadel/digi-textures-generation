"""
    To run this script (To be able to see python outputs/prints/etc):
        [YOUR-LOCAL-PATH-TO-BLENDER-EXEC]/blender 
"""
""" TODO : CEM
    Add argparser to call the script to iterate and process all 3d objects
    '''
        parser = argparse.ArgumentParser(description='Renders given obj file by rotation a camera around it.')
        parser.add_argument('obj', type=str, help='Path to the obj file to be rendered.')
        parser.add_argument('cam', type=str, help='Path to the cam pose file.')
        argv = sys.argv[sys.argv.index("--") + 1:]
        args = parser.parse_args(argv)
        print('args.obj:' + args.obj)
        print('args.cam:' + args.cam)
    '''
"""

"""
Useful links:
	https://blender.stackexchange.com/questions/137648/how-to-render-depth-pass-with-alpha-channel-transparency-in-cycles
	https://www.youtube.com/watch?app=desktop&v=AVVEOrQDNgg&ab_channel=LightArchitect
	https://thousandyardstare.de/blog/generating-depth-images-in-blender-279.html#top
"""

import bpy
import bpy_extras
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import copy
import math
import mathutils
import numpy as np
import os
import sys

import random

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Imports to run this script in a loop
from argparse import ArgumentParser
from pathlib import Path

############################## HELPER FUNCTIONS ################################################
def random_color_generator(n_item):
    colors = []
    for i in range(n_item):
        r = random.randint(0, 256)
        g = random.randint(0, 256)
        b = random.randint(0, 256)
        if r > 200 and g > 200 and b > 200:
            pass
        else:
            colors.append((r,g,b))
    return colors
    
def point_at(obj, target, roll=0):
    if not isinstance(target, mathutils.Vector):
        target = mathutils.Vector(target)
    loc = obj.location
    direction = target - loc
    quat = direction.to_track_quat('-Z', 'Y')
    quat = quat.to_matrix().to_4x4()
    rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')
    loc = loc.to_tuple()
    obj.matrix_world = quat @ rollMatrix
    obj.location = loc


def get_material_names():
    mats = bpy.data.materials
    mat_list = []
    for m in mats:
        if m.name.startswith('material_'):
            mat_list.append(m.name)
    return mat_list


def new_color_material(mat_name, color, shadow_mode='NONE'):
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    # principled_node = nodes.get('Principled BSDF')
    principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    output_node = nodes.get("Material Output")
    principled_node.inputs.get("Base Color").default_value = color
    principled_node.inputs.get("Alpha").default_value = color[3]
    principled_node.inputs.get("Roughness").default_value = 1.0
    # principled_node.inputs.get("Emission Strength").default_value = 0
    link = links.new( principled_node.outputs['BSDF'], output_node.inputs['Surface'] )
    if color[-1] < 1:
        mat.blend_method = 'BLEND'
    mat.shadow_method = shadow_mode
    return mat


def spherical_to_cartesian(radius, azimuth, elevation):
    x = radius * math.cos(azimuth) * math.sin(elevation)
    y = radius * math.cos(elevation)
    z = radius * math.sin(azimuth) * math.sin(elevation)
    return (x, y, z)

###############################################################################################

######################### HELPER FUNCTION TO GET SEGMENTATION MAP  ############################
def GenerateSegmentationImage(mat_name, color, shadow_mode='NONE'):
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    emission_node = nodes.new(type='ShaderNodeEmission')
    seg_out_node = nodes.get("Material Output")
    emission_node.inputs['Color'].default_value = color
    link = links.new(emission_node.outputs['Emission'], seg_out_node.inputs['Surface'])
    mat.shadow_method = shadow_mode
    return mat
###############################################################################################

######################### INPUTS  #############################################################
parser = ArgumentParser(
    prog="Blender Rendering Of Objects",
    description="This script is to render given 3D object from angles  \
    to generate 3D aware images of objects to be used in Stable Diffusion for noval look generation"
)
parser.add_argument("--shape", required=True, type=Path)
parser.add_argument("--root", required=True, type=Path)
parser.add_argument("--output", required=True, type=str)
parser.add_argument("--focal_length", required=True, type=int)
parser.add_argument("--cam_x", required=True, type=int)
parser.add_argument("--cam_y", required=True, type=int)
parser.add_argument("--sample_count", required=False, default=1024)
parser.add_argument("--render_engine", required=False, default="CYCLES")
parser.add_argument("--img_res", required=False, default=1024)
parser.add_argument("--device", required=False, default="GPU")

try:
    args = parser.parse_args()
except Exception as e:
    print(f"Error at parsing arguments for 'generate_rendering.py' file with given error log : {e}")

SHAPE_PATH = args.shape
ROOT_PATH = args.root
FOCAL_LENGTH =  args.focal_length
CAM_ARGS = [args.cam_x, args.cam_y]

# Save the filename to create a new folder to store all rendered images
FILENAME = args.shape.split("/")[-1].split('.')[0]
OUTPUT_PATH = args.output + "/" + FILENAME

bpy.context.scene.render.engine =  args.render_engine
bpy.context.scene.cycles.samples = args.sample_count
bpy.context.scene.cycles.device =  args.device

# Set out rendered image size:
RENDER_IMAGE_RESOLUTION = args.img_res
bpy.context.scene.render.resolution_x = RENDER_IMAGE_RESOLUTION
bpy.context.scene.render.resolution_y = RENDER_IMAGE_RESOLUTION
bpy.context.scene.render.film_transparent = True
bpy.context.scene.view_settings.view_transform = 'Standard'

######################### DELETE INITIAL SETUPS AND LOAD OBJECT  ##############################
# Load obj files
try:
    cube = bpy.data.objects['Cube']
    cube.select_set(True)
    bpy.ops.object.delete()
except:
    print("Initial cube doesn't exist")

try:
    light = bpy.data.objects['Light']
    light.select_set(True)
    bpy.ops.object.delete()
except:
    print("NO light object exists")

# Import the object
if 'obj' in SHAPE_PATH:
    bpy.ops.import_scene.obj(filepath=SHAPE_PATH, axis_forward='Y', axis_up='Z')
elif 'glb' in SHAPE_PATH:
    bpy.ops.import_scene.gltf(filepath=SHAPE_PATH)
# Save imported objects for layer coordinate mapping
objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(objects)

# Set nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree 
links = tree.links
for n in tree.nodes:
    tree.nodes.remove(n)

# Set bg white
render_layers = tree.nodes.new('CompositorNodeRLayers')
alpha_node = tree.nodes.new(type="CompositorNodeAlphaOver")
alpha_node.premul = 1
output_node_img = tree.nodes.new(type='CompositorNodeOutputFile')
output_node_img.format.color_mode = 'RGBA'
output_node_img.format.file_format = 'PNG'
links.new(render_layers.outputs['Image'], alpha_node.inputs[2])
links.new(alpha_node.outputs['Image'], output_node_img.inputs[0])

# set output path.
output_node_img.base_path = OUTPUT_PATH
if not os.path.exists(output_node_img.base_path):
    os.makedirs(output_node_img.base_path)
    
### FIRST TAKE PICTURE OF BLACK OBJECT WITHOUT SEGMENTATION COLORS
# set lights
focus_point = [0,0,0]
light_distance = 3
light_names = ['Light_front', 'Light_back', 'Light_left', 'Light_right', 'Light_top', 'Light_bottom']
light_locations = []
for i in range(3):
    light_location = focus_point[:]
    light_location[i] -= light_distance
    light_locations.append(light_location)
    light_location = focus_point[:]
    light_location[i] += light_distance
    light_locations.append(light_location)
for i in range(len(light_names)):
    light_data = bpy.data.lights.new(name=light_names[i], type='POINT')
    light_data.energy = 1000
    light_object = bpy.data.objects.new(name=light_names[i], object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    bpy.context.view_layer.objects.active = light_object
    light_object.location = light_locations[i]
    
# set obj materials.
mat_list = get_material_names()
for mat in mat_list:
    tar_color = (0,0,0)
    new_color_material(mat, [tar_color[0] / 255., tar_color[1] / 255., tar_color[2] / 255., 1.])
    
# set camera.
cam = bpy.data.objects['Camera']
cam.location = spherical_to_cartesian(2, CAM_ARGS[0], CAM_ARGS[1])
point_at(cam, (0., 0., 0.))
cam.data.lens_unit = 'MILLIMETERS'
cam.data.lens = FOCAL_LENGTH

output_node_img.file_slots[0].path = f'focalLength={FOCAL_LENGTH},theta={CAM_ARGS[0]},phi={CAM_ARGS[1]}_RENDERED'
print(output_node_img.file_slots[0].path)
bpy.ops.render.render(write_still=True)


### TAKE SEGMENTATION PICTURES NOW WITH LESSER LIGHT ILLUMINATION TO AVOID OVEREXPOSURE
# Change material colors to random ones.
mat_no = len(mat_list)
colors = random_color_generator(mat_no)
for mat, color in zip(mat_list, colors):
    tar_color = color
    #new_color_material(mat, [tar_color[0] / 255., tar_color[1] / 255., tar_color[2] / 255., 1.])
    GenerateSegmentationImage(mat, [tar_color[0] / 255., tar_color[1] / 255., tar_color[2] / 255., 1.])
    
    
lights = bpy.data.lights
for light in lights:
    light.energy = 100
    light.use_shadow = False
    
output_node_img.file_slots[0].path = f'focalLength={FOCAL_LENGTH},theta={CAM_ARGS[0]},phi={CAM_ARGS[1]}_SEGMENTED'
print(output_node_img.file_slots[0].path)
bpy.ops.render.render(write_still=True)

### TAKE RENDER IMAGE OF NORMAL VECTORS
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
bpy.context.scene.display.shading.light = 'MATCAP'
bpy.context.scene.display.shading.studio_light = 'check_normal+y.exr'

                
output_node_img.file_slots[0].path = f'focalLength={FOCAL_LENGTH},theta={CAM_ARGS[0]},phi={CAM_ARGS[1]}_NORMALS'
print(output_node_img.file_slots[0].path)
bpy.ops.render.render(write_still=True)

### TAKE RENDER IMAGE OF DEPTH INFORMATION
bpy.context.scene.render.engine = 'CYCLES'
scene = bpy.context.scene
scene.view_layers['ViewLayer'].use_pass_z = True
depth_node = tree.nodes.new(type="CompositorNodeNormalize")
setAlpha_node = tree.nodes.new(type="CompositorNodeSetAlpha")
inverter_node = tree.nodes.new(type="CompositorNodeInvert")

links.new(render_layers.outputs['Depth'], depth_node.inputs[0])
links.new(depth_node.outputs[0], inverter_node.inputs['Color'])
links.new(inverter_node.outputs[0], setAlpha_node.inputs['Image'])

links.new(render_layers.outputs['Alpha'], setAlpha_node.inputs['Alpha'])
links.new(setAlpha_node.outputs[0], output_node_img.inputs[0])

output_node_img.file_slots[0].path = f'focalLength={FOCAL_LENGTH},theta={CAM_ARGS[0]},phi={CAM_ARGS[1]}_DEPTH'
bpy.ops.render.render(write_still=True)


### SAVE INFORMATION ABOUT PIXEL TO 3D WORLD COORDINATES
# Used solution is from : https://blender.stackexchange.com/questions/77607/how-to-get-the-3d-coordinates-of-the-visible-vertices-in-a-rendered-image-in-ble

# Threshold to test if ray cast corresponds to the original vertex
limit = 0.1

selected = 0
not_selected = 0
discarded = 0
with open(OUTPUT_PATH + '/' + 'vertexToPixCoordinates.txt', 'w') as file:
    scene = bpy.context.scene
    for obj in objects:
        file.write(str(obj))
        vertices = obj.data.vertices # It will return the coordinates of vertices
    
        for v in vertices:

            # Local to global coordinates
            co = v.co @ obj.matrix_world
            
            # Calculate 2D Image coordinates
            co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, co)
            
            if 0.0 <= co_2d.x <= 1.0 and 0.0 <= co_2d.y <= 1.0 and co_2d.z > 0:
                
                location = scene.ray_cast(bpy.context.view_layer.depsgraph, cam.location, (v.co - cam.location).normalized())
                
                if location[0] and (v.co - location[1]).length < limit:
                    
                    render_scale = scene.render.resolution_percentage / 100
                    render_size = (
                                    int(scene.render.resolution_x * render_scale),
                                    int(scene.render.resolution_y * render_scale),
                    )
                    # This is the result
                    pix_coordinates = (int(co_2d.x * render_size[0]),
                                        int(co_2d.y * render_size[1]))
                        
                    file.write(" ".join(str(i) for i in pix_coordinates) + " " + " ".join(str(i) for i in co) + "\n")
                    
                    selected += 1
                
                else:
                    discarded += 1
            else:
                not_selected += 1
                
print(f"Selected number of vertices : {selected}\nDiscardd number of vertices : {discarded}\nNot selected number of vertices : {not_selected}")
