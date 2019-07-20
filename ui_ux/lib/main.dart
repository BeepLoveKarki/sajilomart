import 'package:flutter/material.dart';

void main() => runApp(App());

class App extends StatelessWidget{
  @override 
  Widget build(BuildContext context){
    return MaterialApp(
      title: 'Shop App',
      theme: ThemeData(
        primarySwatch: Colors.deepOrange,
      ),
      home: LoginPage(title:'Login'),
    );
  }
}

class LoginPage extends 