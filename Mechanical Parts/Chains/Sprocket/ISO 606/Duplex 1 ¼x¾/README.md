# Chain Sprockets ISO606 duplex 1 1/4" x 3/4" from z 8 to z 76

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 1 1/4" x 3/4" with number of teeth ranging from z=8 to z=76.

![Image](../images/duplex_screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/duplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
31,75|19,56|19,05|32|3,5|18,2|54,6|8|98,1|82,96|53|20|75
31,75|19,56|19,05|32|3,5|18,2|54,6|9|108|92,84|63|20|75
31,75|19,56|19,05|32|3,5|18,2|54,6|10|117,9|102,74|70|20|75
31,75|19,56|19,05|32|3,5|18,2|54,6|11|127,8|112,68|80|20|80
31,75|19,56|19,05|32|3,5|18,2|54,6|12|137,8|122,68|90|20|80
31,75|19,56|19,05|32|3,5|18,2|54,6|13|147,8|132,65|100|20|80
31,75|19,56|19,05|32|3,5|18,2|54,6|14|157,8|142,68|110|20|80
31,75|19,56|19,05|32|3,5|18,2|54,6|15|167,9|152,72|120|20|80
31,75|19,56|19,05|32|3,5|18,2|54,6|16|177,9|162,75|120|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|17|187,9|172,78|120|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|18|198|182,85|120|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|19|208,1|192,91|120|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|20|218,1|202,98|120|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|21|228,2|213,04|140|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|22|238,3|223,11|140|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|23|248,3|233,17|140|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|24|258,4|243,23|140|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|25|268,5|253,33|140|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|26|278,6|263,4|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|27|288,6|273,49|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|28|298,7|283,56|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|29|308,8|293,65|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|30|318,9|303,75|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|31|329|313,85|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|32|339,1|323,91|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|33|349,2|334,01|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|34|359,3|344,1|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|35|369,4|354,2|150|25|80
31,75|19,56|19,05|32|3,5|18,2|54,6|36|379,5|364,3|150|30|80
31,75|19,56|19,05|32|3,5|18,2|54,6|37|389,5|374,39|150|30|80
31,75|19,56|19,05|32|3,5|18,2|54,6|38|399,6|384,49|150|30|80
31,75|19,56|19,05|32|3,5|18,2|54,6|39|409,7|394,59|150|30|80
31,75|19,56|19,05|32|3,5|18,2|54,6|40|419,8|404,69|150|30|80
31,75|19,56|19,05|32|3,5|18,2|54,6|45|470,3|455,17|160|30|90
31,75|19,56|19,05|32|3,5|18,2|54,6|76|783,5|768,32|180|30|100

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex 1 ¼x¾.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
