import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import axios from "axios";
import React, { useState, useEffect } from "react";
import Landing from "./Landing";
import Login from "./Login";
import SignUp from "./SignUp";
import Hopper from "./Hopper";
// import { BrowserRouter, Routes, Route } from "react-router-dom";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { Button, NativeBaseProvider } from "native-base";

const Stack = createNativeStackNavigator();

export default function App() {
  const [message, setMessage] = useState("");

  // useEffect(() => {
  //   axios
  //     .get("http://127.0.0.1:8000")

  //     .then((response) => {
  //       setMessage(response.data);
  //     })

  //     .catch((error) => {
  //       console.log(error);
  //     });
  // }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Landing">
        <Stack.Screen name="Landing" component={Landing} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="SignUp" component={SignUp} />
        <Stack.Screen name="Hopper" component={Hopper} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
