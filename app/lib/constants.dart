import 'dart:ui';
import 'package:flutter/material.dart' show Alignment, LinearGradient;

var secondaryColor = Color(0xFF5593f8);
var primaryColor = Color(0xFF48c9e2);

final fancyButtonGradient = LinearGradient(
  colors: [
    primaryColor,
    secondaryColor,
  ],
  begin: Alignment.topRight,
  end: Alignment.bottomLeft,
);