bl_info = {
    "name": "Sun Beams Locator",
    "blender": (3, 1, 0),
    "category": "Node",
}

import bpy
import math as m

def update_location():
    x1 = bpy.data.objects["Camera"].location[0]
    y1 = bpy.data.objects["Camera"].location[1]
    z1 = bpy.data.objects["Camera"].location[2]
    x2 = bpy.data.objects["Suzanne.001"].location[0]
    y2 = bpy.data.objects["Suzanne.001"].location[1]
    z2 = bpy.data.objects["Suzanne.001"].location[2]
    xrot = bpy.data.objects["Camera"].rotation_euler[0]
    yrot = bpy.data.objects["Camera"].rotation_euler[1]
    zrot = bpy.data.objects["Camera"].rotation_euler[2]
    
    ez = bpy.data.cameras["Camera"].lens/18
    # Get the coordinates of the target relative to the camera
    dx = m.cos(yrot) * (m.sin(zrot) * (y2 - y1) + m.cos(zrot) * (x2 - x1)) - (m.sin(yrot) * (z2 - z1))
    dy = m.sin(xrot) * (m.cos(yrot) * (z2 - z1) + m.sin(yrot) * (m.sin(zrot) * (y2 - y1) + m.cos(zrot) * (x2 - x1))) + m.cos(xrot) * (m.cos(zrot) * (y2 - y1) - m.sin(zrot) * (x2 - x1))
    dz = -(m.cos(xrot) * (m.cos(yrot) * (z2 - z1) + m.sin(yrot) * (m.sin(zrot) * (y2 - y1) + m.cos(zrot) * (x2 - x1))) - m.sin(xrot) * (m.cos(zrot) * (y2 - y1) - m.sin(zrot) * (x2 - x1)))

    sx = bpy.data.scenes["Scene"].render.resolution_x
    sy = bpy.data.scenes["Scene"].render.resolution_y
    proportion_x = sy/sx if sx < sy else 1
    proportion_y = sx/sy if sx > sy else 1
    length_save = bpy.data.scenes["Scene"].node_tree.nodes["Sun Beams"].ray_length
    
    # Project the 3D scene into 2D
    if dz >= 0:
        bpy.data.scenes["Scene"].node_tree.nodes["Sun Beams"].source[0] = ((dx*ez/dz)/2)*proportion_x + 0.5
        bpy.data.scenes["Scene"].node_tree.nodes["Sun Beams"].source[1] = ((dy*ez/dz)/2)*proportion_y + 0.5
    else:
        #just to remove the thing from the screen
        bpy.data.scenes["Scene"].node_tree.nodes["Sun Beams"].source[0] = 999
        bpy.data.scenes["Scene"].node_tree.nodes["Sun Beams"].source[1] = 999

class SunBeamsLocator(bpy.types.Operator):
    bl_idname = "object.sun_beam_locate"
    bl_label = "Sun Beams Locator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.handlers.frame_change_pre.append(update_location)

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SunBeamsLocator.bl_idname)

def register():
    bpy.utils.register_class(SunBeamsLocator)
    bpy.types.VIEW3D_MT_object.append(menu_func)  

def unregister():
    bpy.utils.unregister_class(SunBeamsLocator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)  

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
