# Chain Sprockets ISO606 duplex 3/8" x 7/32" from z 8 to z 114

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 3/8" x 7/32" with number of teeth ranging from z=8 to z=114.

![Image](../images/duplex_screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/duplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
9,525|5,72|6,35|10|1|5,2|15,4|8|28|24,89|15|8|22
9,525|5,72|6,35|10|1|5,2|15,4|9|31|27,85|18|8|22
9,525|5,72|6,35|10|1|5,2|15,4|10|34|30,82|20|8|22
9,525|5,72|6,35|10|1|5,2|15,4|11|37|33,8|22|10|25
9,525|5,72|6,35|10|1|5,2|15,4|12|40|36,8|25|10|25
9,525|5,72|6,35|10|1|5,2|15,4|13|43|39,79|28|10|25
9,525|5,72|6,35|10|1|5,2|15,4|14|46,3|42,8|31|10|25
9,525|5,72|6,35|10|1|5,2|15,4|15|49,3|45,81|34|10|25
9,525|5,72|6,35|10|1|5,2|15,4|16|52,3|48,82|37|12|30
9,525|5,72|6,35|10|1|5,2|15,4|17|55,3|51,83|40|12|30
9,525|5,72|6,35|10|1|5,2|15,4|18|58,3|54,85|43|12|30
9,525|5,72|6,35|10|1|5,2|15,4|19|61,3|57,87|46|12|30
9,525|5,72|6,35|10|1|5,2|15,4|20|64,3|60,89|49|12|30
9,525|5,72|6,35|10|1|5,2|15,4|21|68|63,91|52|12|30
9,525|5,72|6,35|10|1|5,2|15,4|22|71|66,93|55|12|30
9,525|5,72|6,35|10|1|5,2|15,4|23|73,5|69,95|58|12|30
9,525|5,72|6,35|10|1|5,2|15,4|24|77|72,97|61|12|30
9,525|5,72|6,35|10|1|5,2|15,4|25|80|76,02|64|12|30
9,525|5,72|6,35|10|1|5,2|15,4|26|83|79,02|67|12|30
9,525|5,72|6,35|10|1|5,2|15,4|27|86|82,02|70|12|30
9,525|5,72|6,35|10|1|5,2|15,4|28|89|85,07|73|12|30
9,525|5,72|6,35|10|1|5,2|15,4|29|92|88,09|76|12|30
9,525|5,72|6,35|10|1|5,2|15,4|30|94,7|91,12|79|12|30
9,525|5,72|6,35|10|1|5,2|15,4|31|98,3|94,15|80|16|30
9,525|5,72|6,35|10|1|5,2|15,4|32|101,3|97,17|80|16|30
9,525|5,72|6,35|10|1|5,2|15,4|33|104,3|100,2|80|16|30
9,525|5,72|6,35|10|1|5,2|15,4|34|107,3|103,23|80|16|30
9,525|5,72|6,35|10|1|5,2|15,4|35|110,4|106,26|80|16|30
9,525|5,72|6,35|10|1|5,2|15,4|36|113,4|109,29|90|16|30
9,525|5,72|6,35|10|1|5,2|15,4|37|116,4|112,32|90|16|30
9,525|5,72|6,35|10|1|5,2|15,4|38|119,5|115,35|90|16|30
9,525|5,72|6,35|10|1|5,2|15,4|39|122,5|118,37|90|16|30
9,525|5,72|6,35|10|1|5,2|15,4|40|125,5|121,4|90|16|30
9,525|5,72|6,35|10|1|5,2|15,4|45|140,7|136,55|90|16|40
9,525|5,72|6,35|10|1|5,2|15,4|50|155,7|151,69|90|16|40
9,525|5,72|6,35|10|1|5,2|15,4|57|176,9|172,91|90|16|40
9,525|5,72|6,35|10|1|5,2|15,4|76|234,9|230,49|90|16|40
9,525|5,72|6,35|10|1|5,2|15,4|95|292,5|288,08|90|16|40
9,525|5,72|6,35|10|1|5,2|15,4|114|349,5|345,68|90|16|40

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex ⅜x⁷⁄₃₂.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
