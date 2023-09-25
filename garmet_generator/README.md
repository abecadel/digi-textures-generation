'app/garment_generator' module contains sub-modules and a 'main.py' script.
Sub-modules are designed to accomplish a single high-level task. 
'main.py' script integrates all sub-modules to make the framework end-to-end.
'main.py' integrates the sub-modules in the order of:
    - image_generator : With given segmented shape and its render images (segmentation, normals, depth, render view), 
                        it generates a novel appearance by utilizing Stable Diffusion + ControlNet and given user prompt.

    - material_predictor : This sub-module uses the output of the image_generator, segmentation map of the rendered 
                        shape and database of materials under the 'app/data/materials' with similarity scores to predict 
                        the materials for the segments on the generated image.
                        
    - material_transfer : This sub-module uses blender to assign the predicted materials from the previous step to given 
                        3D garment shape and stores the results under 'app/outputs'
