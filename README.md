# virtualsmaenergymeter
Virtual (emulated) SMA Energy Meter

The problem with SMA Sunny Portal is that you only can choose one SMA energy meter for Supply/Consume or Solar Supply.
This usually is no problem because SMA Home manager can at least speak with all SMA solar inverters to get their values and feed it combined into sunny island.
Now what if you have a Balkonkraftwerk (=one or more additional solar inverters from other manufacturers) ? Sunny Island will be blind about them and only your house consumption will decrease.
You now can get an SMA energy meter and connect it to your extra non-SMA inverter. Then use my software to "add-in" the values of this meter to your main meter.
Another problem in your setup can be that you have several energy meters and different places and want to have the values combined.
My program simply gets the values of your "master" meter and values of your "extra" meter(s) and combines all values into a virtual/emulated energy meter.
(In the end you even don't need the extra SMA EMeter because it's all based on JSON values (which you can get from many inverters easily). 
See my other project which combines SMA speedwire inverters with Hoymiles JSON at https://github.com/Vinylrider/virtualsmainverter)

Btw, my program also handles the problem if you connected your energy meter wrong to the inverter (having supply as consume and vice versa).

Example output :<br>
<br>
<b>SMA-EM Serial:xxxxxxxx (MASTER)</b><br>
----sum----<br>
P: consume:0.0W 179655.8169kWh supply:3773.3W 123561.0353kWh<br>
S: consume:0.0VA 188958.3022kVAh supply:10004.7VA 130858.7795VAh<br>
Q: cap 9265.9var 31803.9637kvarh ind 0.0var 43213.8065kvarh<br>
cos phi:0.377Â°<br>
----L1----<br>
P: consume:0.0W 59070.5019kWh supply:1043.4W 41670.9272kWh<br>
S: consume:0.0VA 63711.8505kVAh supply:2976.1VA 44284.1413kVAh<br>
Q: cap 2787.2var 10866.5784kvarh ind 0.0var 17757.2545kvarh<br>
U: 237.057V I:12.816A cos phi:0.351Â°<br>
----L2----<br>
P: consume:0.0W 73791.4176kWh supply:807.4W 38866.2951kWh<br>
S: consume:0.0VA 77179.146kVAh supply:3209.9VA 40903.6016kVAh<br>
Q: cap 3106.7var 10126.2493kvarh ind 0.0var 17184.425kvarh<br>
U: 238.868V I:13.628A cos phi:0.252Â°<br>
----L3----<br>
P: consume:0.0W 52110.253kWh supply:1922.5W 48340.1685kWh<br>
S: consume:0.0VA 54202.9726kVAh supply:3881.5VA 50495.4517kVAh<br>
Q: cap 3372.0var 11846.9288kvarh ind 0.0var 9307.9197kvarh<br>
U: 238.243V I:16.453A cos phi:0.495Â°<br>
Version: 1.2.8.R|010208<br>
<br>
<b>SMA-EM Serial:xxxxxxx</b> (To add to to master values)<br>
----sum----<br>
P: consume:1284.9W 72.9117kWh supply:0.0W 0.0kWh<br>
S: consume:1286.5VA 77.7805kVAh supply:0.0VA 0.0VAh<br>
Q: cap 63.8var 9.5125kvarh ind 0.0var 0.0kvarh<br>
cos phi:0.999Â°<br>
----L1----<br>
P: consume:429.4W 24.4237kWh supply:0.0W 0.0kWh<br>
S: consume:429.9VA 25.963kVAh supply:0.0VA 0.0kVAh<br>
Q: cap 20.6var 3.1kvarh ind 0.0var 0.0kvarh<br>
U: 236.764V I:1.817A cos phi:0.999Â°<br>
----L2----<br>
P: consume:429.9W 24.3999kWh supply:0.0W 0.0051kWh<br>
S: consume:430.5VA 25.1318kVAh supply:0.0VA 0.9112kVAh<br>
Q: cap 22.6var 3.2557kvarh ind 0.0var 0.0kvarh<br>
U: 239.492V I:1.799A cos phi:0.999Â°<br>
----L3----<br>
P: consume:425.6W 24.1005kWh supply:0.0W 0.0073kWh<br>
S: consume:426.1VA 24.7019kVAh supply:0.0VA 1.0719kVAh<br>
Q: cap 20.6var 3.1566kvarh ind 0.0var 0.0kvarh<br>
U: 238.5V I:1.788A cos phi:0.999Â°<br>
Version: 1.2.4.R|010204<br>
<br>
<b>SMA-EM Serial:1900999999</b> (emulated SMA energy meter which combines values from two SMA energy meters)<br>
----sum----<br>
P: consume:0.0W 179655.8169kWh supply:5058.2W 123633.9467kWh<br>
S: consume:0.0VA 188958.3022kVAh supply:11291.0VA 130936.5596VAh<br>
Q: cap 9325.9var 31813.4762kvarh ind 0.0var 43213.8065kvarh<br>
cos phi:0.377Â°<br>
----L1----<br>
P: consume:0.0W 59070.5019kWh supply:1473.0W 41695.3507kWh<br>
S: consume:0.0VA 63711.8505kVAh supply:3406.2VA 44310.1041kVAh<br>
Q: cap 2787.2var 10866.5784kvarh ind 0.0var 17757.2545kvarh<br>
U: 237.057V I:14.635A cos phi:0.351Â°<br>
----L2----<br>
P: consume:0.0W 73791.4176kWh supply:1237.4W 38890.6949kWh<br>
S: consume:0.0VA 77179.146kVAh supply:3640.5VA 40928.7333kVAh<br>
Q: cap 3106.7var 10126.2493kvarh ind 0.0var 17184.425kvarh<br>
U: 238.868V I:15.427A cos phi:0.252Â°<br>
----L3----<br>
P: consume:0.0W 52110.253kWh supply:2347.8W 48364.2689kWh<br>
S: consume:0.0VA 54202.9726kVAh supply:4307.2VA 50520.1535kVAh<br>
Q: cap 3372.0var 11846.9288kvarh ind 0.0var 9307.9197kvarh<br>
U: 238.243V I:18.238A cos phi:0.495Â°<br>
Version: 1.2.4.R|010204<br>
<br>
<u>Thanks to </u>:<br>
https://github.com/datenschuft/SMA-EM : I use their "speedwiredecoder.py" for decoding and sma-em-measurement.py for testing the emulator.<br>
https://github.com/Roeland54/SMA-Energy-Meter-emulator : I use their "emeter.py" for encoding, but had to fix an UDP protocol address so it is "emeter2.py" in my rep.<br>
