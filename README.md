# Terrain eroder
Blender plugin for terrain erosion

<img src="https://github.com/petak5/BP/blob/master/resources/screenshot_hydraulic_erosion.png?raw=true">

# Installation
- Download the latest release from [here](https://github.com/petak5/BP/releases/) or create the `.zip` manually from `terrain_eroder/` folder and install the `.zip` file from Blender (`Preferences -> Add-ons -> Install`)

# Development
## Installation (changes to code are applied to plugin after Blender restarts)
- Create a symlink to `terrain_eroder/` folder from Blender's addons folder
### macOS
- `cd /Users/<user>/Library/Application\ Support/Blender/<blender-version>/scripts/addons/`
- `ln -s <path-to-terrain-eroder> terrain_eroder`
### Windows (cmd as Administrator)
- `cd "c:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\<blender-version>\scripts\addons\"`
- `mklink /D terrain_eroder <path-to-terrain-eroder>`

# Features
### Terrain generation
Create terrain based on built in noise functions (`mathutils` module in Blender)
<img src="https://github.com/petak5/BP/blob/master/resources/screenshot_generated_terrain.png?raw=true">

### Thermal erosion
<img src="https://github.com/petak5/BP/blob/master/resources/screenshot_thermal_erosion.png?raw=true">

### Hydraulic erosion
<img src="https://github.com/petak5/BP/blob/master/resources/screenshot_hydraulic_erosion.png?raw=true">

### Rainfall area selection
Select where the rain falls using vertex groups and paint tools built into Blender
<img src="https://github.com/petak5/BP/blob/master/resources/screenshot_vertex_group_paint.png?raw=true">
<img src="https://github.com/petak5/BP/blob/master/resources/screenshot_hydraulic_erosion_vertex_group.png?raw=true">