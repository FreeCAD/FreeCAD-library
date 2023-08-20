# Chain Plate Wheels ISO606 simplex ¾ x ⁷⁄₁₆ from z 8 to z 30

This folder contains the 3D models of the plate wheels for ISO 606 chains simplex ¾x⁷⁄₁₆ with number of teeth ranging from z=8 to z=30.

![Image](screenshot.png "Plate Wheel Simplex")

The model is parametric and the values are contained in the spreadsheet `Data`.

The parameters refer to the plate wheel dimensions as in the drawing below:

![Drawing](drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt (Tooth width)|z (Number of teeth)|De (External Diameter)|Dp (Pitch diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---
19,05|11,68|12,07|19|2|11,1|8|57,3|49,78|10|11,1
19,05|11,68|12,07|19|2|11,1|9|62|55,7|10|11,1
19,05|11,68|12,07|19|2|11,1|10|69|61,64|10|11,1
19,05|11,68|12,07|19|2|11,1|11|75|67,61|12|11,1
19,05|11,68|12,07|19|2|11,1|12|81,5|73,6|14|11,1
19,05|11,68|12,07|19|2|11,1|13|87,5|79,59|14|11,1
19,05|11,68|12,07|19|2|11,1|14|93,6|85,61|14|11,1
19,05|11,68|12,07|19|2|11,1|15|99,8|91,63|14|11,1
19,05|11,68|12,07|19|2|11,1|16|105,5|97,65|14|11,1
19,05|11,68|12,07|19|2|11,1|17|111,5|103,67|14|11,1
19,05|11,68|12,07|19|2|11,1|18|118|109,71|14|11,1
19,05|11,68|12,07|19|2|11,1|19|124,2|115,75|14|11,1
19,05|11,68|12,07|19|2|11,1|20|129,7|121,78|14|11,1
19,05|11,68|12,07|19|2|11,1|21|136|127,82|16|11,1
19,05|11,68|12,07|19|2|11,1|22|141|133,86|16|11,1
19,05|11,68|12,07|19|2|11,1|23|149|139,9|16|11,1
19,05|11,68|12,07|19|2|11,1|24|153,9|145,94|16|11,1
19,05|11,68|12,07|19|2|11,1|25|160|152|16|11,1
19,05|11,68|12,07|19|2|11,1|26|165,9|158,04|16|11,1
19,05|11,68|12,07|19|2|11,1|27|172,3|164,09|16|11,1
19,05|11,68|12,07|19|2|11,1|28|178|170,13|16|11,1
19,05|11,68|12,07|19|2|11,1|29|184,1|176,19|16|11,1
19,05|11,68|12,07|19|2|11,1|30|190,5|182,25|16|11,1

The 3D model configuration of each plate wheel can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Plate Wheel simplex ¾x⁷⁄₁₆.FCStd`**.

To obtain the 3D model of the desidered plate wheel, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](configuration.png "Configuration")

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
