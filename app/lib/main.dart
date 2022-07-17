import 'package:app/screens/BaseLayout.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const pfIBMApp());
}

class pfIBMApp extends StatelessWidget {
  const pfIBMApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'pfIBM',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
          primarySwatch: Colors.blue,
          primaryColor: Color(0xff867cef),
          backgroundColor: Color(0xfff0f0f0),
          disabledColor: Color(0xffededed),
          colorScheme: ColorScheme.fromSwatch(accentColor: Color(0xffaf92ea)),
          //textTheme: GoogleFonts.openSansTextTheme(),
          visualDensity: VisualDensity.adaptivePlatformDensity
      ),
      home: BaseLayout(),
    );
  }
}