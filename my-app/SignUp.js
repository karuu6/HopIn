import React from "react";

import {
  Center,
  Box,
  Heading,
  VStack,
  FormControl,
  Input,
  Link,
  Button,
  HStack,
  Text,
  NativeBaseProvider,
} from "native-base";

import axios from "axios";
import { useState, useEffect } from "react";

const SignUp = ({ navigation }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSignUp = () => {
    setErrorMessage("");
    // Make a POST request to api/signup
    axios
      .post("https://2009-68-234-168-22.ngrok-free.app/api/signup/", {
        username: username,
        password: password,
      })
      .then((response) => {
        // Handle the response, e.g., show success message or navigate to another page
        console.log("SignUp successful:", response);
        navigation.navigate("Login");
      })
      .catch((error) => {
        console.error("SignUp failed", error.response.data);
        // Handle errors, e.g., display an error message to the user
        setErrorMessage("User already exists. Please login.");
      });
  };

  return (
    <NativeBaseProvider>
      <Center w="100%">
        <Box safeArea p="2" w="90%" maxW="290" py="8">
          <Heading
            size="lg"
            color="coolGray.800"
            _dark={{
              color: "warmGray.50",
            }}
            fontWeight="semibold"
          >
            Welcome
          </Heading>
          <Heading
            mt="1"
            color="coolGray.600"
            _dark={{
              color: "warmGray.200",
            }}
            fontWeight="medium"
            size="xs"
          >
            Sign up to continue!
          </Heading>
          <VStack space={3} mt="5">
            <FormControl>
              <FormControl.Label>User Name</FormControl.Label>
              <Input onChangeText={(value) => setUsername(value)} />
            </FormControl>
            <FormControl>
              <FormControl.Label>Password</FormControl.Label>
              <Input
                type="password"
                onChangeText={(value) => setPassword(value)}
              />
            </FormControl>
            <Button mt="2" colorScheme="indigo" onPress={handleSignUp}>
              Sign up
            </Button>
            {errorMessage && (
              <Text color="red.500" mt="2">
                {errorMessage}
              </Text>
            )}
          </VStack>
        </Box>
      </Center>
    </NativeBaseProvider>
  );
};

export default SignUp;
