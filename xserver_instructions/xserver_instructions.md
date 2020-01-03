# How to use graphical applications with the Windows Subsytem for Linux

## Install an XServer application.

A very common XServer application is Xming X Server for Windows. It can be downloaded at https://sourceforge.net/projects/xming/

After downloading the Xming setup executable, run it and install Xming.

## Setting the correct display variable

Once Xming is installed, open your Ubuntu 18.04 on Windows. Enter the command `export DISPLAY=:0`.

To test if it is working, you can use a simple app like the ones found in x11-apps. Install these using `sudo apt-get install x11-apps`.

A simple app to test with is `xeyes`.
