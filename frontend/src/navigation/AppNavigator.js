import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import RegisterUserScreen from '../screens/users/RegisterUserScreen';
import CheckInScreen from '../screens/attendance/CheckInScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <Stack.Navigator initialRouteName="CheckIn">
      <Stack.Screen 
        name="CheckIn" 
        component={CheckInScreen} 
        options={{ title: 'Checador Biométrico' }}
      />
      <Stack.Screen 
        name="RegisterUser" 
        component={RegisterUserScreen} 
        options={{ title: 'Registro de Empleado' }}
      />
    </Stack.Navigator>
  );
}