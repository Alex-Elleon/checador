import axios from 'axios';

const API_URL = 'http://192.168.1.16:8000'; 

export const api = axios.create({
  baseURL: API_URL,
});

// Registrar usuario enviando el FormData
export const registerUser = async (formData) => {
  return await api.post('/users/register', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Servicio para autenticación / asistencia biométrica
export const verifyFace = async (imageBase64) => {
  return await api.post('/attendance/verify', { image: imageBase64 });
};

export const markAttendance = async (formData) => {
  const response = await fetch(`${API_URL}/checks/mark`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al procesar la asistencia');
  }

  return await response.json();
};