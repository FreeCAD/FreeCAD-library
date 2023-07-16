# Chain Plate Wheels ISO606 simplex ½ x⁵⁄₁₆ from z 8 to z 30

This folder contains the 3D models of the plate wheels for ISO 606 chains simplex ½ x ⁵⁄₁₆ with number of teeth ranging from z=8 to z=30.

![Image](screenshot.png "Plate Wheel Simplex")

The model is parametric and the values are contained in the spreadsheet `Data`.

The parameters refer to the plate wheel dimensions as in the drawing below:

![Drawing](drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt (Tooth width)|z (Number of teeth)|De (External Diameter)|Dp (Pitch diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---
12,7|7,75|8,51|13|1,3|7,2|8|37|33,18|8|7,2
12,7|7,75|8,51|13|1,3|7,2|9|41|37,13|8|7,2
12,7|7,75|8,51|13|1,3|7,2|10|45,2|41,1|8|7,2
12,7|7,75|8,51|13|1,3|7,2|11|48,7|45,07|10|7,2
12,7|7,75|8,51|13|1,3|7,2|12|53|49,07|10|7,2
12,7|7,75|8,51|13|1,3|7,2|13|57,4|53,06|10|7,2
12,7|7,75|8,51|13|1,3|7,2|14|61,8|57,07|10|7,2
12,7|7,75|8,51|13|1,3|7,2|15|65,5|61,09|10|7,2
12,7|7,75|8,51|13|1,3|7,2|16|69,5|65,1|10|7,2
12,7|7,75|8,51|13|1,3|7,2|17|73,6|69,11|10|7,2
12,7|7,75|8,51|13|1,3|7,2|18|77,8|73,14|10|7,2
12,7|7,75|8,51|13|1,3|7,2|19|81,7|77,16|10|7,2
12,7|7,75|8,51|13|1,3|7,2|20|85,8|81,19|10|7,2
12,7|7,75|8,51|13|1,3|7,2|21|89,7|85,22|12|7,2
12,7|7,75|8,51|13|1,3|7,2|22|93,8|89,24|12|7,2
12,7|7,75|8,51|13|1,3|7,2|23|98,2|93,27|12|7,2
12,7|7,75|8,51|13|1,3|7,2|24|101,8|97,29|12|7,2
12,7|7,75|8,51|13|1,3|7,2|25|105,8|101,33|12|7,2
12,7|7,75|8,51|13|1,3|7,2|26|110|105,36|16|7,2
12,7|7,75|8,51|13|1,3|7,2|27|114|109,4|16|7,2
12,7|7,75|8,51|13|1,3|7,2|28|118|113,42|16|7,2
12,7|7,75|8,51|13|1,3|7,2|29|122|117,46|16|7,2
12,7|7,75|8,51|13|1,3|7,2|30|126,1|121,5|16|7,2

The 3D model configuration of each plate wheel can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Plate Wheel simplex ½x⁵⁄₁₆.FCStd`**.

To obtain the 3D model of the desidered plate wheel, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](configuration.png "Configuration")

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
