# TouchDesigner Hue Control
*a tox for controlling phillips hue devices*  
[matthew ragan](matthewragan.com)  
[zoe sandoval](zoesandoval.com)

## TouchDesigner Version
* 099 2018.26750

## OS Support
* Windows 10
* macOS

## Dependencies
* [phue](https://github.com/studioimaginaire/phue)

## Summary
Philips Hue smart lights are intended to be used in homes / studios. The devices come in many varieties - individual lamps, outdoor lights, LED strip lights, etc. These are synchronized by communicating with an additional device called a Bridge. A single Bridge can control up to 50 lights. There are many stand alone applications to drive Hue Lights, and this repo aims to provide some additional control by exposing those controls through TouchDesigner. In order to do this, we use the `phue` library. There is some additional set-up required in order to use an external library, though hopefully much of this is now streamlined.

This TOX provides global control for all lights, or individual control for single lights.

## Set-up
This module module has some additional requirements in the from of dependencies, as well as some set-up requirements for working with hue devices. To begin we need to ensure that we've collected all of the requisite external dependencies

### Install Python3
Ensure that you've installed a `Python 3.5+` variety.

### Installing Dependencies for Windows Users
For Window's users a convenience script is provided here:
`\dependencies\update-dep-python-windows.cmd`
In order for this to operate correctly, right click and run this `.cmd` file as an Administrator. This should first ensure that your python package manager is updated, and that your additional python modules are added to a newly created directory in your project `dependencies\python`. 

### Installing Dependencies for macOS Users
For Mac users a convenience script is provided here:
`\dependencies\update-dep-python-mac.sh`
In order for this to operate correctly, open a terminal window and drag the file above into the command line. Press return / Enter to run the bash script. This should first ensure that your python package manager is updated, and that your additional python modules are added to a newly created directory in your project `dependencies\python`. 

### Connecting to the Hue Bridge
Before being able to control lights you'll need to ensure that you can connect to your Hue Bridge. You'll need to know the IP address for your Hue Bridge. You can locate this IP address by looking at the Hue app on your phone, or by setting your Bridge to have an assigned IP on your router.

You'll need to enter the IP address of your Hue Bridge onto the component itself, and then press the large center button on the Hue Bridge. After doing this you'll need to pulse the `Set-up Individual Lights` button on the `base_hueControl` TOX.

## Parameters

### Set-up Individual Lights

### Bridge IP

### All Color

### All Brightness

### All Trans Time

### All Power

### Update All

### Update by Settings

### Light n Name

### Light n Color

### Light n Brightness

### Light n Trans Time

### Light n Power

### Update n Light

## Credits
### Inspired by the work of:
[zoe sandoval](zoesandoval.com)  
[lightnotes](https://www.lightnotes.es/)  
[forum inspiration](https://www.derivative.ca/Forum/viewtopic.php?f=4&t=6131)