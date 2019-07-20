import 'package:flutter/material.dart';
import 'login.dart';

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Home Page",
          style: TextStyle(color: Colors.white),
        ),
        centerTitle: true,
        automaticallyImplyLeading: false,
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            children: <Widget>[
              Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Image.asset(
                    "assets/avatar.png",
                    width: 120.0,
                    height: 150.0,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Text(
                    "User Name",
                    style: TextStyle(
                      fontFamily: 'Montserrat',
                      fontSize: 28.0,
                    ),
                  ),
                ),
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: Text(
                  "Email Address",
                  style: TextStyle(
                    fontFamily: 'Montserrat',
                    fontSize: 28.0,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: Text(
                  "Balance\t\t100000",
                  style: TextStyle(
                    fontFamily: 'Montserrat',
                    fontSize: 28.0,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        label: Text('Logout', style: TextStyle(fontSize: 20.0, fontFamily: 'Montserrat'),),
        onPressed: () {
          Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(builder: (context) => LoginPage()),
            (Route<dynamic> route) => false,
          );
        },
        foregroundColor: Colors.white,
        // icon: Icon(Icons.get_app),
        shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(20.0))),
      ),
    );
  }
}
