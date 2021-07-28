from src.common import *
from src.utils import blend_utils
from src.utils.stdout_utils import RedirectAllStdout

import bpy
import numpy as np

import os
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

def main():

    cfg = OmegaConf.load('config/render.yaml')

    bpy.ops.wm.open_mainfile(filepath=str(cfg.dataset.template_file))

    if cfg.use_cuda:
        use_cuda()

    example_paths = list(Path(cfg.dataset.plys_folder).iterdir())
    print(f"Starting processing of {len(example_paths)} scenes")
    for example_folder_path in example_paths:

        example_id = example_folder_path.parts[-1]

        for ply_path in example_folder_path.iterdir():

            ply_name = ply_path.parts[-1]
            ply_id = '_'.join(list(ply_name.split('_'))[1:])

            # import the requisite ply
            blend_utils.select_none()
            print(f"Importing {ply_path}")
            with RedirectAllStdout('/dev/null'):
                bpy.ops.import_mesh.ply(filepath=str(ply_path))
            imported_ply = bpy.context.selected_objects[0]

            # rotate it correctly
            imported_ply.rotation_euler = np.radians(np.array(cfg.override_ply_euler))

            # make it colored according to vertex colors
            material = bpy.data.materials[-1]
            assert material.name == 'vertex color'
            if imported_ply.data.materials:
                imported_ply.data.materials[0] = material
            else:
                imported_ply.data.materials.append(material)

            # configure render output location
            outpath = Path(cfg.output.output_base_dir)/example_id/ply_id
            outpath.mkdir(exist_ok=True, parents=True)
            bpy.context.scene.render.filepath = str(outpath) + '/'

            bpy.ops.render.render(animation=True, use_viewport=True, write_still=True)

            # clean up the ply
            blend_utils.select_none()
            imported_ply.select_set(True)
            bpy.ops.object.delete()



if __name__ == '__main__':
    main()