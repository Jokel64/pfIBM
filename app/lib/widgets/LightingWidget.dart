import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:sleek_circular_slider/sleek_circular_slider.dart';

class LigthingController extends StatefulWidget {

  @override
  State<StatefulWidget> createState() => _LigthingControllerState();
}

class _LigthingControllerState extends State<LigthingController> {
  static const platform = MethodChannel('samples.flutter.dev/pfibm');

  double ist_light = 25;

  double soll_light = 22;

  @override
  Widget build(BuildContext context) {
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
                        min: 0,
                        max: 100,
                        initialValue: 50,
                        onChangeEnd: (_value) async {


                          soll_light = _value;
                          final result = await platform.invokeMethod("light", <String, dynamic>{'l': soll_light*10}) as double;

                          setState((){ist_light = result;});


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
                                              'Soll: ${percentage.toStringAsFixed(0)} %',
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
                                              'Ist: ${ist_light.toString()} %',
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