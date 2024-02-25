import React, { useState, useEffect } from "react";
import { FlatList } from "react-native";
import { Box, Text, Button, Center, NativeBaseProvider, Image } from "native-base";

const PendingTripRequests = ({ route, navigation }) => {
  const { access } = route.params;
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    // Fetch the current trips for the driver
    fetch("http://127.0.0.1:8000/api/current_trips_for_driver/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${access}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Extract trip ids
        const tripIds = data.past_trips.map((trip) => trip.id);
        // For each trip ID, fetch the current hopper requests
        tripIds.forEach((tripId) => {
          fetch(`http://127.0.0.1:8000/api/current_hopper_requests/${tripId}/`, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${access}`,
            },
          })
            .then((response) => response.json())
            .then((data) => {
              // Add the hopper requests to the state, appending to any existing requests
              setRequests((prevRequests) => [...prevRequests, ...data.hopper_requests]);
            })
            .catch((error) => console.error(error));
        });
      })
      .catch((error) => console.error(error));
  }, [access]);

  const acceptRequest = (index) => {
    const updatedRequests = requests.map((item, idx) => {
        if (idx === index) {
          return { ...item, isAccepted: true };
        }
        return item;
      });
      setRequests(updatedRequests);
  };

  const declineRequest = (hopperRequestId) => {
    fetch(`http://127.0.0.1:8000/api/decline_hopper_request/${hopperRequestId}/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${access}`,
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      if (response.ok) {
        alert("Request declined successfully");
        // Optionally, refresh the list of requests here
      } else {
        alert("Failed to decline the request");
      }
    })
    .catch((error) => console.error(error));
  };

  return (
    <NativeBaseProvider>
      <Center flex={1} px="3">
      <FlatList
          data={requests}
          renderItem={({ item, index }) => (
            <Box borderWidth="1" borderRadius="md" p="5" mb="2" bg="white">
              <Image
                source={{ uri: "https://s3media.247sports.com/Uploads/Assets/548/529/9529548.jpg" }}
                alt="Profile Pic"
                size="md"
                borderRadius={100}
                alignSelf="center"
                mb="3"
              />
              <Text fontSize="md" bold>
                Hopper Request ID: {item.id} {/* Assuming 'item.id' is the request ID */}
              </Text>
              <Text fontSize="sm">Trip ID: {item.trip_id}</Text>
              {item.isAccepted ? (
                <Text color="green.500" fontSize="md" bold mt="3">
                  Success!
                </Text>
              ) : (
                <>
                  <Button 
                    onPress={() => acceptRequest(index)} 
                    mt="3" 
                    colorScheme="success"
                    _text={{ color: "white" }}>
                    Accept
                  </Button>
                  <Button 
                    onPress={() => declineRequest(item.id)} 
                    mt="2" 
                    colorScheme="danger"
                    _text={{ color: "white" }}>
                    Decline
                  </Button>
                </>
              )}
            </Box>
          )}
          keyExtractor={(item, index) => index.toString()}
        />
      </Center>
    </NativeBaseProvider>
  );
};

export default PendingTripRequests;
