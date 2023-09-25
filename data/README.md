This 'data' module contains all the data needed for modules under '/app/'.

'data' module stores data and a sub-module for preprocessing the raw data. Preprocessing sub-module saves the processed data into corresponding data type such as shapes, materials, etc.

'data/preprocess' sub-module process raw data to be ready-to-use by 'app/garmet_generator' module.

DIRECTORY CONFIGURATION:

    'app/data/shapes':  
                    -> shape_{0}  
                                -> images  
                                        -> shape_0_SEGMENTATION.png  
                                        -> shape_0_DEPTH.png  
                                        -> shape_0_RENDER.png  
                                        -> shape_0_NORMALS.png  
                    .  
                    .  
                    .  
                    .  

                    -> shape_{n}  

    'app/data/materials':  
                    -> database  
                                -> stores all files related to create materials database  
                                -> material_{0}  
                                                -> material_0_basecolor.png  
                                                -> material_0_normals.png  
                                                -> material_0_displacement.png  
                                                -> material_0_metalness.png  
                                                -> material_0_roughness.png  
                                                -> material_0_ao.png  
                                .  
                                .  
                                .  
                                .  
                                .  
                                -> material_{n}  
