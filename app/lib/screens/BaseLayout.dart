import 'package:app/screens/HomeScreen.dart';
import 'package:flutter/material.dart';

class BaseLayout extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _BaseLayoutState();
}

class _BaseLayoutState extends State<BaseLayout> {
  int _index = 0;

  void _setIndex(int i) {
    setState(() {
      _index = i;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Scaffold(
      body: IndexedStack(
        index: _index,
        children: [
          [
            HomeScreen(),
            HomeScreen(),
            HomeScreen()
          ][_index]],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _index,
        onTap: _setIndex,
        selectedLabelStyle: TextStyle(fontSize: 1),
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: ''),
          BottomNavigationBarItem(icon: Icon(Icons.verified_user), label: ''),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: '')
        ],
      ),
    ));
  }
}
