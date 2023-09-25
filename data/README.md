This 'data' module contains all the data needed for modules under '/app/'.

'data' module stores data and a sub-module for preprocessing the raw data. Preprocessing sub-module saves the processed data into corresponding data type such as shapes, materials, etc.

'data/preprocess' sub-module process raw data to be ready-to-use by 'app/garmet_generator' module.

DIRECTORY CONFIGURATION:
\n    'app/data/shapes':
\n>                    -> shape_{0}
\n>>                                -> images
\n>>>                                        -> shape_0_SEGMENTATION.png
\n>>>                                        -> shape_0_DEPTH.png
\n>>>                                        -> shape_0_RENDER.png
\n>>>                                        -> shape_0_NORMALS.png
\n>                    .
\n>                    .
\n>                    .
\n>                    .

\n>                    -> shape_{n}

    
\n    'app/data/materials':
\n>                    -> database
\n>>                                -> stores all files related to create materials database
\n>>                                -> material_{0}
\n>>>                                                -> material_0_basecolor.png
\n>>>                                                -> material_0_normals.png
\n>>>                                                -> material_0_displacement.png
\n>>>                                                -> material_0_metalness.png
\n>>>                                                -> material_0_roughness.png
\n>>>                                                -> material_0_ao.png
\n>>>                                .
\n>>>                                .
\n>>>                                .
\n>>>                                .
\n>>>                                .
\n>>>                                -> material_{n}