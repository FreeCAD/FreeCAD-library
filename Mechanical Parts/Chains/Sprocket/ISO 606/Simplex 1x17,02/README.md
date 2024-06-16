# Chain Sprockets ISO606 simplex 1" x 17,02 from z 8 to z 114

This folder contains the 3D models of the sprockets for ISO 606 chains simplex 1" x 17,02 with number of teeth ranging from z=8 to z=114.

![Image](../images/simplex_screenshot.png "Sprocket Simplex")

The model is parametric and the values are contained in the spreadsheet `Data`.

The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/simplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt (Tooth width)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---
25,4|17,02|15,88|26|2,5|16,2|8|77|6,37|42|16|35
25,4|17,02|15,88|26|2,5|16,2|9|85|74,27|50|16|35
25,4|17,02|15,88|26|2,5|16,2|10|93|82,19|55|16|35
25,4|17,02|15,88|26|2,5|16,2|11|101,5|90,14|61|16|40
25,4|17,02|15,88|26|2,5|16,2|12|109|98,14|69|16|40
25,4|17,02|15,88|26|2,5|16,2|13|117|106,12|78|16|40
25,4|17,02|15,88|26|2,5|16,2|14|125|114,15|84|16|40
25,4|17,02|15,88|26|2,5|16,2|15|133|122,17|92|16|40
25,4|17,02|15,88|26|2,5|16,2|16|141|130,2|100|20|45
25,4|17,02|15,88|26|2,5|16,2|17|149|138,22|100|20|45
25,4|17,02|15,88|26|2,5|16,2|18|157|146,28|100|20|45
25,4|17,02|15,88|26|2,5|16,2|19|165,2|154,33|100|20|45
25,4|17,02|15,88|26|2,5|16,2|20|173,2|162,38|100|20|45
25,4|17,02|15,88|26|2,5|16,2|21|181,2|170,43|110|20|50
25,4|17,02|15,88|26|2,5|16,2|22|189,3|178,48|110|20|50
25,4|17,02|15,88|26|2,5|16,2|23|197,5|186,53|110|20|50
25,4|17,02|15,88|26|2,5|16,2|24|205,5|194,59|110|20|50
25,4|17,02|15,88|26|2,5|16,2|25|213,5|202,66|110|20|50
25,4|17,02|15,88|26|2,5|16,2|26|221,6|210,72|120|20|50
25,4|17,02|15,88|26|2,5|16,2|27|229,6|218,79|120|20|50
25,4|17,02|15,88|26|2,5|16,2|28|237,7|226,85|120|20|50
25,4|17,02|15,88|26|2,5|16,2|29|245,8|234,92|120|20|50
25,4|17,02|15,88|26|2,5|16,2|30|254|243|120|20|50
25,4|17,02|15,88|26|2,5|16,2|31|262|251,08|120|25|50
25,4|17,02|15,88|26|2,5|16,2|32|270|259,13|120|25|50
25,4|17,02|15,88|26|2,5|16,2|33|278,5|267,21|120|25|50
25,4|17,02|15,88|26|2,5|16,2|34|287|275,28|120|25|50
25,4|17,02|15,88|26|2,5|16,2|35|296,2|283,36|120|25|50
25,4|17,02|15,88|26|2,5|16,2|36|304,6|291,44|120|25|50
25,4|17,02|15,88|26|2,5|16,2|37|312,6|299,51|120|25|50
25,4|17,02|15,88|26|2,5|16,2|38|320,7|307,59|120|25|50
25,4|17,02|15,88|26|2,5|16,2|39|328,8|315,67|120|25|50
25,4|17,02|15,88|26|2,5|16,2|40|336,9|323,75|120|25|50
25,4|17,02|15,88|26|2,5|16,2|45|377,11|364,12|125|25|70
25,4|17,02|15,88|26|2,5|16,2|50|417,4|404,52|125|25|70
25,4|17,02|15,88|26|2,5|16,2|57|474|461,08|125|25|70
25,4|17,02|15,88|26|2,5|16,2|76|627|614,64|140|25|80
25,4|17,02|15,88|26|2,5|16,2|95|781,1|768,22|140|25|80
25,4|17,02|15,88|26|2,5|16,2|114|934,3|921,81|140|25|80

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI simplex 1x17,02.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png "Configuration")

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
