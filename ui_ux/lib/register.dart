import 'dart:io';
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:ui_ux/login.dart';

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  File _image;
  TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20.0);
  String profileURL = "assets/avatar.png";

  Future getImage() async {
    var image = await ImagePicker.pickImage(source: ImageSource.gallery);

    setState(() {
      _image = image;
    });
  }

  @override
  Widget build(BuildContext context) {
    final usernameField = TextField(
      obscureText: false,
      style: style,
      decoration: InputDecoration(
              contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
              hintText: "User Name",
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      ),
    );

    final passwordField = TextField( 
      obscureText: true,
      style: style,
      decoration: InputDecoration( 
        contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        hintText: "Password",
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      )
    );

    final confirmpasswordField = TextField( 
      obscureText: true,
      style: style,
      decoration: InputDecoration( 
        // contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        hintText: "Confirm Password",
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      )
    );

    Widget avatar(){
      if(_image == null)
        return Image.asset(
          profileURL,
          fit: BoxFit.contain,
        );
      else
        return Image.file(_image);
    }

    final registerButton = Material(
      elevation: 5.0,
      borderRadius: BorderRadius.circular(30.0),
      color: Color(0xff01A0C7),
      child: MaterialButton(
        minWidth: MediaQuery.of(context).size.width,
        padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        onPressed: () {
          Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(builder: (context) => LoginPage()),
            (Route<dynamic> route) => false,
          );
        },
        child: Text("Register",
            textAlign: TextAlign.center,
            style: style.copyWith(
                color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );

    return Scaffold(
      appBar: AppBar(
        title: Text("Register Page",style: TextStyle(color:Colors.white),),
        centerTitle: true ,
        automaticallyImplyLeading: false,
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Padding( 
            padding:const EdgeInsets.all(36.0),
            child: Column(  
              children: <Widget>[
                GestureDetector(
                  child: ClipOval(
                    child: Container(width:150,height:200,child:avatar()),
                  ),
                  onTap: (){
                    getImage();
                  },
                ),
              
                SizedBox(height: 15.0),
                usernameField,
                SizedBox(height: 15.0),
                passwordField,
                SizedBox(height: 15.0),
                confirmpasswordField,
                SizedBox(height: 15.0),
                registerButton
              ],
            ),
          ),
        )
      ),
    );
  }
}

