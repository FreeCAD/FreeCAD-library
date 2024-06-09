# Chain Sprockets ISO606 duplex 1 1/2" x 1" from z 8 to z 40

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 1 1/2" x 1" with number of teeth ranging from z=8 to z=40.

![Image](../images/duplex_screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/duplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
38,1|25,4|25,4|38|4|23,6|72|8|115|99,55|58|25|95
38,1|25,4|25,4|38|4|23,6|72|9|126,4|111,4|70|25|95
38,1|25,4|25,4|38|4|23,6|72|10|138|123,29|80|25|95
38,1|25,4|25,4|38|4|23,6|72|11|150|135,21|90|25|100
38,1|25,4|25,4|38|4|23,6|72|12|162|147,22|102|25|100
38,1|25,4|25,4|38|4|23,6|72|13|174,2|159,18|114|25|100
38,1|25,4|25,4|38|4|23,6|72|14|186,2|171,22|128|25|100
38,1|25,4|25,4|38|4|23,6|72|15|198,2|183,26|140|25|100
38,1|25,4|25,4|38|4|23,6|72|16|210,3|195,3|140|25|100
38,1|25,4|25,4|38|4|23,6|72|17|222,3|207,34|150|25|100
38,1|25,4|25,4|38|4|23,6|72|18|234,3|219,42|160|25|100
38,1|25,4|25,4|38|4|23,6|72|19|246,5|231,49|160|25|100
38,1|25,4|25,4|38|4|23,6|72|20|258,6|243,57|160|25|100
38,1|25,4|25,4|38|4|23,6|72|21|270,6|255,65|160|25|100
38,1|25,4|25,4|38|4|23,6|72|22|282,7|267,73|160|25|100
38,1|25,4|25,4|38|4|23,6|72|23|294,8|279,8|160|25|100
38,1|25,4|25,4|38|4|23,6|72|24|306,8|291,88|160|25|100
38,1|25,4|25,4|38|4|23,6|72|25|319|304|160|25|100
38,1|25,4|25,4|38|4|23,6|72|26|331|316,08|160|30|100
38,1|25,4|25,4|38|4|23,6|72|27|343,2|328,19|160|30|100
38,1|25,4|25,4|38|4|23,6|72|28|355,2|340,27|160|30|100
38,1|25,4|25,4|38|4|23,6|72|29|367,3|352,38|160|30|100
38,1|25,4|25,4|38|4|23,6|72|30|379,5|364,5|160|30|100
38,1|25,4|25,4|38|4|23,6|72|31|391,6|376,62|170|30|100
38,1|25,4|25,4|38|4|23,6|72|32|403,7|388,69|170|30|100
38,1|25,4|25,4|38|4|23,6|72|33|415,8|400,81|170|30|100
38,1|25,4|25,4|38|4|23,6|72|34|427,8|412,93|170|30|100
38,1|25,4|25,4|38|4|23,6|72|35|440|425,04|170|30|100
38,1|25,4|25,4|38|4|23,6|72|36|452|437,16|170|30|100
38,1|25,4|25,4|38|4|23,6|72|37|464,2|449,27|170|30|100
38,1|25,4|25,4|38|4|23,6|72|38|476,2|461,39|170|30|100
38,1|25,4|25,4|38|4|23,6|72|39|488,5|473,5|170|30|100
38,1|25,4|25,4|38|4|23,6|72|40|500,6|485,62|170|30|100

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex 1 ½x1.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
