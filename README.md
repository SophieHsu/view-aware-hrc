<!-- TOC -->
* [Integrating Field of View in Human-Aware Collaboration](#integrating-field-of-view-in-human-aware-collaboration)
  * [Overview](#overview)
  * [Installation Instructions](#installation-instructions)
    * [Install SteamVR](#install-steamvr)
    * [Install Oculus](#install-oculus)
    * [Set up the Repositories](#set-up-the-repositories)
  * [Usage](#usage)
    * [Running the scripts](#running-the-scripts)
    * [Runtime arguments](#runtime-arguments)
  * [Citation](#citation)
  * [Contact](#contact)
<!-- TOC -->

# Integrating Field of View in Human-Aware Collaboration #

## Overview ##

This project is organized into three repositories including this one. Briefly, the repositories are described as follows.

| **Repository**      | **Link**                                               | **Purpose**                                            |
|---------------------|--------------------------------------------------------|--------------------------------------------------------|
| `view-aware-hrc`    | [Link](https://github.com/SophieHsu/view-aware-hrc)    | Parent repo with setup and launch instructions.        |
| `3d-plan-eval`      | [Link](https://github.com/SophieHsu/3d-plan-eval)      | Repo for running the vr kitchen environment.           |
| `FOV-aware-planner` | [Link](https://github.com/SophieHsu/FOV-aware-planner) | Repo for running various planners for the robot agent. |

For a more detailed description please refer to the individual READMEs of the repositories using the provided links.

## Installation Instructions ##
<b>We highly recommend using windows to use the VR.</b> Majority of the testing for this project, especially with VR has been done in windows only.

### Install SteamVR ###
Install the SteamVR (found [here](https://store.steampowered.com/app/250820/SteamVR/)) using the steam platform.


### Install Oculus ###
- Perform the initial setup of your VR headset. For oculus/quest see [this](https://www.meta.com/blog/quest/you-got-a-quest-2-heres-how-to-set-it-up/).
- Set the VR headset to run with SteamVR. For oculus/quest see [this](https://docs.varwin.com/latest/en/instructions-for-using-the-oculus-quest-2-headset-2260861409.html).

### Set up the Repositories ###
Clone the project using: 
```
git clone --recurse-submodules git@github.com/SophieHsu/view-aware-hrc.git
or
git clone --recurse-submodules https://github.com/SophieHsu/3d-plan-eval
```

This will clone this repository along with the necessary repositories as submodules.
The `3d-plan-eval` repository will be cloned in the `vr_kitchen` directory and the `FOV-aware-planner` repository will be
cloned in the `fov-aware-planner` directory.

Next, set up the virtual environments used to run the code inside the two submodule repositories using the provided `setup_env.sh` script.
For windows:
```
.\setup_venv.ps1 # for windows
or
./setup.bash # for linux/mac
```

## Usage ##

### Running the scripts ###
Launch the planner and the VR kitchen environment using the following command.
```
python3 launch.py
```

### Runtime arguments ###
The `launch.py` file proves launch config in the `__LAUNCH_CONFIG` var which can be updated to change the 
arguments used to run the individual scripts. A brief description of the launch argument is also provided in the file.

## Citation ##
Please cite this work using the following BibTex:
```
Coming soon
```

## Contact ##
For any questions, please reach out to: [yachuanh@usc.edu](mailto:yachuanh@usc.edu)
