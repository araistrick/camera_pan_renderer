import os
import argparse
from pathlib import Path

import bpy
import numpy as np

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def use_cuda():
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
    print(bpy.context.preferences.addons["cycles"].preferences.get_devices())
    bpy.context.preferences.addons["cycles"].preferences.devices[0].use = True
    bpy.context.scene.cycles.device = "GPU"
    bpy.context.scene.render.tile_x = 128
    bpy.context.scene.render.tile_x = 128
    print('Using GPU device:', bpy.context.preferences.addons["cycles"].preferences.devices[0])

def select_none():
    for obj in bpy.data.objects:
        obj.select_set(False)

def render_ply(args, ply_path):

    ply_name = ply_path.parts[-1]
    ply_id = '_'.join(list(ply_name.split('_'))[1:])

    # import the requisite ply
    select_none()
    print(f"Importing {ply_path}")
    bpy.ops.import_mesh.ply(filepath=str(ply_path))
    imported_ply = bpy.context.selected_objects[0]

    # rotate it correctly
    imported_ply.rotation_euler = np.radians(np.array(args.override_ply_euler))

    # make it colored according to vertex colors
    material = next(m for m in bpy.data.materials if m.name == args.template_material_name)
    if imported_ply.data.materials:
        imported_ply.data.materials[0] = material
    else:
        imported_ply.data.materials.append(material)

    # configure render output location
    outpath = Path(args.output_folder)/ply_id
    outpath.mkdir(exist_ok=True, parents=True)
    bpy.context.scene.render.filepath = str(outpath) + '/'

    bpy.ops.render.render(animation=True, write_still=True)

    # clean up
    select_none()
    imported_ply.select_set(True)
    bpy.ops.object.delete()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str)
    parser.add_argument('output_folder', type=str)
    parser.add_argument('--template_file', type=str, default='template.blend')
    parser.add_argument('--override_ply_euler', type=int, nargs='+', default=[90, 0, 0])
    parser.add_argument('--template_material_name', type=str, default='vertex color')
    parser.add_argument('--cuda', action='store_true')
    args = parser.parse_args()

    bpy.ops.wm.open_mainfile(filepath=args.template_file)

    if args.cuda:
        use_cuda()

    input_paths = list(Path(args.input_folder).glob('*.ply'))
    print(f"Starting processing of {len(input_paths)} .plys from {args.input_folder}")
    for ply_path in input_paths:
        render_ply(args, ply_path)

if __name__ == '__main__':
    main()