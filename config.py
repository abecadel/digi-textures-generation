from pathlib import Path

use_cuda : bool = True

######################## Data Generation ######################
DATA_ROOT = Path("data")
SHAPES_ROOT = DATA_ROOT / "shapes"
MATERIALS_ROOT = DATA_ROOT / "materials"
###############################################################

######################## Image Generator ######################
CONTROLNET_CANNY_PATH = Path("diffusers/controlnet-canny-sdxl-1.0")
CONTROLNET_DEPTH_PATH = Path("diffusers/controlnet-depth-sdxl-1.0")
CONTROLNET_SEGMENTATION_PATH = Path("SargeZT/sdxl-controlnet-seg")  # TODO [Cem] : Test if it is any good model.
CONTROLNET_NORMALS_PATH = Path("")

VAE_MODEL_PATH = Path("madebyollin/sdxl-vae-fp16-fix")
SDXL_MODEL_PATH = Path("stabilityai/stable-diffusion-xl-base-1.0")
CONTROLNET_CONDITIONING_SCALE : float = 0.5
SDXL_USE_SAFETENSORS : bool = True
SEED = None         # Leave None to generate random seed.
num_inference_steps = 30
check_nsfw_info = True
#image_resolution = (1024, 1024) # This arg is discard to match the image generation resolution to controlnet image input resolutions

### Shape rendered image suffixes
render_image = "_RENDERED"
seg_image = "_SEGMENTED"
normals_image = "_NORMALS"
depth_image = "_DEPTH"

# controlnet - canny
control_canny = False
control_canny_cond_scale : float = 0.5
canny_threshold_min = 100
canny_threshold_max = 200

# controlnet - depth
control_depth = False
control_depth_cond_scale : float = 0.5

# controlnet - segmentation
control_seg = False
control_seg_cond_scale : float = 0.5

# controlnet - normals
control_normals = False
control_normals_cond_scale : float = 0.5

###############################################################


###################### Material Prediction ####################

###############################################################

####################### Material Transfer #####################

###############################################################