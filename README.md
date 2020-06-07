# treegame

Treegame is a shameless copy of the board game [Photosynthesis](https://blueorangegames.eu/pf/photosynthesis/), Currently with very minimal graphics...

Dependencies are:
* [pygame](https://github.com/pygame/): The game is made with pygame
* [hexy](https://github.com/RedFT/Hexy): Hexy is a module that implements the hexagonal coordainate system the game utilizes.

Dependencies can be installed with pip or conda (I prefer the former). I've managed to get it running both on Windows and Linux.

The treegame/scripts/ folder contains python scripts to run the game

* locally:  treegame_local
* online: treegame_network
* server: treegame_server

Provided that you want an online version of the game, you currently have to make sure that there's a server running. The 'treegame_server' script also provided in the scripts folder runs a server, which the clients can connect to. (some kind of lobby is planned, but currently i'm quite busy with other stuff... ).
For now, feel free to contact me so we can get this running. I've already played a couple of rounds online with friends. 

### DISCLAIMER
There is some bugs which are known, and probably lots of bugs yet to be found. Check the issues section for known bugs and report new bugs therein. 




