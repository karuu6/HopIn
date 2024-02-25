import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Center,
  Box,
  Heading,
  Text,
  NativeBaseProvider,
  Button,
} from "native-base";

const Trips = ({ route, navigation }) => {
  const [trips, setTrips] = useState([]);
  const [requestStatus, setRequestStatus] = useState(null);

  const {
    access,
    refresh,
    date,
    radius,
    pickupLoc,
    dropoffLoc,
    arriveBy,
    leaveBy,
  } = route.params;

  useEffect(() => {
    // Make a GET request to api/search/ endpoint

    axios
      .get("https://2009-68-234-168-22.ngrok-free.app/api/search/", {
        headers: {
          Authorization: `Bearer ${access}`,
          "Content-Type": `application/json;`,
        },
        params: {
          // Add any query parameters you need for the request
          date: date, // Replace with the actual date
          radius: radius, // Replace with the actual radius
          pickup_loc: pickupLoc, // Replace with the actual pickup location
          dropoff_loc: dropoffLoc, // Replace with the actual dropoff location
          arrive_by: arriveBy, // Replace with the actual arrive_by time
          leave_by: leaveBy, // Replace with the actual leave_by time
        },
      })
      .then((response) => {
        // Set the trips state with the data from the response
        setTrips(response.data.trips);
        console.log(response.data.trips);
      })
      .catch((error) => {
        console.error("Error fetching trips:", error);
        console.log(`Bearer ${access}`);
      });
  }, [access]); // Empty dependency array means this effect will run once on component mount

  const handleRequestTrip = (tripId) => {
    // Navigate to TripInfo component with the selected tripId
    // console.log(tripId);
    // navigation.navigate("TripInfo", { refresh, access, tripId });
    setRequestStatus("Trip Request Sent Successfully");
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
            Trips
          </Heading>
          <Box mt="5">
            {trips.map((trip) => (
              <Box key={trip.id} p="3" borderWidth={1} borderRadius="md" mb="3">
                <Text fontWeight="bold">{trip.title}</Text>
                <Text>Date: {trip.date}</Text>
                <Text>Start Time: {trip.start_time}</Text>
                <Text>End Time: {trip.end_time}</Text>
                <Text>Price: {trip.price}</Text>
                <Text>Pickup Address: {trip.pickup_location}</Text>
                <Text>Dropoff Address: {trip.dropoff_location}</Text>
                {/* Add other fields you want to display */}
                <Button
                  onPress={() => handleRequestTrip(trip.id)}
                  mt="2"
                  colorScheme="indigo"
                >
                  Request Trip
                </Button>
              </Box>
            ))}
          </Box>
          {requestStatus && (
            <Text fontSize="lg" color="green.500" mt="3">
              {requestStatus}
            </Text>
          )}
        </Box>
      </Center>
    </NativeBaseProvider>
  );
};

export default Trips;
