# Camera Pan Renderer
A simple utility designed for rendering animations of PLY files with vertex-colors. In practice, all it does is load up template.blend, import the PLY, set up the materials, and hit the 'render animation' button

## Installation

Use the provided environment.yml to create a conda environment:
```conda env create -f environment.yml```

This will attempt to install blender as a python module under the name `bpy`. It can be quite finicky however. Make sure you are using python3.7.10.

Then, finish installing blender by running:
```bpy_post_install```

### Alternative for bpy install 
Follow instructions from here [https://github.com/TylerGubala/blenderpy/releases/tag/v2.91a0]
````
  1. Install blender dependecies from https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu
  2. Download the wheel distribution from https://github.com/TylerGubala/blenderpy/releases/tag/v2.91a0
  3. pip install bpy-2.91a0-cp37-cp37m-manylinux2014_x86_64.whl && bpy_post_install
````

## Setup

Given a PLY with vertex colors, the script will:
1. Open up blend_files/template.blend
2. Import your PLY at the origin
3. Set the material of your PLY to be a material named "vertex_color" (a material which already exists in the provided template.blend)
4. Set the PLY orientation to be the value found in render.yaml's "override_ply_euler"
5. 'Render Animation'using EEVEE

So, to make sure you will get sensible output, you should follow those steps yourself using an example PLY file, and make modifications to `template.blend` or `config/render.yaml` as necessary.

If you wish, you can affect the program behavior by modifying `template.blend` via the Blender UI, for example by:
- Editing the position / location / intensity of lights relative to your PLY file
- Editing the camera trajectory. Pro-tip: Select the curve, and search for "Convert To" and convert the Curve object to a Mesh. Edit it as a mesh using Proportional Editing, then use "Convert To" to turn it back into a camera curve. You may need to re-assign the cameras 'Follow' constraint to point at the curve again once editing is done. 
- Changing the camera properties or render resolution

## Running the script
```python render.py <input_folder>```

If input_folder is not provided, the program will attempt to use `dataset.plys_folder` from `config/render.yaml`.

