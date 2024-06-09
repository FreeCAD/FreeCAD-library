# Chain Sprockets ISO606 duplex 2" x 1 1/4" from z 8 to z 30

This folder contains the 3D models of the sprockets for ISO 606 chains duplex 2" x 1 1/4" with number of teeth ranging from z=8 to z=30.

![Image](../images/duplex_screenshot.png "Sprocket Duplex")

The model is parametric and the values are contained in the spreadsheet `Data`.
The parameters refer to the sprocket dimensions as in the drawing below:

![Drawing](../images/duplex_drawing.png "Drawing")

### Table of dimensions in millimeters:

P (Pitch)|Wc (Chain width)|Dr (Roller diameter)|Tr (Tooth radius)|Rw (Radius width)|Wt1 (Tooth width 1)|Wt2 (Tooth width 2)|z (Number of teeth)|De (External Diameter)|Dp (pitch diameter)|d (Hub diameter)|D (Hole diameter)|H (Total height)
---|---|---|---|---|---|---|---|---|---|---|---|---
50,8|30,99|29,21|51|6|28,8|87,4|8|153|132,69|82|30|120
50,8|30,99|29,21|51|6|28,8|87,4|9|169|148,54|88|30|120
50,8|30,99|29,21|51|6|28,8|87,4|10|185|164,44|104|30|120
50,8|30,99|29,21|51|6|28,8|87,4|11|200,8|180,34|120|30|120
50,8|30,99|29,21|51|6|28,8|87,4|12|216,8|196,29|133|30|120
50,8|30,99|29,21|51|6|28,8|87,4|13|232,8|212,29|145|30|120
50,8|30,99|29,21|51|6|28,8|87,4|14|248,8|228,29|145|30|120
50,8|30,99|29,21|51|6|28,8|87,4|15|264,8|244,3|160|30|120
50,8|30,99|29,21|51|6|28,8|87,4|16|280,9|260,4|160|30|120
50,8|30,99|29,21|51|6|28,8|87,4|17|296,9|276,4|180|30|120
50,8|30,99|29,21|51|6|28,8|87,4|18|313|292,55|180|30|120
50,8|30,99|29,21|51|6|28,8|87,4|19|329,1|308,66|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|20|345,2|324,71|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|21|361,3|340,82|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|22|377,5|356,98|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|23|393,6|373,08|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|24|409,7|389,18|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|25|425,8|405,33|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|26|441,9|421,44|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|27|458,1|437,59|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|28|474,2|453,69|200|30|120
50,8|30,99|29,21|51|6|28,8|87,4|30|506,5|486|200|30|120

The 3D model configuration of each sprocket can be dynamically retrieved using a preset `Configuration table`.
The file name of the 3D model containing the `Configuration table` is **`Sprocket ANSI duplex 2x1 ¼.FCStd`**.

To obtain the 3D model of the desidered sprocket, click the spreadsheet `Data` in the Tree View and then select the `Teeth Number` in the property editor. If nothing changes try to `Refresh` the model.

See the following image for details

![Drawing](../images/configuration.png)

### Notes for developers
If you add a row in the `Configuration table` of the `Data` spreadsheet, then add that row in the above table of this `README.md` file, without the first cell.
