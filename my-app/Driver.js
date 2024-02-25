import React, { useState } from "react";
import {
  Center,
  Box,
  Heading,
  VStack,
  FormControl,
  Input,
  Button,
  NativeBaseProvider,
} from "native-base";
import axios from "axios";

const Driver = ({ route, navigation }) => {
  const { access, refresh } = route.params;

  const [formData, setFormData] = useState({
    date: "",
    start_time: "",
    end_time: "",
    pickup_location: "",
    dropoff_location: "",
    dropoffLatitude: "",
    dropoffLongitude: "",
    open_seats: "",
    price: "",
  });

  const handleInputChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handlePostTrip = () => {
    // Make a POST request to api/driver/trip/ endpoint with formData
    const headers = {
      Authorization: `Bearer ${access}`,
      "Content-Type": "application/json",
    };

    axios
      .post(
        "https://2009-68-234-168-22.ngrok-free.app/api/post_trip/",
        formData,
        { headers }
      )
      .then((response) => {
        console.log("Trip posted successfully:", response.data);
        // Handle success, e.g., navigate to a confirmation page
      })
      .catch((error) => {
        console.error("Error posting trip:", error);
        // Handle error, e.g., display an error message to the user
      });
  };

  return (
    <NativeBaseProvider>
      <Center w="100%">
        <Box safeArea p="2" w="90%" maxW="290" py="8">
          <Heading size="lg" color="coolGray.800" fontWeight="semibold">
            Post Trip
          </Heading>
          <VStack space={3} mt="5">
            <FormControl>
              <FormControl.Label>Date</FormControl.Label>
              <Input
                placeholder="YYYY-MM-DD"
                value={formData.date}
                onChangeText={(value) => handleInputChange("date", value)}
              />
            </FormControl>
            <FormControl>
              <FormControl.Label>Start Time</FormControl.Label>
              <Input
                placeholder="HH:mm AM/PM"
                value={formData.start_time}
                onChangeText={(value) => handleInputChange("start_time", value)}
              />
            </FormControl>
            <FormControl>
              <FormControl.Label>End Time</FormControl.Label>
              <Input
                placeholder="HH:mm AM/PM"
                value={formData.end_time}
                onChangeText={(value) => handleInputChange("end_time", value)}
              />
            </FormControl>
            <FormControl>
              <FormControl.Label>Pickup Location</FormControl.Label>
              <Input
                placeholder="Pickup Location"
                value={formData.pickup_location}
                onChangeText={(value) =>
                  handleInputChange("pickup_location", value)
                }
              />
            </FormControl>
            <FormControl>
              <FormControl.Label>Dropoff Location</FormControl.Label>
              <Input
                placeholder="Dropoff Location"
                value={formData.dropoff_location}
                onChangeText={(value) =>
                  handleInputChange("dropoff_location", value)
                }
              />
            </FormControl>
            <FormControl>
              <FormControl.Label>Open Seats</FormControl.Label>
              <Input
                placeholder="Open Seats"
                value={formData.open_seats}
                onChangeText={(value) => handleInputChange("open_seats", value)}
              />
            </FormControl>
            <FormControl>
              <FormControl.Label>Price</FormControl.Label>
              <Input
                placeholder="Price"
                value={formData.price}
                onChangeText={(value) => handleInputChange("price", value)}
              />
            </FormControl>
            {/* Add other form controls for each field */}
            <Button onPress={handlePostTrip} mt="2" colorScheme="indigo">
              Post Trip
            </Button>
          </VStack>
        </Box>
      </Center>
    </NativeBaseProvider>
  );
};

export default Driver;
