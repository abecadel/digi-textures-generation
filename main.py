import config

from garmet_generator.image_generator.generate_image import ImageGenerator
from garmet_generator.material_predictor.predict_material import MaterialPredictor
from garmet_generator.material_transfer.transfer_material import MaterialTransfer

############################Prepare 3D Object Renderings############################
####################################################################################

############################Generate Novel 2D Garment Appearance####################

# Initialize Image Generator
sdxl_controlnet = ImageGenerator(config=config)

# Define Stable Diffusion + ControlNet inputs : prompt, negative prompt, controlnet images (support for multiple inputs)
prompt = ""
negative_prompt = ""
control_image_paths = []

# Output of generate function is {'images': images, 'nsfw_info' : nsfw_info}
results = sdxl_controlnet.generate(control_image_paths, prompt=prompt, negative_prompt=negative_prompt)

####################################################################################

############################Predict Material on 2D Image############################
material_predictor = MaterialPredictor()
####################################################################################

############################Transfer Predicted Material#############################
material_transfer = MaterialTransfer()
####################################################################################
