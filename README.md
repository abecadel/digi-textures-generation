Directories:
\n    /app/
\n>        -> data/
\n>>                -> __init__.py
\n>>                -> materials
\n>>                -> shapes
\n>>                -> preprocess
\n>>>                        -> materials
\n>>>                        -> shapes
\n>        -> garment_generator/
\n>>                -> __init__.py
\n>>                -> image_generator
\n>>                -> material_predictor
\n>>                -> material_transfer
\n>        -> outputs/
\n>>                ->
\n>        -> main.py
\n>        -> config.py
\n>        -> requirements.txt
\n>        -> README.md

This repository is to generate novel appearances for provided 3D garment objects in end-to-end framework.
'main.py' integrates all sub-modules with single high-level tasks. 