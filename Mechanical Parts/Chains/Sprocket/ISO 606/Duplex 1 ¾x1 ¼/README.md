# Chain Sprockets ISO606 duplex 1 3/4" x 1 1/4" from z 8 to z 40

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 1 3/4" x 1 1/4" with number of teeth ranging from z=8 to z=40.

![Image](screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
44,45|30,99|27,94|44|5|28,8|88,4|8|132|116,15|74|25|120
44,45|30,99|27,94|44|5|28,8|88,4|9|148,4|129,96|88|25|120
44,45|30,99|27,94|44|5|28,8|88,4|10|162,3|143,85|100|25|120
44,45|30,99|27,94|44|5|28,8|88,4|11|176,3|157,77|112|25|120
44,45|30,99|27,94|44|5|28,8|88,4|12|189,5|171,74|125|25|120
44,45|30,99|27,94|44|5|28,8|88,4|13|204,2|185,74|125|25|120
44,45|30,99|27,94|44|5|28,8|88,4|14|218,2|199,76|125|25|120
44,45|30,99|27,94|44|5|28,8|88,4|15|232,3|213,79|145|25|120
44,45|30,99|27,94|44|5|28,8|88,4|16|246,3|227,84|160|30|120
44,45|30,99|27,94|44|5|28,8|88,4|17|260|241,91|160|30|120
44,45|30,99|27,94|44|5|28,8|88,4|18|274|255,98|160|30|120
44,45|30,99|27,94|44|5|28,8|88,4|19|289|270,06|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|20|303|284,15|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|21|317|298,24|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|22|331|312,34|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|23|345|326,44|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|24|359|340,55|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|25|373|354,66|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|26|387|368,77|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|27|401,4|382,88|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|28|416|397|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|29|430|411,12|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|30|444|425,24|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|31|458|439,37|180|30|120
44,45|30,99|27,94|44|5|28,8|88,4|35|514|495,88|200|30|120
44,45|30,99|27,94|44|5|28,8|88,4|38|557|538,27|200|30|120
44,45|30,99|27,94|44|5|28,8|88,4|40|585|566,54|200|30|120

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex 1 ¾x1 ¼.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](https://github.com/FreeCAD/FreeCAD-library/raw/master/Mechanical%20Parts/Chains/Plate%20Wheel/ISO%20606/Simplex%201%20½%20x%201/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
