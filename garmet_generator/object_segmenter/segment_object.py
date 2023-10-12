from pathlib import Path
from os.path import exists

class Garment3D():
    def __init__(self, obj_path) -> None:
        
        self.obj_path = obj_path
        self.obj = self.Import3DObject()
        
        self.vertices = self.GetAllVertices()
        
    
    def Import3DObject(self):
        
        return None
    
    def GetAllVertices(self):
        
        return None

def RenderObjectImages(obj_path : Path = None, views_count : int = 30):
    """
        Function to generate rendered images from multiple views for given object path.
        @inputs:
            - obj_path : Path to the object path. (Supported file formats: obj, glb)
            - view_count : Number of rendered images to be generated
        @returns:
            - List of all generated render images and dict of vertices and their positions on each generated render images. 
                e.i. vertices = {'img_0' : pix_coords, ... , ..., 'img_n' : pix_coords}
    """
    if not (obj_path and exists(obj_path)):
        raise FileNotFoundError(f"Provided object path doesn't exists: Given path : {obj_path}")
    
    garment3D = Garment3D(obj_path=obj_path)
    vertices = garment3D.vertices
    


INPUT_OBJ_PATH = ""
VERTICES = {
    #VERTEX_ID : [PREDICTED PART ID]
}

############## Generate multiple view render images of the object.
# view_images: 
view_images, image_2_vertex = RenderObjectImages()

############## For each render images -> predict semantic segmentation 
for render_id, img in enumerate(view_images):
    ############# Run semantic segmentation
    segments = RunSegmentation(img)     # Pixel-level classification
    
    ############# Parse pixel-wise classification to corresponding vertex value
    for segment in segments:
        pixel_coordinates = GetPixelCoordinatesForSegment(segment)
        #### Look up to corresponding vertex
        vertex_id = image_2_vertex[render_id][pixel_coordinates]
        
        
        
        VERTICES[vertex_id].append(segment.CATEGORY)


######### Once all rendered images segmented, manipulate 3D object file to insert the segments.

######### For each vertex use VOTING mechanism or general DOMINANT CAT type of determination of the category
for vertex_id, preds in enumerate(VERTICES):
    final_pred = max(preds)
    VERTICES[vertex_id] = final_pred # UPDATE THE DICT AS YOU GO.
    

######## 3D Object update
vert_ids, cats = VERTICES.items()
total_cat_count = len(set(vals))
colors = GetRandomColors(how_many=total_cat_count)

parts = []
for cat in cats:
    cat_vertices = GetCatVertices(cat)

    part = GroupCatVertices(cat_vertices)
    
    # Generate a new 3D object for each part
    part_obj = Obj(part)


final_obj = CombineParts(parts=parts)
final_obj.save(OUTPUT_OBJ_PATH)