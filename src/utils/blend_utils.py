from ..common import *

import bpy
import mathutils

def xyzw_to_wxyz(xyzw):
    x, y, z, w = xyzw
    return [w, x, y, z]

def get_axis_matrix(forward, up, pos):
    forward /= np.linalg.norm(forward)
    up /= np.linalg.norm(up)

    right = np.cross(forward, up)
    mat = np.eye(4)
    mat[:3, :3] = np.vstack([right, up, forward]).T
    mat[:3, -1] = np.array(pos)
    return mat.T

def get_facing_matrix(pos, target):
    forward = pos - target
    forward /= np.linalg.norm(forward)
    right = np.cross(np.array([0, 1, 0]), forward)
    up = np.cross(forward, right)
    
    mat = np.eye(4)
    mat[:3, :3] = np.vstack([right, up, forward]).T
    mat[:3, -1] = pos
    return mat.T

def select_none():
    for obj in bpy.data.objects:
        obj.select_set(False)

def group_in_collection(objs, name: str):

    '''
    objs: List of (None | Blender Object | List[Blender Object])

    Many of our 'create' functions may return nones or lists, hence them being accepted here for convinience
    '''

    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)

    for obj in objs:
        if obj is None:
            continue
        if not isinstance(obj, list):
            obj = [obj]
        for child in obj:
            collection.objects.link(child)
            bpy.context.scene.collection.objects.unlink(child)
            
def configure_principled_node(
        principled_node,
        base_color = (0.6, 0.6, 0.6, 1.0),
        subsurface: float = 0.0,
        subsurface_color = (0.8, 0.8, 0.8, 1.0),
        subsurface_radius= (1.0, 0.2, 0.1),
        metallic: float = 0.0,
        specular: float = 0.5,
        specular_tint: float = 0.0,
        roughness: float = 0.5,
        anisotropic: float = 0.0,
        anisotropic_rotation: float = 0.0,
        sheen: float = 0.0,
        sheen_tint: float = 0.5,
        clearcoat: float = 0.0,
        clearcoat_roughness: float = 0.03,
        ior: float = 1.45,
        transmission: float = 0.0,
        transmission_roughness: float = 0.0) -> None:
    principled_node.inputs['Base Color'].default_value = base_color
    principled_node.inputs['Subsurface'].default_value = subsurface
    principled_node.inputs['Subsurface Color'].default_value = subsurface_color
    principled_node.inputs['Subsurface Radius'].default_value = subsurface_radius
    principled_node.inputs['Metallic'].default_value = metallic
    principled_node.inputs['Specular'].default_value = specular
    principled_node.inputs['Specular Tint'].default_value = specular_tint
    principled_node.inputs['Roughness'].default_value = roughness
    principled_node.inputs['Anisotropic'].default_value = anisotropic
    principled_node.inputs['Anisotropic Rotation'].default_value = anisotropic_rotation
    principled_node.inputs['Sheen'].default_value = sheen
    principled_node.inputs['Sheen Tint'].default_value = sheen_tint
    principled_node.inputs['Clearcoat'].default_value = clearcoat
    principled_node.inputs['Clearcoat Roughness'].default_value = clearcoat_roughness
    principled_node.inputs['IOR'].default_value = ior
    principled_node.inputs['Transmission'].default_value = transmission
    principled_node.inputs['Transmission Roughness'].default_value = transmission_roughness

def clear_scene():

    # delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # delete all materials
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)

    # delete all collections
    for c in bpy.data.collections:
        bpy.data.collections.remove(c)
