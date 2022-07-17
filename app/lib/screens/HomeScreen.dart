import 'package:app/widgets/CustomButtons.dart';
import 'package:app/widgets/TemperatureWidget.dart';
import 'package:flutter/material.dart';

import '../constants.dart';

class HomeScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

   String room = "A4.356";
   String username = "Steve";
   String humidity = "10%";
   String temprature = "22°C";

   int active_page = 1;

   bool inLightsScreen = true;

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Scaffold(
      body: Column(
        children: [
          Stack(
            children: [
              GradientContainer(size),
              Positioned(
                  top: size.width * 0.15,
                  left: 30,
                  child: Column(
                    crossAxisAlignment:  CrossAxisAlignment.start,
                    children: [
                      Text(
                          'Good Morning, $username',
                          style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 26
                          )),


                            ],
                  )),
              Positioned(
                  top: size.width * 0.25,
                  left: 30,
                  child: Column(
                    crossAxisAlignment:  CrossAxisAlignment.start,
                    children: [
                      Text(
                          "You are in room $room",
                          style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.normal,
                              fontSize: 20
                          ))
                    ],
                  ),
              ), Positioned(
                top: size.width * 0.4,
                left: 30,
                child: Column(
                  crossAxisAlignment:  CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                            width: size.width * 0.12,
                            height: size.width * 0.12,
                            decoration: const BoxDecoration(
                              color: Colors.lightGreen,
                              shape: BoxShape.circle,
                            ),
                            child: Icon(Icons.thermostat_outlined,color: Colors.white, size: 30,)
                        ),
                        SizedBox(width: 5),

                        Text(
                            "Temperature $temprature",
                            style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.normal,
                                fontSize: 15
                            )),
                        SizedBox(width: 20,),
                        Container(
                        width: size.width * 0.12,
                        height: size.width * 0.12,
                        decoration: const BoxDecoration(
                          color: Colors.lightBlueAccent,
                          shape: BoxShape.circle,
                        ),
                        child: Icon(Icons.water_drop_outlined,color: Colors.white, size: 30,)
                      ),
                        SizedBox(width: 5),

                        Text(
                            "Humidity $humidity",
                            style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.normal,
                                fontSize: 15
                            ))
                      ],
                    )

                  ],
                ),
              )
            ],
          ),
          Stack(
            children: [
              Column(
                children: [
                  Container(
                    width: size.width,
                    height: size.height*0.56,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: const [
                            Padding(padding: EdgeInsets.all(10),
                            child: Text(
                                "Room Controls",
                                style: TextStyle(
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 17
                                )),)

                          ],
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                                SizedBox(width: 10),
                                HomeButton(image: "assets/lights.png", text: "Lights", isSelected: active_page == 0, onTap: (){setState((){active_page = 0;});}),
                                SizedBox(width: 10),
                                HomeButton(image: "assets/hvac.png", text: "Climate", isSelected: active_page == 1, onTap: (){setState((){active_page = 1;});}),
                                SizedBox(width: 10),
                                HomeButton(image: "assets/blinds.png", text: "Blinds", isSelected: active_page == 2, onTap: (){setState((){active_page = 2;});}),
                                SizedBox(width: 10),
                          ],
                        ),
                        Row(
                          children: [
                            Column(
                              children: [ TemeratureController(),]
                            )

                          ],
                        )
                      ],
                    ),
                  )
                ],
              )
            ],
          )
        ],
      ),
    );
  }
}

Container GradientContainer(Size size) {
  return Container(
    height: size.height * .3,
    width: size.width,
    decoration: const BoxDecoration(
        borderRadius: BorderRadius.only(
            bottomLeft: Radius.circular(30),
            bottomRight: Radius.circular(30)),
        image: DecorationImage(
            image: AssetImage('assets/office.jpg'), fit: BoxFit.cover)
    ),
    child: Container(
      decoration: BoxDecoration(
          borderRadius: const BorderRadius.only(
              bottomLeft: Radius.circular(30),
              bottomRight: Radius.circular(30)),
          gradient: LinearGradient(colors: [
            Color(0xFF48c9e2).withOpacity(0.9),
            Color(0xFF5593f8).withOpacity(0.9)
          ])),
    ),
  );
}
