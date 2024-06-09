# Chain Plate Wheels ISO606 simplex ½ x ⅛ from z 8 to z 50

This folder contains the 3D models of the plate wheels for ISO 606 chains simplex ½ x ⅛ with number of teeth ranging from z=8 to z=50.

![Image](../images/simplex_screenshot.png "Plate Wheel Simplex")

The model is parametric and the values are contained in the spreadsheet `Data`.

The parameters refer to the plate wheel dimensions as in the drawing below:

![Drawing](../images/simplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt (Tooth width)|z (Number of teeth)|De (External Diameter)|Dp (Pitch diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---
12,7|3,3|7,75|13|1|3|8|37,2|33,18|8|4
12,7|3,3|7,75|13|1|3|9|41,5|37,13|8|4
12,7|3,3|7,75|13|1|3|10|46,2|41,1|8|4
12,7|3,3|7,75|13|1|3|11|49,6|45,07|8|4
12,7|3,3|7,75|13|1|3|12|53,9|49,07|8|4
12,7|3,3|7,75|13|1|3|13|58,4|53,06|8|4
12,7|3,3|7,75|13|1|3|14|62,8|57,07|8|4
12,7|3,3|7,75|13|1|3|15|66,8|61,09|8|4
12,7|3,3|7,75|13|1|3|16|70,9|65,1|8|4
12,7|3,3|7,75|13|1|3|17|74,9|69,11|8|4
12,7|3,3|7,75|13|1|3|18|78,9|73,14|8|4
12,7|3,3|7,75|13|1|3|19|82,9|77,16|8|4
12,7|3,3|7,75|13|1|3|20|86,9|81,19|8|4
12,7|3,3|7,75|13|1|3|21|91|85,22|8|4
12,7|3,3|7,75|13|1|3|22|95|89,24|10|4
12,7|3,3|7,75|13|1|3|23|99|93,27|10|4
12,7|3,3|7,75|13|1|3|24|103|97,29|10|4
12,7|3,3|7,75|13|1|3|25|107,1|101,33|10|4
12,7|3,3|7,75|13|1|3|26|111,2|105,36|12|4
12,7|3,3|7,75|13|1|3|27|115,4|109,4|12|4
12,7|3,3|7,75|13|1|3|28|119,4|113,42|12|4
12,7|3,3|7,75|13|1|3|29|123,4|117,46|12|4
12,7|3,3|7,75|13|1|3|30|127,5|121,5|12|4
12,7|3,3|7,75|13|1|3|31|131,5|125,54|12|4
12,7|3,3|7,75|13|1|3|32|135,5|129,56|12|4
12,7|3,3|7,75|13|1|3|33|139,6|133,6|12|4
12,7|3,3|7,75|13|1|3|34|143,6|137,64|12|4
12,7|3,3|7,75|13|1|3|35|147,6|141,68|12|4
12,7|3,3|7,75|13|1|3|36|151,7|145,72|16|4
12,7|3,3|7,75|13|1|3|37|155,7|149,76|16|4
12,7|3,3|7,75|13|1|3|38|159,8|153,8|16|4
12,7|3,3|7,75|13|1|3|39|163,8|157,83|16|4
12,7|3,3|7,75|13|1|3|40|167,8|161,87|16|4
12,7|3,3|7,75|13|1|3|41|171,4|165,91|16|4
12,7|3,3|7,75|13|1|3|42|175,4|169,95|16|4
12,7|3,3|7,75|13|1|3|43|179,5|173,99|16|4
12,7|3,3|7,75|13|1|3|44|183,5|178,03|16|4
12,7|3,3|7,75|13|1|3|45|187,5|182,07|16|4
12,7|3,3|7,75|13|1|3|46|191,6|186,1|20|4
12,7|3,3|7,75|13|1|3|47|195,6|190,14|20|4
12,7|3,3|7,75|13|1|3|48|199,7|194,18|20|4
12,7|3,3|7,75|13|1|3|49|203,7|198,22|20|4
12,7|3,3|7,75|13|1|3|50|207,8|202,26|20|4

The 3D model configuration of each plate wheel can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Plate Wheel simplex ½x⅛.FCStd`**.

To obtain the 3D model of the desidered plate wheel, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png "Configuration")

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
