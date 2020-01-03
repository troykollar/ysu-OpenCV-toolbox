# OpenCV Toolbox
Guide/Examples for OpenCV

## Installing OpenCV for Ubuntu 18.04
Open a terminal in Ubuntu 18.04. The following commands will install OpenCV.
```
sudo apt update
sudo apt upgrade
```
Then, to ensure that python is up to date, run `sudo apt install python3`.

Next you must install pip. To do this use `sudo apt install python3-pip`.

Now you will use pip to install OpenCV by typing `sudo pip3 install opencv-contrib-python`

To ensure that everything was installed correctly, we will create a script that outputs the installed version of OpenCV. Use `python3` to open the python interpreter.

Once in the python interpreter, type:
```
import cv2
cv2.__version__
```
This will output the installed version of OpenCV. The output should be: `'4.1.2'`. Type `quit()` to exit the python interpreter.
