# Chain Sprockets ISO606 duplex 1" x 17,02mm from z 8 to z 95

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 1" x 17,02mm with number of teeth ranging from z=8 to z=95.

![Image](../images/duplex_screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/duplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
25,4|17,02|15,88|26|2,5|15,8|47,7|8|77|66,37|42|16|65
25,4|17,02|15,88|26|2,5|15,8|47,7|9|85|74,27|50|16|65
25,4|17,02|15,88|26|2,5|15,8|47,7|10|93|82,19|56|16|65
25,4|17,02|15,88|26|2,5|15,8|47,7|11|101,5|90,14|64|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|12|109|98,14|72|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|13|117|106,12|80|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|14|125|114,15|88|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|15|133|122,17|96|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|16|141|130,2|104|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|17|149|138,22|112|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|18|157|146,28|120|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|19|165,2|154,33|128|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|20|173,2|162,38|130|20|70
25,4|17,02|15,88|26|2,5|15,8|47,7|21|181,2|170,43|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|22|189,3|178,48|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|23|197,5|186,53|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|24|205,5|194,59|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|25|213,5|202,66|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|26|221,6|210,72|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|27|229,6|218,79|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|28|237,7|226,85|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|29|245,8|234,92|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|30|254|243|130|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|31|262|251,08|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|32|270|259,13|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|33|278,5|267,21|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|34|287|275,28|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|35|296,2|283,36|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|36|304,6|291,44|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|37|312,6|299,51|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|38|320,7|307,59|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|39|328,8|315,67|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|40|336,9|323,75|140|25|70
25,4|17,02|15,88|26|2,5|15,8|47,7|45|377|364,12|150|25|80
25,4|17,02|15,88|26|2,5|15,8|47,7|50|417,4|404,52|150|25|80
25,4|17,02|15,88|26|2,5|15,8|47,7|57|474|461,08|160|25|90
25,4|17,02|15,88|26|2,5|15,8|47,7|76|627|614,64|160|25|90
25,4|17,02|15,88|26|2,5|15,8|47,7|95|781,1|768,22|160|25|116

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex 1x17.02.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
