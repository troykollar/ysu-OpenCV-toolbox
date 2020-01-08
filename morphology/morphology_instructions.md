# Morphology

There are several examples of morhpological transformations in the [OpenCV Docs](https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html).

For these examples, kerel is a 5x5 matrix of ones created using `np.ones()`

The first is erosion. It "erodes" away the boundaries of an object (works best on white objects). This can be used to reduce small bits of white noise in photos.

`erosionImg = cv2.erode(baseImg, kernel)`

The next is dilation. It is the opposite of erosion. It will increase the white region of an image. It is generally used after erosion, since erosion removes the noise, but also shrinks the image, dilation would grow the image back to size without reintroducing the white noise.

`dilationImg = cv2.dilate(baseImg, kernel)`

As explained above, erosion is usually followed by dilation. So OpenCV provides a function to perform erosion followed by dilation, it is opening and would be used like:

`openingImg = cv2.morphologyEx(baseImg, cv2.MORPH_OPEN, kernel)`

Closing is the opposite of opening. While opening is useful for reducing noise, opening is useful for "closing" small holes in the image.

`closingImg = cv2.morphologyEx(baseImg, cv2.MORPH_CLOSE, kernel)`

A morphological gradient is the difference between the dilation and erosion of an image. It will look like the outline of the image.

`morphGradient = cv2.morphologyEx(baseImg, cv2.MORPH_GRADIENT, kernel)`

A top hat is the difference between the input image and the opening of the same image. Top-hat transforms are used for various image processing tasks such as feature extraction, background equalization, image enhancement, and others.

`tophat = cv2.morphologyEx(baseImg, cv2.MORPH_TOPHAT, kernel)`

A black hat is the difference between the input image and the closing of that image. Black hat tranforms are often used enhance dark objects of interest in a bright background.

`blackhat = cv2.morphologyEx(baseImg, cv2.MORPH_BLACKHAT, kernel)`

