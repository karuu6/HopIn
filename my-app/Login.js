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

import SignUp from "./SignUp";

const Login = ({ navigation }) => {
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = () => {
    setErrorMessage("");

    axios
      .post("http://127.0.0.1:8000/api/token/", {
        username: username,
        password: password,
      })
      .then((response) => {
        // Handle the response, for example, store the token in local storage
        console.log("Token:", response.data);
        const access = response.data.access;
        const refresh = response.data.refresh;

        // You can also navigate to another page upon successful login
        navigation.navigate("Start", { access, refresh });
      })
      .catch((error) => {
        console.error("Login failed", error.response.data);
        setErrorMessage("Login failed. Check your credentials.");
      });
  };

  return (
    <NativeBaseProvider>
      <Center w="100%">
        <Box safeArea p="2" py="8" w="90%" maxW="290">
          <Heading
            size="lg"
            fontWeight="600"
            color="coolGray.800"
            _dark={{
              color: "warmGray.50",
            }}
          >
            Welcome
          </Heading>
          <Heading
            mt="1"
            _dark={{
              color: "warmGray.200",
            }}
            color="coolGray.600"
            fontWeight="medium"
            size="xs"
          >
            Sign in to continue!
          </Heading>

          <VStack space={3} mt="5">
            <FormControl>
              <FormControl.Label>Username</FormControl.Label>
              <Input onChangeText={(value) => setUsername(value)} />
            </FormControl>
            <FormControl>
              <FormControl.Label>Password</FormControl.Label>
              <Input
                onChangeText={(value) => setPassword(value)}
                type="password"
              />
              <Link
                _text={{
                  fontSize: "xs",
                  fontWeight: "500",
                  color: "indigo.500",
                }}
                alignSelf="flex-end"
                mt="1"
              >
                Forget Password?
              </Link>
            </FormControl>
            <Button mt="2" colorScheme="indigo" onPress={handleLogin}>
              Sign in
            </Button>
            {errorMessage && (
              <Text color="red.500" mt="2">
                {errorMessage}
              </Text>
            )}
            <HStack mt="6" justifyContent="center">
              <Text
                fontSize="sm"
                color="coolGray.600"
                _dark={{
                  color: "warmGray.200",
                }}
              >
                I'm a new user.{" "}
              </Text>
              <Link
                _text={{
                  color: "indigo.500",
                  fontWeight: "medium",
                  fontSize: "sm",
                }}
                onPress={() => navigation.navigate("SignUp")}
              >
                Sign Up
              </Link>
            </HStack>
          </VStack>
        </Box>
      </Center>
    </NativeBaseProvider>
  );
};

export default Login;
