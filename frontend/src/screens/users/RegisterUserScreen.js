import React, { useState, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, Image, Alert, ScrollView, Platform } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { registerUser } from '../../services/api';

export default function RegisterUserScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [employNumber, setEmployNumber] = useState('');
  const [name, setName] = useState('');
  const [lastnames, setLastnames] = useState('');
  const [genre, setGenre] = useState('');
  const [occupation, setOccupation] = useState('');
  const [photoUri, setPhotoUri] = useState(null);
  const [loading, setLoading] = useState(false);
  const cameraRef = useRef(null);

  const isWeb = Platform.OS === 'web';

  const takePicture = async () => {
    if (isWeb) {
      Alert.alert('Aviso', 'Para capturar foto directamente con la cámara, usa la app desde tu celular con Expo Go.');
      return;
    }

    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({ quality: 0.8 });
        setPhotoUri(photo.uri);
      } catch (error) {
        Alert.alert('Error', 'No se pudo capturar la foto de la cámara.');
      }
    }
  };

  const handleRegister = async () => {
    if (!employNumber || !name || !lastnames) {
      Alert.alert('Error', 'Por favor completa el número de empleado, nombre y apellidos.');
      return;
    }

    if (!photoUri) {
      Alert.alert('Error', 'Debes capturar una foto del rostro obligatoriamente para registrar al usuario.');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('employ_number', employNumber);
      formData.append('name', name);
      formData.append('lastnames', lastnames);
      if (genre) formData.append('genre', genre);
      if (occupation) formData.append('occupation', occupation);

      const cleanUri = Platform.OS === 'ios' ? photoUri.replace('file://', '') : photoUri;
      formData.append('file', {
        uri: cleanUri,
        name: `${employNumber}.jpg`,
        type: 'image/jpeg',
      });

      await registerUser(formData);
      Alert.alert('¡Éxito!', 'Usuario y patrón facial registrados correctamente.');

      setPhotoUri(null);
      setEmployNumber('');
      setName('');
      setLastnames('');
      setGenre('');
      setOccupation('');
    } catch (error) {
      console.error(error?.response?.data || error);
      Alert.alert('Error', error?.response?.data?.detail || 'No se pudo conectar con el servidor.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView className="flex-1 p-4 bg-white" style={{ padding: 16 }}>
      <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 16, textAlign: 'center' }}>
        Registro de Empleado
      </Text>

      <TextInput placeholder="Número de Empleado" value={employNumber} onChangeText={setEmployNumber} style={{ borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 12 }} />
      <TextInput placeholder="Nombre" value={name} onChangeText={setName} style={{ borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 12 }} />
      <TextInput placeholder="Apellidos" value={lastnames} onChangeText={setLastnames} style={{ borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 12 }} />
      <TextInput placeholder="Género" value={genre} onChangeText={setGenre} style={{ borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 12 }} />
      <TextInput placeholder="Ocupación" value={occupation} onChangeText={setOccupation} style={{ borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 8, marginBottom: 12 }} />

      <View style={{ height: 250, width: '100%', borderRadius: 8, overflow: 'hidden', marginVertical: 12, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' }}>
        {photoUri ? (
          <Image source={{ uri: photoUri }} style={{ width: '100%', height: '100%' }} />
        ) : isWeb ? (
          <Text style={{ color: '#fff', textAlign: 'center', padding: 16 }}>
            Vista previa de cámara activa en dispositivos móviles (Expo Go)
          </Text>
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
            {photoUri ? 'Volver a Tomar Foto' : 'Capturar Foto Rostro'}
          </Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity 
        onPress={handleRegister} 
        disabled={loading}
        style={{ backgroundColor: loading ? '#93c5fd' : '#2563eb', padding: 16, borderRadius: 8, marginTop: 12, marginBottom: 32 }}
      >
        <Text style={{ color: '#fff', textAlign: 'center', fontWeight: 'bold', fontSize: 16 }}>
          {loading ? 'Registrando...' : 'Registrar Usuario'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}