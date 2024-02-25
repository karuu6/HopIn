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
import { useEffect, useState } from "react";

const Hopper = ({ route, navigation }) => {
  const { access, refresh } = route.params;

  const [date, setDate] = useState("");
  const [radius, setRadius] = useState("");
  const [pickupLoc, setPickupLoc] = useState("");
  const [dropoffLoc, setDropoffLoc] = useState("");
  const [arriveBy, setArriveBy] = useState("");
  const [leaveBy, setLeaveBy] = useState("");

  const handleSearchTrips = () => {
    // Navigate to Trips component with chosen parameters
    navigation.navigate("Trips", {
      access,
      refresh,
      date,
      radius,
      pickupLoc,
      dropoffLoc,
      arriveBy,
      leaveBy,
    });
  };

  // useEffect(() => {
  //   // Make a POST request to api/token/refresh/
  //   axios
  //     .post("http://127.0.0.1:8000/api/token/refresh/", {
  //       refresh: refresh,
  //     })
  //     .then((response) => {
  //       // Update the state with the new access token
  //       setNewAccessToken(response.data.access);
  //     })
  //     .catch((error) => {
  //       console.error("Error refreshing token:", error.response.data);
  //       // Handle errors, e.g., redirect to login if refresh fails
  //       navigation.navigate("Login");
  //     });
  // }, [refresh, navigation]);

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

        {/* <Text>Access Token: {access}</Text>
        <Text>New Access Token: {newAccessToken}</Text> */}
        {/* ... rest of your UI */}

        <Box mt="5">
          <Input
            placeholder="Date"
            value={date}
            onChangeText={(value) => setDate(value)}
          />
          <Input
            placeholder="Radius"
            value={radius}
            onChangeText={(value) => setRadius(value)}
          />
          <Input
            placeholder="Pickup Location"
            value={pickupLoc}
            onChangeText={(value) => setPickupLoc(value)}
          />
          <Input
            placeholder="Dropoff Location"
            value={dropoffLoc}
            onChangeText={(value) => setDropoffLoc(value)}
          />
          <Input
            placeholder="Arrive By"
            value={arriveBy}
            onChangeText={(value) => setArriveBy(value)}
          />
          <Input
            placeholder="Leave By"
            value={leaveBy}
            onChangeText={(value) => setLeaveBy(value)}
          />
          <Button mt="2" colorScheme="indigo" onPress={handleSearchTrips}>
            Search Trips
          </Button>
        </Box>

        <Button
          onPress={() => navigation.navigate("Trips", { access, refresh })}
        ></Button>
      </Center>
    </NativeBaseProvider>
  );
};

export default Hopper;
