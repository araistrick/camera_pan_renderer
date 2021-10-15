# Camera Pan Renderer
A simple script for rendering animations of .ply files with vertex-colors. 

## Installation

This script was designed to use `bpy` as a module, [courtesy of this repo](https://github.com/TylerGubala/blenderpy/releases/tag/v2.91a0). The following install instructions provide how to do this. Alternatively, you may run the script using blender's python using `blender --python render.py <input_folder> <output_folder>`. 


#### Installing bpy as a module

You may attempt `pip install numpy future_fstrings bpy`, but in my experience installing `bpy` in this way fails. 

Instead, follow instructions from here [https://github.com/TylerGubala/blenderpy/releases/tag/v2.91a0]
````
  1. Install blender dependecies from https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu
  2. Download the wheel distribution from https://github.com/TylerGubala/blenderpy/releases/tag/v2.91a0
  3. pip install bpy-2.91a0-cp37-cp37m-manylinux2014_x86_64.whl && bpy_post_install
````
Regardless of which method you used, once `bpy` is installed, run `bpy_post_install` in your terminal.

## Setup

By default, for a given .ply with vertex colors, the script will:
1. Open up template.blend
2. Import your .ply at the origin
3. Set the material of your .ply to be a material named "vertex_color" (a material which already exists in the provided template.blend)
4. Rotate the ply by 90deg around the X axis (as specified by --override_ply_euler's default value)
5. Click 'Render Animation'

So, to make sure you will get sensible output, you should follow those steps yourself using an example PLY file, and make modifications to `template.blend` or any commandline arguments as necessary.

If you wish, you can affect the program behavior by modifying `template.blend` via the Blender UI, for example by:
- Editing the position / location / intensity of lights relative to your PLY file
- Editing the camera trajectory. Pro-tip: Select the curve, and search for "Convert To" and convert the Curve object to a Mesh. Edit it as a mesh using Proportional Editing, then use "Convert To" to turn it back into a camera curve. You may need to re-assign the cameras 'Follow' constraint to point at the curve again once editing is done. 
- Changing the camera properties or render resolution

## Running the script
```python render.py <input_folder> <output_folder>```, where input_folder contains a set of ply files to be rendered. For each .ply file in the input folder, the script will produce a folder of rendered frames in the output_folder. You may process these into a video as shown in these [ffmpeg examples](https://trac.ffmpeg.org/wiki/Slideshow)
