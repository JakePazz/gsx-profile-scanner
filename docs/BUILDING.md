# Building Guide

Use these instructions to create a distributable installer (and executable) to allow the program to be used on a system without a python interpreter. This guide is primarily for future me when I forget how to do this, but can also be used as a guide if adding your own changes/additions.

## Steps

### [1]

*Option 1*

Launch 'Auto Py To Exe' within cmd using `python -m auto_py_to_exe` and use the provided and configure the settings yourself or copy the values below into a json file and import it under `Settings > Configuration` but be sure to change the file paths, currently with placeholders in [brackets]!
<details>
<summary><strong>Config file</strong></summary>

```json
{
 "version": "auto-py-to-exe-configuration_v1",
 "pyinstallerOptions": [
  {
   "optionDest": "noconfirm",
   "value": true
  },
  {
   "optionDest": "filenames",
   "value": "[main.py file path]"
  },
  {
   "optionDest": "onefile",
   "value": true
  },
  {
   "optionDest": "console",
   "value": true
  },
  {
   "optionDest": "icon_file",
   "value": "[app-icon.ico file path]"
  },
  {
   "optionDest": "name",
   "value": "GSX Pro Profile Scanner"
  },
  {
   "optionDest": "contents_directory",
   "value": "profile-scanner"
  },
  {
   "optionDest": "clean_build",
   "value": true
  },
  {
   "optionDest": "strip",
   "value": false
  },
  {
   "optionDest": "noupx",
   "value": false
  },
  {
   "optionDest": "disable_windowed_traceback",
   "value": false
  },
  {
   "optionDest": "uac_admin",
   "value": false
  },
  {
   "optionDest": "uac_uiaccess",
   "value": false
  },
  {
   "optionDest": "argv_emulation",
   "value": false
  },
  {
   "optionDest": "bootloader_ignore_signals",
   "value": false
  },
  {
   "optionDest": "hiddenimports",
   "value": "rich"
  },
  {
   "optionDest": "hiddenimports",
   "value": "shellingham"
  },
  {
   "optionDest": "hiddenimports",
   "value": "click"
  },
  {
   "optionDest": "hiddenimports",
   "value": "pandas"
  },
  {
   "optionDest": "hiddenimports",
   "value": "typer"
  },
  {
   "optionDest": "hiddenimports",
   "value": "typing"
  },
  {
   "optionDest": "hiddenimports",
   "value": "pyclip"
  },
  {
   "optionDest": "hiddenimports",
   "value": "shutil"
  },
  {
   "optionDest": "hiddenimports",
   "value": "pathlib"
  },
  {
   "optionDest": "hiddenimports",
   "value": "requests"
  },
  {
   "optionDest": "hiddenimports",
   "value": "json"
  },
  {
   "optionDest": "hiddenimports",
   "value": "datetime"
  },
  {
   "optionDest": "hiddenimports",
   "value": "webbrowser"
  },
  {
   "optionDest": "hiddenimports",
   "value": "os"
  }
 ],
 "nonPyinstallerOptions": {
  "increaseRecursionLimit": true,
  "manualArguments": ""
 }
}

```

</details>

*Option 2*

Or run the pyinstaller command directly with the current configurations and just make changes to the paths/values in [brackets] and anything else that you wish to change


<details>
<summary><strong>Command</strong></summary>

```bash
pyinstaller --noconfirm --onefile --console --icon "[icon.ico file path]" --name "GSX Pro Profile Scanner v[X.X.X version number]" --contents-directory "profile-scanner" --clean --hidden-import "rich" --hidden-import "shellingham" --hidden-import "click" --hidden-import "pandas" --hidden-import "typer" --hidden-import "typing" --hidden-import "pyclip" --hidden-import "shutil" --hidden-import "pathlib" --hidden-import "requests" --hidden-import "json" --hidden-import "datetime" --hidden-import "webbrowser" --hidden-import "os"  "[main.py file location]"
```
*Note: Some values must be updated, within [brackets]*

</details>

### [2]

Create a new folder for the 'program files' where the following files should be copied:

- data folder (__must contain airports.csv__)
- actions.py
- setup.py
- utils.py
- Executable (.exe)

### [3]

Next convert this folder into a zip file

### [4]

Launch NSIS and select 'Installer based on ZIP file' provide the path to the zip file and otherwise leave everything default (inc. default folder)

### [5]

Distribute this .exe (installer) as this contains all the files needed.
