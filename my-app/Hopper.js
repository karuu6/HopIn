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

const Hopper = () => {
  return (
    <NativeBaseProvider>
      <Center w="100%">
        <Heading
          size="lg"
          fontWeight="600"
          color="coolGray.800"
          _dark={{
            color: "warmGray.50",
          }}
        >
          Welcome Hopper!
        </Heading>
      </Center>
    </NativeBaseProvider>
  );
};

export default Hopper;
