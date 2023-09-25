"""
Refs:
    https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sdxl
"""

from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline, AutoencoderKL
from diffusers.utils import load_image
from PIL import Image
import torch
import numpy as np
import cv2

from os.path import exists
import os

import sys
sys.path.append("./")
import config

"""
    ImageGenerator is a class to generate 2D images with StableDiffusionXL + ControlNet from diffusers library. 
    It doesn't support generation without ControlNet input.
    TODO [Cem] : Implement SDXL Refiner model. [input -> SDXL Base + Controlnet -> SDXL Refiner -> output]
    
    KeyNotes:
            - No need for depth estimator. ControlNet Depth input image is Blender generated depth image.
            - No need for segmenter. ControlNet Segmentation input image is Blender generated segmentation image.
            - No need for normals detector. ControlNet Normals input image is Blender generated normals image.
"""
class ImageGenerator():
    def __init__(self, config):
        
        self.config = config
        
        #### ControlNet Model collections:
        # https://huggingface.co/lllyasviel/sd_control_collection/tree/main
        # https://huggingface.co/collections/diffusers/sdxl-controlnets-64f9c35846f3f06f5abe351f
        
        # Manage multiple controlnet inputs pipeline.
        counter = 1
        self.controlnets = []
        if config.control_canny:
            print("Loading CONTROLNET-{counter} = 'CANNY EDGE DETECTION' model...")
            counter += 1
            controlnet_canny = ControlNetModel.from_pretrained(self.config.CONTROLNET_CANNY_PATH, torch_dtype=torch.float16)
            self.controlnets.append(controlnet_canny)
        if config.control_depth:
            print("Loading CONTROLNET-{counter} = 'DEPTH' model...")
            counter += 1
            controlnet_depth = ControlNetModel.from_pretrained(self.config.CONTROLNET_DEPTH_PATH, torch_dtype=torch.float16)
            self.controlnets.append(controlnet_depth)
        if config.control_seg:
            print("Loading CONTROLNET-{counter} = 'SEGMENTATION' model...")
            counter += 1
            controlnet_seg = ControlNetModel.from_pretrained(self.config.CONTROLNET_SEGMENTATION_PATH, torch_dtype=torch.float16)
            self.controlnets.append(controlnet_seg)
        if config.control_normals:
            print("Loading CONTROLNET-{counter} = 'NORMALS' model...")
            counter += 1
            controlnet_normals = ControlNetModel.from_pretrained(self.config.CONTROLNET_NORMALS_PATH, torch_dtype=torch.float16)
            self.controlnets.append(controlnet_normals)
        
        if len(self.controlnets) == 0:
            raise ValueError("No ControlNet models are provided! ImageGenerator doesn't support it! Provide a valid ControlNet model.")
        
        print("Loading vae model...")
        self.vae = AutoencoderKL.from_pretrained(self.config.VAE_MODEL_PATH, torch_dtype=torch.float16)
        
        print("Loading sdxl model...")
        pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
                                        self.config.SDXL_MODEL_PATH,
                                        vae=self.vae,
                                        controlnet=self.controlnet,
                                        use_safetensors=self.config.SDXL_USE_SAFETENSORS,
                                        variant="fp16",
                                        torch_dtype=torch.float16
        )
        
        if config.use_cuda:
            self.pipe = pipe.to("cuda")

    def load_image(self, path, mode="RGB"):
        if mode == "RGB":
            return load_image(path).convert("RGB")
        elif mode =="L":
            return load_image(path).convert("L")
        else:
            raise ValueError(f"[ImageGenerator.load_image]- Invalid mode for loading image : {mode}")
    
    def get_canny_image(self, path, threshold_min : int = 100, threshold_max : int = 200) -> Image:
        image = load_image(path)
        image = np.array(image)
        image = cv2.Canny(image, threshold_min, threshold_max)
        image = image[:, :, None]
        image = np.concatenate([image, image, image], axis=2)
        return Image.fromarray(image)
    
    def get_depth_image(self, path):
        return self.load_image(path, mode="L")
    
    def get_seg_image(self, path):
        return self.load_image(path)
    
    def get_normals_image(self, path):
        return self.load_image(path)

    def generate(self,
                 image_path : str = "",
                 prompt : str = "",
                 negative_prompt : str = "",
                 ) -> dict:
        if not exists(image_path):
            raise FileNotFoundError(f"Given image path doesn't exists : {image_path}")
        if not (prompt.strip() and negative_prompt.strip()):
            
            raise ValueError("Please provide at least prompt to generate image")
        
        if (self.config.SEED is None) or (self.config.SEED <= 0):
            seed = int.from_bytes(os.urandom(2), "big")
        else:
            seed = self.config.SEED
            
        if config.use_cuda:
            generator = torch.Generator("cuda").manual_seed(seed=seed)
        else:
            generator = torch.Generator("cpu").manual_seed(seed=seed)
        print(f"Using seed :  {seed}")
        
        self.pipe.enable_model_cpu_offload()  # Use or not ?
        
        ## TODO : Deal with different rendered images to set up inputs to image load functions.
        controlnet_images = []      # PIL Images
        controlnet_cond_scales = []
        counter = 1
        if self.config.control_canny:
            print(f"Loading CONTROLNET-{counter} image and condition scale for CANNY...")
            counter += 1
            controlnet_images.append(
                self.get_canny_image(image_path, self.config.canny_threshold_min, self.config.canny_threshold_max)
            )
            controlnet_cond_scales.append(self.config.control_canny_cond_scale)
        if self.config.control_depth:
            print(f"Loading CONTROLNET-{counter} image and condition scale for DEPTH...")
            counter += 1
            controlnet_images.append(
                self.get_depth_image(image_path)
            )
            controlnet_cond_scales.append(self.config.control_depth_cond_scale)
        if self.config.control_seg:
            print(f"Loading CONTROLNET-{counter} image and condition scale for SEGMENTATION...")
            counter += 1
            controlnet_images.append(
                self.get_seg_image(image_path)
            )
            controlnet_cond_scales.append(self.config.control_seg_cond_scale)
        if self.config.control_normals:
            print(f"Loading CONTROLNET-{counter} image and condition scale for NORMALS...")
            counter += 1
            controlnet_images.append(
                self.get_normals_image(image_path)
            )
            controlnet_cond_scales.append(self.config.control_normals_cond_scale)
            
        # Get image resolution from control images since image resolution changes the generation process. Thus, it is important to set
        # image resolution same as the controlnet images. 
        # Also all controlnet images are rendered with same camera parameters. Due to that, checking only one of the controlnet image is sufficient.
        img_width = controlnet_images[0].width
        img_height = controlnet_images[0].height
            

        if self.config.check_nsfw_info:
            images, nsfw_info = self.pipe(
                            prompt,
                            negative_prompt=negative_prompt,
                            image=controlnet_images,
                            controlnet_conditioning_scale=controlnet_cond_scales,
                            num_inference_steps=self.config.num_inference_steps,
                            generator=generator
                        )       # nsfw_info = List[Bool]
            return {'image' :images, 'nsfw_info': nsfw_info}
        else:
            images = self.pipe(
                                prompt,
                                negative_prompt=negative_prompt,
                                width=img_width,
                                height=img_height,
                                image=controlnet_images,
                                controlnet_conditioning_scale=controlnet_cond_scales,
                                num_inference_steps=self.config.num_inference_steps,
                                generator=generator
            ).images

            return {'image' :images, 'nsfw_info': None}