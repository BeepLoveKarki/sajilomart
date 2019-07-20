import 'package:flutter/material.dart';

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {

  int balance = 10000;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Home Page",style: TextStyle(color:Colors.white),),
        centerTitle: true ,
        automaticallyImplyLeading: false,
      ),
    );
  }
}