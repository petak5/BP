# Installation

## End user installation
- Download the latest release from [here](https://github.com/petak5/BP/releases/) or create the `.zip` manually from `src/` folder and install the `.zip` file from Blender (`Preferences -> Add-ons -> Install`)

## Development installation (changes to code are applied to plugin after Blender restarts)
- Create a symlink to `src/` folder from Blender's addons folder
### macOS
- `cd /Users/<user>/Library/Application Support/Blender/<blender-version>/scripts/addons/`
- `ln -s erosion_plugin <path-to-src>`
### Windows (cmd as Administrator)
- `cd c:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\<blender-version>\scripts\addons\`
- `mklink /D erosion_plugin <path-to-src>` 
