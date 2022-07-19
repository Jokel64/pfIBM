import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:sleek_circular_slider/sleek_circular_slider.dart';

class TemperatureController extends StatefulWidget {

  @override
  State<StatefulWidget> createState() => _TemperatureControllerState();
}

class _TemperatureControllerState extends State<TemperatureController> {
  static const platform = MethodChannel('samples.flutter.dev/pfibm');

  double ist_temp = 25;
  double soll_temp = 22;

  void _startTimer() {
    // Disable the button after it has been pressed

    Timer(const Duration(seconds: 1),() async {
      final ist_temp_v = await platform.invokeMethod("temp_ist") as double;
      final soll_temp_v =  await platform.invokeMethod("temp_soll") as double;

      setState(() {
        ist_temp = ist_temp_v;
        soll_temp = soll_temp_v;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    _startTimer();
    return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                  width: Get.size.width,
                  child: Padding(
                      padding: const EdgeInsets.fromLTRB(0, 50, 0, 0),
                      child: SleekCircularSlider(
                        appearance: CircularSliderAppearance(
                          customColors: CustomSliderColors(
                            trackColor: Colors.grey,
                            dotColor: Colors.grey,
                            progressBarColor: Get.theme.primaryColor,
                          ),
                          startAngle: 130.0,
                          angleRange: 280.0,
                          size: Get.size.width * 0.6,
                          customWidths: CustomSliderWidths(
                              progressBarWidth: 5, handlerSize: 10),
                        ),
                        min: 10,
                        max: 30,
                        initialValue: soll_temp,
                        onChangeEnd: (_value) async {


                          soll_temp = _value;
                          final result = await platform.invokeMethod("temp", <String, dynamic>{'t': soll_temp}) as double;

                          setState((){ist_temp = result;});


                        },
                        innerWidget: (percentage) => Padding(
                            padding: const EdgeInsets.all(30.0),
                            child: Center(
                              child: Container(
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    shape: BoxShape.circle,
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black.withOpacity(0.1),
                                        blurRadius: 7,
                                        spreadRadius: 8,
                                      ),
                                    ],
                                  ),
                                  child: Container(
                                      margin: EdgeInsets.all(8),
                                      decoration: BoxDecoration(
                                        border: Border.all(
                                          color: Get.theme.primaryColor,
                                          width: 1,
                                        ),
                                        shape: BoxShape.circle,
                                        color: Colors.white,
                                      ),
                                      child: Column(
                                        crossAxisAlignment:
                                        CrossAxisAlignment.center,
                                        mainAxisAlignment:
                                        MainAxisAlignment.center,
                                        children: [
                                          SizedBox(
                                            height: 15,
                                          ),
                                          Center(
                                            child: Text(
                                              'Soll: ${percentage.toStringAsFixed(0)} °C',
                                              style: TextStyle(
                                                fontSize: 23,
                                                color: Colors.black,
                                                fontWeight: FontWeight.w600,
                                              ),
                                            ),
                                          ),
                                          SizedBox(
                                            height: 10,
                                          ),
                                          Center(
                                            child: Text(
                                              'Ist: ${ist_temp} °C',
                                              style: TextStyle(
                                                fontSize: 18,
                                                color: Colors.black,
                                                fontWeight: FontWeight.w600,
                                              ),
                                            ),
                                          )
                                        ],
                                      ))),
                            )),
                      )))
            ],
          )
        ]);
  }
}
