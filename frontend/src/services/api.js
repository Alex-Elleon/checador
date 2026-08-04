import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; 

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Servicio para registrar usuario enviando foto en base64 o multipart
export const registerUser = async (userData) => {
  return await api.post('/users/', userData);
};

// Servicio para autenticación / asistencia biométrica
export const verifyFace = async (imageBase64) => {
  return await api.post('/attendance/verify', { image: imageBase64 });
};