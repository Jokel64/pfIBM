# Room Node
In oder to start a room node use ``docker-compose build`` to build all images and ``docker-compose up --force-recreate``
to run the room node. Both commands need to be executed if changes have been done.


Raum State:
	- Klima
		- Ist Temperatur		-> Const Val. / Temp. Sensor
		- Soll Temperatur		-> UE	/ Other States	-> Goal State
		- User_allow_Cooling	-> UE
		- User_allow_heating    -> UE
	- Lighting
		- In_Room_lux_soll	-> UE -> Goal State
		- In_Room_lux_ist		-> Function / Sensor
		- Outside_lux		-> Internet API
		- Lamps			-> Function / Sensor
		- Rolershutter		-> const. val
		- User rs preference 	-> UE

	- UE States
		- (EnvironmentalAwareness -> UE -> Goal State)
		- OccupantMotionStatus	-> UE
		- Work_start		-> UE
		- Work_end			-> UE
		- Calendar			-> UE


	-RommOccupationState

	-Enrgy Efficency -> UE