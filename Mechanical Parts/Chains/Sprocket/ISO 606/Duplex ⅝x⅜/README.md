# Chain Sprockets ISO606 duplex 5/8" x 3/8" from z 8 to z 95

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 5/8" x 3/8" with number of teeth ranging from z=8 to z=114.

![Image](../images/duplex_screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/duplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
15,875|9,65|10,16|16|1,6|9|25,5|8|47|41,48|25|12|40
15,875|9,65|10,16|16|1,6|9|25,5|9|52,6|46,42|30|12|40
15,875|9,65|10,16|16|1,6|9|25,5|10|57,5|51,37|35|12|40
15,875|9,65|10,16|16|1,6|9|25,5|11|63|56,34|39|14|40
15,875|9,65|10,16|16|1,6|9|25,5|12|68|61,34|44|14|40
15,875|9,65|10,16|16|1,6|9|25,5|13|73|66,32|49|14|40
15,875|9,65|10,16|16|1,6|9|25,5|14|78|71,34|54|14|40
15,875|9,65|10,16|16|1,6|9|25,5|15|83|76,36|59|14|40
15,875|9,65|10,16|16|1,6|9|25,5|16|88|81,37|64|16|45
15,875|9,65|10,16|16|1,6|9|25,5|17|93|86,39|69|16|45
15,875|9,65|10,16|16|1,6|9|25,5|18|98,3|91,42|74|16|45
15,875|9,65|10,16|16|1,6|9|25,5|19|103,3|96,45|79|16|45
15,875|9,65|10,16|16|1,6|9|25,5|20|108,4|101,49|84|16|45
15,875|9,65|10,16|16|1,6|9|25,5|21|113,4|106,52|85|16|45
15,875|9,65|10,16|16|1,6|9|25,5|22|118|111,55|90|16|45
15,875|9,65|10,16|16|1,6|9|25,5|23|123,5|116,58|95|16|45
15,875|9,65|10,16|16|1,6|9|25,5|24|128,3|121,62|100|16|45
15,875|9,65|10,16|16|1,6|9|25,5|25|134|126,66|105|16|45
15,875|9,65|10,16|16|1,6|9|25,5|26|139|131,7|110|20|45
15,875|9,65|10,16|16|1,6|9|25,5|27|144|136,75|110|20|45
15,875|9,65|10,16|16|1,6|9|25,5|28|148,7|141,78|115|20|45
15,875|9,65|10,16|16|1,6|9|25,5|29|153,8|146,83|115|20|45
15,875|9,65|10,16|16|1,6|9|25,5|30|158,8|151,87|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|31|163,9|156,92|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|32|168,9|161,95|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|33|174,5|167|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|34|179|172,05|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|35|184,1|177,1|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|36|189,1|182,15|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|37|194,2|187,2|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|38|199,2|192,24|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|39|204,2|197,29|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|40|209,3|202,34|120|20|45
15,875|9,65|10,16|16|1,6|9|25,5|45|235|227,58|120|20|50
15,875|9,65|10,16|16|1,6|9|25,5|50|260,3|252,82|120|20|50
15,875|9,65|10,16|16|1,6|9|25,5|57|296|288,18|130|20|50
15,875|9,65|10,16|16|1,6|9|25,5|76|392,1|384,15|130|20|63
15,875|9,65|10,16|16|1,6|9|25,5|95|488,5|480,14|130|20|63

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex ⅝x⅜.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
