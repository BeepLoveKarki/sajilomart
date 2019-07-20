import 'package:flutter/material.dart';


class Explore extends StatefulWidget {
  @override
  _ExploreState createState() => _ExploreState();
}

class _ExploreState extends State<Explore> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Explore the Shop",style: TextStyle(color:Colors.white),),
        centerTitle: true ,
        automaticallyImplyLeading: false,
      ),    
      body: Center(

      ),
    );
  }
}