bl_info = {
    "name": "Auto 3-Point Studio",
    "author": "SkdSam & Mr Steve 3D",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Steve 3D",
    "description": "Creates a 3-point lighting setup and tracked camera for the active object.",
    "warning": "",
    "doc_url": "",
    "category": "Lighting",
}

import bpy
import math
import textwrap
from bpy.props import (
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    StringProperty,
    PointerProperty,
)

# -------------------------------------------------------------------
# Helper Functions & Preferences
# -------------------------------------------------------------------

def get_prefs(context):
    package_name = __package__ if __package__ else __name__
    return context.preferences.addons.get(package_name).preferences

class Auto3PointStudioPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__ if __package__ else __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Auto 3-Point Studio", icon='LIGHT')
        
        box = layout.box()
        box.label(text="Authors: SkdSam & Mr Steve 3D", icon='USER')
        
        info_text = (
            "This addon automatically generates a professional 3-point lighting rig "
            "(Key, Fill, and Rim lights) and a Camera targeting the selected object. "
            "You can adjust light properties, positions, and Depth of Field directly from "
            "the 'Steve 3D' tab in the 3D Viewport Sidebar (N-panel)."
        )
        
        # Word wrapping for responsiveness across Blender versions
        if hasattr(layout, "label") and hasattr(bpy.app, "version") and bpy.app.version >= (4, 0, 0):
            box.label(text=info_text, word_wrap=True)
        else:
            lines = textwrap.wrap(info_text, width=60)
            for line in lines:
                box.label(text=line)

# -------------------------------------------------------------------
# Update Callbacks for Real-Time Adjustments
# -------------------------------------------------------------------

def update_studio_lights(self, context):
    scene = context.scene
    props = scene.auto_3point_studio_properties
    
    target_obj = bpy.data.objects.get(props.target_name)
    if not target_obj:
        return
        
    target_loc = target_obj.location
    
    # 1. Update Key Light
    key_light = bpy.data.objects.get(props.key_light_name)
    if key_light and key_light.type == 'LIGHT':
        key_light.data.energy = props.key_energy
        key_light.data.color = props.key_color
        rad = math.radians(props.key_angle)
        key_light.location.x = target_loc.x + props.key_distance * math.cos(rad)
        key_light.location.y = target_loc.y + props.key_distance * math.sin(rad)
        key_light.location.z = target_loc.z + props.key_height
        
    # 2. Update Fill Light
    fill_light = bpy.data.objects.get(props.fill_light_name)
    if fill_light and fill_light.type == 'LIGHT':
        fill_light.data.energy = props.fill_energy
        fill_light.data.color = props.fill_color
        rad = math.radians(props.fill_angle)
        fill_light.location.x = target_loc.x + props.fill_distance * math.cos(rad)
        fill_light.location.y = target_loc.y + props.fill_distance * math.sin(rad)
        fill_light.location.z = target_loc.z + props.fill_height
        
    # 3. Update Rim Light
    rim_light = bpy.data.objects.get(props.rim_light_name)
    if rim_light and rim_light.type == 'LIGHT':
        rim_light.data.energy = props.rim_energy
        rim_light.data.color = props.rim_color
        rad = math.radians(props.rim_angle)
        rim_light.location.x = target_loc.x + props.rim_distance * math.cos(rad)
        rim_light.location.y = target_loc.y + props.rim_distance * math.sin(rad)
        rim_light.location.z = target_loc.z + props.rim_height
        
    # 4. Update Camera
    camera = bpy.data.objects.get(props.camera_name)
    if camera and camera.type == 'CAMERA':
        rad = math.radians(props.cam_angle)
        camera.location.x = target_loc.x + props.cam_distance * math.cos(rad)
        camera.location.y = target_loc.y + props.cam_distance * math.sin(rad)
        camera.location.z = target_loc.z + props.cam_height
        
        # Depth of Field
        camera.data.dof.use_dof = props.cam_dof_enabled
        camera.data.dof.focus_object = target_obj
        camera.data.dof.aperture_fstop = props.cam_dof_fstop

# -------------------------------------------------------------------
# Properties Registration
# -------------------------------------------------------------------

class StudioLightingProperties(bpy.types.PropertyGroup):
    # Object references (by name for stability)
    target_name: StringProperty(default="")
    key_light_name: StringProperty(default="")
    fill_light_name: StringProperty(default="")
    rim_light_name: StringProperty(default="")
    camera_name: StringProperty(default="")

    # Key Light settings
    key_energy: FloatProperty(name="Key Intensity", default=1000.0, min=0.0, update=update_studio_lights)
    key_color: FloatVectorProperty(name="Key Color", subtype='COLOR', default=(1.0, 0.95, 0.9), min=0.0, max=1.0, update=update_studio_lights)
    key_distance: FloatProperty(name="Key Distance", default=5.0, min=0.1, update=update_studio_lights)
    key_angle: FloatProperty(name="Key Angle (deg)", default=45.0, min=-360.0, max=360.0, update=update_studio_lights)
    key_height: FloatProperty(name="Key Height", default=3.0, update=update_studio_lights)

    # Fill Light settings
    fill_energy: FloatProperty(name="Fill Intensity", default=300.0, min=0.0, update=update_studio_lights)
    fill_color: FloatVectorProperty(name="Fill Color", subtype='COLOR', default=(0.9, 0.95, 1.0), min=0.0, max=1.0, update=update_studio_lights)
    fill_distance: FloatProperty(name="Fill Distance", default=5.0, min=0.1, update=update_studio_lights)
    fill_angle: FloatProperty(name="Fill Angle (deg)", default=-45.0, min=-360.0, max=360.0, update=update_studio_lights)
    fill_height: FloatProperty(name="Fill Height", default=2.0, update=update_studio_lights)

    # Rim Light settings
    rim_energy: FloatProperty(name="Rim Intensity", default=800.0, min=0.0, update=update_studio_lights)
    rim_color: FloatVectorProperty(name="Rim Color", subtype='COLOR', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, update=update_studio_lights)
    rim_distance: FloatProperty(name="Rim Distance", default=6.0, min=0.1, update=update_studio_lights)
    rim_angle: FloatProperty(name="Rim Angle (deg)", default=180.0, min=-360.0, max=360.0, update=update_studio_lights)
    rim_height: FloatProperty(name="Rim Height", default=4.0, update=update_studio_lights)

    # Camera settings
    cam_distance: FloatProperty(name="Camera Distance", default=7.0, min=0.1, update=update_studio_lights)
    cam_angle: FloatProperty(name="Camera Angle (deg)", default=0.0, min=-360.0, max=360.0, update=update_studio_lights)
    cam_height: FloatProperty(name="Camera Height", default=1.5, update=update_studio_lights)
    
    # Depth of Field settings
    cam_dof_enabled: BoolProperty(name="Enable DoF", default=True, update=update_studio_lights)
    cam_dof_fstop: FloatProperty(name="F-Stop", default=2.8, min=0.1, max=128.0, update=update_studio_lights)

# -------------------------------------------------------------------
# Operators
# -------------------------------------------------------------------

class OBJECT_OT_setup_3point_studio(bpy.types.Operator):
    bl_idname = "object.setup_3point_studio"
    bl_label = "Setup 3-Point Studio"
    bl_description = "Creates a 3-point lighting setup and a tracked camera targeting the selected object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        target = context.active_object
        scene = context.scene
        props = scene.auto_3point_studio_properties
        
        # Keep track of target name
        props.target_name = target.name
        
        # Ensure we are in Object Mode
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        # Create or retrieve target collection
        col_name = "Steve3D Studio"
        if col_name in bpy.data.collections:
            studio_col = bpy.data.collections[col_name]
        else:
            studio_col = bpy.data.collections.new(col_name)
            scene.collection.children.link(studio_col)

        # Helper to create/link objects
        def get_or_create_light(name, light_type):
            light_obj = bpy.data.objects.get(name)
            if not light_obj:
                light_data = bpy.data.lights.new(name=name, type=light_type)
                light_obj = bpy.data.objects.new(name=name, object_data=light_data)
                studio_col.objects.link(light_obj)
            return light_obj

        def get_or_create_camera(name):
            cam_obj = bpy.data.objects.get(name)
            if not cam_obj:
                cam_data = bpy.data.cameras.new(name=name)
                cam_obj = bpy.data.objects.new(name=name, object_data=cam_data)
                studio_col.objects.link(cam_obj)
            return cam_obj

        # 1. Create lights (Key, Fill, Rim)
        key_light = get_or_create_light("Steve3D_Key_Light", 'SPOT')
        fill_light = get_or_create_light("Steve3D_Fill_Light", 'POINT')
        rim_light = get_or_create_light("Steve3D_Rim_Light", 'SPOT')

        # Configure spotlights specifically for targeting/focusing
        key_light.data.spot_size = math.radians(45)
        rim_light.data.spot_size = math.radians(45)

        props.key_light_name = key_light.name
        props.fill_light_name = fill_light.name
        props.rim_light_name = rim_light.name

        # 2. Create camera
        camera = get_or_create_camera("Steve3D_Studio_Camera")
        props.camera_name = camera.name
        scene.camera = camera

        # 3. Add constraint to lights and camera to target the object
        def setup_constraint(obj, target_obj):
            # Check if Track To constraint exists
            track_constraint = None
            for c in obj.constraints:
                if c.type == 'TRACK_TO':
                    track_constraint = c
                    break
            if not track_constraint:
                track_constraint = obj.constraints.new(type='TRACK_TO')
            track_constraint.target = target_obj
            track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
            track_constraint.up_axis = 'UP_Y'

        setup_constraint(key_light, target)
        setup_constraint(fill_light, target)
        setup_constraint(rim_light, target)
        setup_constraint(camera, target)

        # Trigger update to set initial locations and values
        update_studio_lights(props, context)

        self.report({'INFO'}, "Auto 3-Point Studio Rig Created!")
        return {'FINISHED'}

# -------------------------------------------------------------------
# Interface Panel
# -------------------------------------------------------------------

class VIEW3D_PT_auto_3point_studio(bpy.types.Panel):
    bl_label = "Auto 3-Point Studio"
    bl_idname = "VIEW3D_PT_auto_3point_studio"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Steve 3D'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.auto_3point_studio_properties

        # Warning if no active object
        active_obj = context.active_object
        if not active_obj:
            layout.label(text="Select an object first!", icon='ERROR')
            return

        # Setup Button
        layout.operator("object.setup_3point_studio", icon='LIGHTPRESET', text="Setup Studio Rig")

        # Rig Status & Settings
        target_obj = bpy.data.objects.get(props.target_name)
        if target_obj:
            box = layout.box()
            box.label(text=f"Target: {props.target_name}", icon='OBJECT_DATA')

            # Key Light Panel
            col = box.column(align=True)
            col.label(text="Key Light Settings (Spot)", icon='LIGHT')
            col.prop(props, "key_energy")
            col.prop(props, "key_color")
            col.prop(props, "key_distance")
            col.prop(props, "key_angle")
            col.prop(props, "key_height")

            # Fill Light Panel
            col = box.column(align=True)
            col.label(text="Fill Light Settings (Point)", icon='LIGHT')
            col.prop(props, "fill_energy")
            col.prop(props, "fill_color")
            col.prop(props, "fill_distance")
            col.prop(props, "fill_angle")
            col.prop(props, "fill_height")

            # Rim Light Panel
            col = box.column(align=True)
            col.label(text="Rim Light Settings (Spot)", icon='LIGHT')
            col.prop(props, "rim_energy")
            col.prop(props, "rim_color")
            col.prop(props, "rim_distance")
            col.prop(props, "rim_angle")
            col.prop(props, "rim_height")

            # Camera Panel
            col = box.column(align=True)
            col.label(text="Camera Settings", icon='CAMERA_DATA')
            col.prop(props, "cam_distance")
            col.prop(props, "cam_angle")
            col.prop(props, "cam_height")
            
            # Depth of Field Controls
            col.prop(props, "cam_dof_enabled")
            if props.cam_dof_enabled:
                col.prop(props, "cam_dof_fstop")

# -------------------------------------------------------------------
# Register / Unregister
# -------------------------------------------------------------------

classes = (
    Auto3PointStudioPreferences,
    StudioLightingProperties,
    OBJECT_OT_setup_3point_studio,
    VIEW3D_PT_auto_3point_studio,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.auto_3point_studio_properties = PointerProperty(type=StudioLightingProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.auto_3point_studio_properties

if __name__ == "__main__":
    register()
