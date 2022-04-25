# Installation

## End user installation
- Download the latest release from [here](https://github.com/petak5/BP/releases/) or create the `.zip` manually from `erosion_plugin/` folder and install the `.zip` file from Blender (`Preferences -> Add-ons -> Install`)

## Development installation (changes to code are applied to plugin after Blender restarts)
- Create a symlink to `erosion_plugin/` folder from Blender's addons folder
### macOS
- `cd /Users/<user>/Library/Application Support/Blender/<blender-version>/scripts/addons/`
- `ln -s erosion_plugin <path-to-erosion-plugin>`
### Windows (cmd as Administrator)
- `cd c:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\<blender-version>\scripts\addons\`
- `mklink /D erosion_plugin <path-to-erosion-plugin>` 
