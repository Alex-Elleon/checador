import React, { useState, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, Image, Alert, ScrollView, Platform } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { markAttendance } from '../../services/api';

export default function CheckInScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [employNumber, setEmployNumber] = useState('');
  const [photoUri, setPhotoUri] = useState(null);
  const [loading, setLoading] = useState(false);
  const cameraRef = useRef(null);

  const isWeb = Platform.OS === 'web';

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({ quality: 0.8 });
        setPhotoUri(photo.uri);
      } catch (error) {
        Alert.alert('Error', 'No se pudo tomar la foto.');
      }
    }
  };

  const handleCheckIn = async () => {
    if (!employNumber) {
      Alert.alert('Error', 'Por favor ingresa tu número de empleado.');
      return;
    }
    if (!photoUri) {
      Alert.alert('Error', 'Debes capturar tu rostro para verificar tu asistencia.');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('employ_number', employNumber);

      const cleanUri = Platform.OS === 'ios' ? photoUri.replace('file://', '') : photoUri;
      formData.append('file', {
        uri: cleanUri,
        name: `check_${employNumber}.jpg`,
        type: 'image/jpeg',
      });

      const response = await markAttendance(formData);
      Alert.alert('¡Asistencia Marcada!', response.message);

      setPhotoUri(null);
      setEmployNumber('');
    } catch (error) {
      Alert.alert('Error de Validación', error.message || 'No se pudo registrar la asistencia.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={{ padding: 16, flex: 1, backgroundColor: '#fff' }}>
      <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 16, textAlign: 'center' }}>
        Checador Biométrico
      </Text>

      <TextInput
        placeholder="Número de Empleado"
        value={employNumber}
        onChangeText={setEmployNumber}
        style={{ borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 16 }}
      />

      <View style={{ height: 280, width: '100%', borderRadius: 8, overflow: 'hidden', marginBottom: 16, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' }}>
        {photoUri ? (
          <Image source={{ uri: photoUri }} style={{ width: '100%', height: '100%' }} />
        ) : permission?.granted ? (
          <CameraView ref={cameraRef} style={{ width: '100%', height: '100%' }} facing="front" />
        ) : (
          <TouchableOpacity onPress={requestPermission} style={{ backgroundColor: '#2563eb', padding: 12, borderRadius: 8 }}>
            <Text style={{ color: '#fff' }}>Conceder Permiso de Cámara</Text>
          </TouchableOpacity>
        )}
      </View>

      {!isWeb && (
        <TouchableOpacity
          onPress={photoUri ? () => setPhotoUri(null) : takePicture}
          style={{ backgroundColor: photoUri ? '#d97706' : '#059669', padding: 12, borderRadius: 8, marginBottom: 12 }}
        >
          <Text style={{ color: '#fff', textAlign: 'center', fontWeight: 'bold' }}>
            {photoUri ? 'Volver a Tomar Foto' : 'Capturar Rostro'}
          </Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity
        onPress={handleCheckIn}
        disabled={loading}
        style={{ backgroundColor: loading ? '#93c5fd' : '#2563eb', padding: 16, borderRadius: 8, marginTop: 8, marginBottom: 32 }}
      >
        <Text style={{ color: '#fff', textAlign: 'center', fontWeight: 'bold', fontSize: 16 }}>
          {loading ? 'Verificando Rostro...' : 'Marcar Asistencia'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}