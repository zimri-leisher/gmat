------------------------------------------------------
OpenFramesInterface plugin for GMAT

Copyright (c) 2022 Emergent Space Technologies, Inc.
http://gitlab.com/EmergentSpaceTechnologies/OpenFramesInterface/wikis/home

Developed under multiple NASA SBIR Contracts (listed below),
and subject to all applicable SBIR data and usage rights.
 - NNX15CG32P
 - NNX16CG16C
 - 80NSSC18P0728
 - 80NSSC18P1457
 - 80NSSC19C0044
------------------------------------------------------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this software except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

------------------------------------------------------
Dependencies and Licenses

This plugin has the following Open Source software (OSS) dependencies. License terms
and source code are available at the listed websites. All OSS dependencies are 
dynamically linked to this plugin, and are used in unmodified form by this plugin.

- OpenFrames: Apache Version 2.0 license
    Software: http://sourceforge.net/projects/openframes
    License : http://github.com/ravidavi/OpenFrames/blob/VR/LICENSE.txt

- OpenSceneGraph: wxWindows Version 3.1 license
    Software: http://www.openscenegraph.org
    License : http://github.com/openscenegraph/OpenSceneGraph/blob/master/LICENSE.txt
    
- osgEarth: LGPL Version 3 license
    Software: http://osgearth.org/
    License : https://github.com/gwaldron/osgearth/blob/master/LICENSE.txt

- wxWidgets: wxWindows Version 3.1 license
    Software: http://www.wxwidgets.org
    License : http://www.wxwidgets.org/about/licence

- OpenVR: BSD 3-clause license
    Software: http://github.com/ValveSoftware/openvr
    License : http://github.com/ValveSoftware/openvr/blob/master/LICENSE

------------------------------------------------------
Instructions for building with GMAT

Detiled instructions on building the OpenFramesInterface with GMAT are available at the OpenFramesInterface Wiki, available at https://gitlab.com/EmergentSpaceTechnologies/OpenFramesInterface/wikis/home . The instructions here are simplified, and assume you have already set up GMAT's build system using CMake.

1: Open CMake-GUI for GMAT
2: Modify the GMAT_ADDITIONAL_PLUGINS variable
   - Select the full path to the "OpenFramesInterface_AdditionalPlugin.txt" file contained next to this README
3: Press "Configure"
4: Enable the "PLUGIN_OPENFRAMESINTERFACE" option
5: Press "Configure" again
   - NOTE: All OpenFramesInterface dependencies will be downloaded and built. THIS WILL TAKE A WHILE!
6: When the configuration is complete, press "Generate"

Now you can build GMAT in the standard way (Visual Studio or makefiles). See GMAT documentation for more info.