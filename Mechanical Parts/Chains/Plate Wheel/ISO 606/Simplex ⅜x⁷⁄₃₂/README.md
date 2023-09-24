# Chain Plate Wheels ISO606 simplex ⅜ x ⁷⁄₃₂ from z 8 to z 50

This folder contains the 3D models of the plate wheels for ISO 606 chains simplex ⅜ x ⁷⁄₃₂ with number of teeth ranging from z=8 to z=50.

![Image](screenshot.png "Plate Wheel Simplex")

The model is parametric and the values are contained in the spreadsheet `Data`.

The parameters refer to the plate wheel dimensions as in the drawing below:

![Drawing](drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt (Tooth width)|z (Number of teeth)|De (External Diameter)|Dp (Pitch diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---
9,525|5,72|6,35|10|1|5,3|8|28|24,89|6|5,3
9,525|5,72|6,35|10|1|5,3|9|31|27,85|8|5,3
9,525|5,72|6,35|10|1|5,3|10|34|30,82|8|5,3
9,525|5,72|6,35|10|1|5,3|11|37|33,8|8|5,3
9,525|5,72|6,35|10|1|5,3|12|40|36,8|8|5,3
9,525|5,72|6,35|10|1|5,3|13|43|39,79|8|5,3
9,525|5,72|6,35|10|1|5,3|14|46,3|42,8|8|5,3
9,525|5,72|6,35|10|1|5,3|15|49,3|45,81|8|5,3
9,525|5,72|6,35|10|1|5,3|16|52,3|48,82|10|5,3
9,525|5,72|6,35|10|1|5,3|17|55,3|51,83|10|5,3
9,525|5,72|6,35|10|1|5,3|18|58,3|54,85|10|5,3
9,525|5,72|6,35|10|1|5,3|19|61,3|57,87|10|5,3
9,525|5,72|6,35|10|1|5,3|20|64,3|60,89|10|5,3
9,525|5,72|6,35|10|1|5,3|21|68|63,91|10|5,3
9,525|5,72|6,35|10|1|5,3|22|71|66,93|10|5,3
9,525|5,72|6,35|10|1|5,3|23|73,5|69,95|10|5,3
9,525|5,72|6,35|10|1|5,3|24|77|72,97|10|5,3
9,525|5,72|6,35|10|1|5,3|25|80|76,02|10|5,3
9,525|5,72|6,35|10|1|5,3|26|83|79,02|10|5,3
9,525|5,72|6,35|10|1|5,3|27|86|82,02|10|5,3
9,525|5,72|6,35|10|1|5,3|28|89|85,07|10|5,3
9,525|5,72|6,35|10|1|5,3|29|92|88,09|10|5,3
9,525|5,72|6,35|10|1|5,3|30|94,7|91,12|10|5,3
9,525|5,72|6,35|10|1|5,3|31|98,3|94,15|12|5,3
9,525|5,72|6,35|10|1|5,3|32|101,3|97,17|12|5,3
9,525|5,72|6,35|10|1|5,3|33|104,3|100,2|12|5,3
9,525|5,72|6,35|10|1|5,3|34|107,3|103,23|12|5,3
9,525|5,72|6,35|10|1|5,3|35|110,4|106,26|12|5,3
9,525|5,72|6,35|10|1|5,3|36|113,4|109,29|12|5,3
9,525|5,72|6,35|10|1|5,3|37|116,4|112,32|12|5,3
9,525|5,72|6,35|10|1|5,3|38|119,5|115,35|12|5,3
9,525|5,72|6,35|10|1|5,3|39|122,5|118,37|12|5,3
9,525|5,72|6,35|10|1|5,3|40|125,5|121,4|12|5,3
9,525|5,72|6,35|10|1|5,3|41|128,5|124,43|16|5,3
9,525|5,72|6,35|10|1|5,3|42|131,6|127,46|16|5,3
9,525|5,72|6,35|10|1|5,3|43|134,6|130,49|16|5,3
9,525|5,72|6,35|10|1|5,3|44|137,6|133,52|16|5,3
9,525|5,72|6,35|10|1|5,3|45|140,7|136,55|16|5,3
9,525|5,72|6,35|10|1|5,3|46|143,7|139,58|16|5,3
9,525|5,72|6,35|10|1|5,3|47|146,7|142,61|16|5,3
9,525|5,72|6,35|10|1|5,3|48|149,7|145,64|16|5,3
9,525|5,72|6,35|10|1|5,3|49|152,7|148,66|16|5,3
9,525|5,72|6,35|10|1|5,3|50|155,7|151,69|16|5,3

The 3D model configuration of each plate wheel can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Plate Wheel simplex ⅜x⁷⁄₃₂.FCStd`**.

To obtain the 3D model of the desidered plate wheel, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](configuration.png "Configuration")

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
