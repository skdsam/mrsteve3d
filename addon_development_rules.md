# Blender Addon Development Rules & Guidelines

This document outlines the architecture, compatibility strategies, and error-handling procedures for the **Mr Steve 3D** Blender addon suite, ensuring support across Blender versions **3.6 to 5.2+**.

---

## 1. Compatibility Strategy (Blender 3.6 - 5.2)

### A. Extension vs. Legacy Addon Support
* **Blender 4.2+ (Extensions):** Uses a `blender_manifest.toml` metadata file.
* **Blender 3.6 - 4.1 (Legacy Addons):** Uses the `bl_info` dictionary in `__init__.py`.
* **Rule:** We must maintain both `bl_info` in `__init__.py` and a `blender_manifest.toml` at the root.

### B. Responsive Preferences & Word Wrapping
* In Blender 4.0+, `layout.label(text="...", word_wrap=True)` is supported.
* In Blender 3.6, `word_wrap` is NOT supported on labels.
* **Rule:** Implement a fallback text-wrapping helper in Python that splits strings into lines fitting the layout if Blender version is < 4.0.

### C. Robust Preferences Access
Extension packages in Blender 4.2+ are prefixed (e.g., `bl_ext.user_default.my_addon`).
* **Rule:** Access preferences dynamically using:
  ```python
  def get_prefs(context):
      package_name = __package__ if __package__ else __name__
      return context.preferences.addons.get(package_name).preferences
  ```

---

## 2. Core Addon Features

1. **3-Point Lighting System:**
   - Adds Key, Fill, and Rim lights (Spot, Point, or Area lights).
   - Constrained/parented or positioned relative to the selected object's bounding box/location.
2. **Camera Tracking:**
   - Adds a Camera with a `Track To` constraint targeting the active object.
3. **Panel Controls:**
   - Lighting intensity, color, and positioning controls.
   - Active camera selection, and camera Depth of Field (DoF) controls directly exposed in the custom panel.

---

## 3. Dos and Don'ts (Error Prevention & Recovery)

### DOs
* **DO** check if `context.active_object` is not `None` before attempting to assign constraints, parent objects, or create lighting setups.
* **DO** use `mathutils` for matrix and vector calculations to ensure correct transformation placement in 3D space.
* **DO** register and unregister all classes cleanly using `bpy.utils.register_class` and `bpy.utils.unregister_class`.
* **DO** use standard Blender naming conventions for new objects so they can be easily cleaned up or identified by the user.

### DON'Ts
* **DON'T** use hardcoded collection names (like `Collection` or `Collection 1`) which might not exist; instead, use `context.collection` or the active collection.
* **DON'T** call `bpy.ops` directly for object property modification if it can be done via direct data API manipulation (e.g., `obj.location = ...` instead of `bpy.ops.transform.translate(...)`).
* **DON'T** assume the user is in Object Mode. Always check or temporarily set context mode when performing object creation/linking.
