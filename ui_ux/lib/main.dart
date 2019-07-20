import 'package:flutter/material.dart';

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
    );
  }
}

class LoginPage extends StatefulWidget {
  LoginPage({Key key, this.title}) : super(key: key);
  final String title;
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20.0);
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
        hintText: "Email ID",
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      )
    );

    final registerButton = Material(
      elevation: 5.0,
      borderRadius: BorderRadius.circular(30.0),
      color: Color(0xff01A0C7),
      child: MaterialButton(
        minWidth: MediaQuery.of(context).size.width,
        padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        onPressed: () {
          Navigator.push(
            context, 
            MaterialPageRoute(builder: (context) => RegisterPage()),
          );
        },
        child: Text("Sign Up",
            textAlign: TextAlign.center,
            style: style.copyWith(
                color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );

    final loginButon = Material(
      elevation: 5.0,
      borderRadius: BorderRadius.circular(30.0),
      color: Color(0xff01A0C7),
      child: MaterialButton(
        minWidth: MediaQuery.of(context).size.width,
        padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        onPressed: () {},
        child: Text("Sign In",
            textAlign: TextAlign.center,
            style: style.copyWith(
                color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );

    return Scaffold(
      appBar: AppBar(
        title: Text("Login Page",style: TextStyle(color:Colors.white),),
        centerTitle: true ,
      ),
      body: Center( 
        child: SingleChildScrollView(
            child: Padding( 
            // color: Colors.white, 
              padding:const EdgeInsets.all(36.0),
              child: Column( 
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  SizedBox(
                    height: 155.0,
                    child: Image.asset(
                      "assets/logo.png",
                      fit: BoxFit.contain,
                    ),
                  ),
                  SizedBox(height: 45.0),
                  usernameField,
                  SizedBox(height: 25.0),
                  passwordField,
                  SizedBox(
                    height: 35.0,
                  ),
                  loginButon,
                  SizedBox(
                    height: 25.0,
                  ),
                  registerButton,
                ],
              )
            )
          )
        )
    );
  }
}

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20.0);
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

    final emailField = TextField( 
      obscureText: false,
      style: style,
      decoration: InputDecoration( 
        contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        hintText: "Email ID",
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      )
    );

    final addressField = TextField( 
      obscureText: false,
      style: style,
      decoration: InputDecoration( 
        contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        hintText: "Address",
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      )
    );

    final phoneField = TextField( 
      obscureText: false,
      style: style,
      decoration: InputDecoration( 
        contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        hintText: "Phone Number",
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))
      )
    );

    

    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Padding( 
            padding:const EdgeInsets.all(36.0),
            child: Column(
              children: <Widget>[
                SizedBox(height: 25.0),
                usernameField,
                SizedBox(height: 25.0),
                emailField,
                SizedBox(height: 25.0),
                addressField,
                SizedBox(height: 25.0),
                phoneField,
                SizedBox(height: 25.0),
                passwordField,
                SizedBox(height: 25.0),
                confirmpasswordField
              ],
            ),
          )
        ),
      )
    );
  }
}