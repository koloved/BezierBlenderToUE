# BezierBlenderToUE
Export Bezier curve from Blender to Unreal Engine 5.

The article is available [here](https://medium.com/@qerrant/export-spline-from-blender-to-unreal-engine-28a4ccdd97c0). 

## List
* **ExportBezierToUE.py** - Blender add-on
* **Spline** - Unreal Engine project
  * **BlueprintVersion** - Blueprint solution
* **TestSpline.csv** - Test file

## Guide
1. Install add-on in Blender:
  Edit -> Preferences... -> Add-ons -> Install (ExportBezierToUE.py)
2. Export Bezier curve points into CSV:
  Select object and File -> Export -> Export BezierCSV for UE4
3. Import CSV such as DataTable (SplineStruct) in Unreal Engine 5
4. Select DataTable in BP_Spline_V