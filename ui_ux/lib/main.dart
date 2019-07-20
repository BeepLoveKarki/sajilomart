import 'package:flutter/material.dart';
import 'login.dart';
// import 'camera.dart';

void main() => runApp(App());

class App extends StatelessWidget{
  @override 
  Widget build(BuildContext context){
    return MaterialApp(
      title: 'Shop App',
      theme: ThemeData(
        primarySwatch: Colors.lightBlue,
      ),
      home: LoginPage(title: 'Login'),
      // home: CapturePhoto(),
    );
  }
}
