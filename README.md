# Bandaged Cube Explorer
Explore and Solve every bandaged 3x3x3

## Usage
Open `start.py`

`explorer(bandage_seq, scramble, scramble_name, length, get, export)`

Input the bandaged cube's bandage to `bandage_seq` (str) using  
`X+Y to connect part X and part Y`

ex.)`"UBL+UB,UBR+UR,U+UL,UF+UFL,F+FD,FL+FDL,FR+FRD,L+LD,BL+BLD,B+BD+D,R+RB,RD+RDB"` would be [Meffert's Bandaged Cube](https://www.hknowstore.com/item.aspx?corpname=nowstore&itemid=3bf6ab3f-1234-45e2-95c0-0f140fbe2827).  
Parts are named correspond to its position, 3 faces for corners, 2 faces for edges and 1 face for centers.  
Core is named `C` and for other faces, please check out [Here](https://ruwix.com/the-rubiks-cube/algorithm/).

Put the scramble into `scramble` (str) and name the solution into `scramble_name ` (str)

Put the maximum length of solution to the `length` (int) and how many solutions to get in `get` (int).

Put the export file name to `export` (str).

Run the script on Python IDLE.
## Credits
[Kentaro Nishi](https://qiita.com/7y2n)  
[Ika no Osushi](https://twitter.com/cube_224)  
[Ladislav Dubravský](https://github.com/ladislavdubravsky)
