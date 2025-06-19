# Dirtbreaker
A (not-so) little project involving a remote controlled car, a 3d printed turret, and a raspberry pi.

# Hello Lurker!

You should probably not expect me to know more than you. I am merely a highschooler trying to get some linux experience (I use arch btw) and some embedded stuff. Support is unlikely, but if you have any questions, feel free to ask. I will explain to the best of my ability.

Oh also, the fbtft-overlay thing was pretty cool. I had to decompile fbtft, add overrides for more SPI busses (ones that support DMA and only exist on later models of raspi such as 4 and 5) and recompile! That took me a long time to figure out. Hopefully this helps someone eventually who wants to have multiple fbtft screens despite all the cons.

#Specs Of Hardware

The turret is 3d printed and modeled by my friend, so it might not be uploaded. Maybe I'll ask him later. I doubt this will gain traction, though. Anyways, there are 2 RPI4 4GBs. I am using 3 HiLetGo 320x240 SPI displays. For cameras, I am using a c270 logitech, a (i think) RPI camera module v2.1, and a lepton 3.1r with a purethermal mini pro. I got the no connector variety because it was on sale for 25 dollars, and it still is by time of writing on groupgets. Sidenote: I kind of regret buying the 3.1r. To be honest, I think the lepton 3.5 might just be better for this, because it will have a higher range given its lower FOV. Regardless, if you're planning on doing this project, I suggest a 3.1r if you want to not have to edit my code, or just nab a lepton 3.5 if you want to do some tinkering with my stuff. As a sidenote, unless someone asks me to, I am not planning on making a support guide for a complete newbie. I am, however, open to anyone asking. I do have summer credit advancement so I might not be able to answer quickly. Also, as previously stated, you likely know more than me. 

Back to the main topic. I am using 2 NEMA 17 200 step stepper motors driven with TB6600 stepper motor drivers. I am using a 11.1v LiPo airsoft battery. Right now, I do not have it, so I am instead using a lab powersupply that emulates it.
