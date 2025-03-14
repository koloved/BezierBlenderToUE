bl_info = {
    "name": "Export BezierCSV for UE4",
    "blender": (4, 3, 0),  # Updated for Blender 4.3
    "author": "Alex Z.",
    "location": "File > Export > BezierCSV For UE (.csv)",
    "category": "Import-Export",
}

import os
import bpy
from bpy_extras.io_utils import ExportHelper  # Changed to ExportHelper
from bpy.props import StringProperty

class ObjectExportPoints(bpy.types.Operator, ExportHelper):  # Now using ExportHelper
    bl_idname = "me.export_bezier_points" 
    bl_label = "Export BezierCSV to UE4"   
    
    # File type settings
    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'}
    )
    
    SCALE_FACTOR = 100.0  # Centralized scale factor
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'CURVE':
            self.report({"WARNING"}, "Selected object isn't a curve")
            return {'CANCELLED'}

        beziers = [s for s in obj.data.splines if s.type == 'BEZIER']
        if not beziers:
            self.report({"WARNING"}, "Selected object isn't a Bezier curve")
            return {'CANCELLED'}
        
        with open(self.filepath, "w") as save_file:  # Removed manual .csv append
            save_file.write("name,px,py,pz,hlx,hly,hlz,hrx,hry,hrz\n")
            
            line_template = ("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,"
                           "%.6f,%.6f,%.6f\n")
            
            count = 1
            for bezier in beziers:
                for point in bezier.bezier_points:
                    data = {
                        'co': point.co * self.SCALE_FACTOR,
                        'hl': point.handle_left * self.SCALE_FACTOR,
                        'hr': point.handle_right * self.SCALE_FACTOR
                    }
                    
                    line = line_template % (
                        count,
                        data['co'].x, 
                        -data['co'].y,  # Flipping Y-axis for UE4
                        data['co'].z,
                        data['hl'].x,
                        -data['hl'].y,   # Flipping Y-axis
                        data['hl'].z,
                        data['hr'].x,
                        -data['hr'].y,   # Flipping Y-axis
                        data['hr'].z
                    )
                    save_file.write(line)
                    count += 1
        
        self.report({"INFO"}, f"Exported {count-1} points successfully")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(ObjectExportPoints.bl_idname, 
                        text="Export BezierCSV For UE4 (.csv)")

def register():
    bpy.utils.register_class(ObjectExportPoints)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ObjectExportPoints)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
