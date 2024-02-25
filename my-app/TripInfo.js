import React, { useEffect } from "react";
import axios from "axios";
import { Center, Text, NativeBaseProvider } from "native-base";

const TripInfo = ({ route, navigation }) => {
  const { refresh, access, trip_id } = route.params;

  useEffect(() => {
    // Make a POST request to post_hopper_request

    axios
      .post(
        "https://2009-68-234-168-22.ngrok-free.app/api/post_hopper_request/",
        {
          trip_id: trip_id,
        },
        {
          headers: {
            Authorization: `Bearer ${access}`,
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        console.log("Hopper request posted successfully:", response.data);
        // Handle success, e.g., navigate to a confirmation page
      })
      .catch((error) => {
        console.error("Error posting hopper request:", error);
        // Handle error, e.g., display an error message to the user
      });
  });

  return (
    <NativeBaseProvider>
      <Center w="100%">
        <Text fontSize="xl" fontWeight="bold" mt="8">
          Posting Hopper Request...
        </Text>
      </Center>
    </NativeBaseProvider>
  );
};

export default TripInfo;
