import 'package:app/constants.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class HomeButton extends StatelessWidget {
  const HomeButton({
    Key? key,
    required this.image,
    required this.text,
    required this.isSelected,
    required this.onTap,
    this.fontSize = 18,
    this.unSelectedImageColor,
  }) : super(key: key);
  final String image;
  final String text;
  final bool isSelected;
  final VoidCallback onTap;
  final Color? unSelectedImageColor;
  final double fontSize;

  @override
  Widget build(BuildContext context) {
    return Expanded(
        child: GestureDetector(
            onTap: onTap,
            child: Container(
              width: 20,
              height: 100,
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(15),
                  color: isSelected ? Colors.lightBlueAccent.withOpacity(0.5) : Colors.grey,
                  boxShadow: [BoxShadow(
                    color: Colors.grey,
                    blurRadius: 10,
                  )]
              ),

              child: Column(
                children: [
                  SizedBox(
                    height: 4,
                  ),
                  Expanded(
                      child: Center(
                          child: Container(
                    width: Get.width / 7,
                    height: Get.height / 10,
                    child: Image.asset(
                      image,
                      color: Colors.white,
                    ),
                  ))),
                  Text(
                    text,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: fontSize,
                    ),
                  ),
                  SizedBox(height: 3,)
                ],
              ),
            )));
  }
}
