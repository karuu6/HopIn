import React from "react";
import { Center, Button, NativeBaseProvider } from "native-base";

const Start = ({ route, navigation }) => {
  const { access, refresh } = route.params;

  const continueAsHopper = () => {
    navigation.navigate("Hopper", { access, refresh });
  };

  const continueAsDriver = () => {
    navigation.navigate("Driver", { access, refresh });
  };

  return (
    <NativeBaseProvider>
      <Center w="100%">
        <Button onPress={continueAsHopper} mt="4">
          Continue as Hopper
        </Button>
        <Button onPress={continueAsDriver} mt="4">
          Continue as Driver
        </Button>
      </Center>
    </NativeBaseProvider>
  );
};

export default Start;
