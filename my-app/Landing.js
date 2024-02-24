import React from "react";

import {
  NativeBaseProvider,
  Box,
  Button,
  Container,
  Header,
  Content,
  Text,
  Center,
  Heading,
  VStack,
  FormControl,
  Input,
  Link,
  HStack,
} from "native-base";

import Login from "./Login";

const Landing = ({ navigation }) => {
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

          <VStack space={3} mt="5">
            <Link>
              <Button
                mt="2"
                colorScheme="indigo"
                onPress={() => navigation.navigate("Login")}
              >
                Hop-in today!
              </Button>
            </Link>
          </VStack>
        </Box>
      </Center>
    </NativeBaseProvider>
  );
};

export default Landing;
