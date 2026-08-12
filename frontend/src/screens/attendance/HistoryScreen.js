import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, RefreshControl, TextInput, TouchableOpacity, Alert, Modal } from 'react-native';

export default function HistoryScreen() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState('');
  const [filterState, setFilterState] = useState('TODOS');

  // Estados para el Modal
  const [modalVisible, setModalVisible] = useState(false);
  const [empNumber, setEmpNumber] = useState('');
  const [reason, setReason] = useState('');

  const API_URL = 'http://192.168.1.16:8000/checks/history';
  const REQUEST_LEAVE_URL = 'http://192.168.1.16:8000/checks/request-leave';
  const MARK_LATE_URL = 'http://192.168.1.16:8000/checks/mark-late';

  const fetchHistory = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error('Error al obtener historial:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchHistory();
  };

  const handleSendLeave = async () => {
    if (!empNumber || !reason) {
      Alert.alert("Error", "Por favor completa todos los campos.");
      return;
    }

    try {
      const details = new URLSearchParams();
      details.append('employ_number', empNumber.trim());
      details.append('reason', reason.trim());

      const response = await fetch(REQUEST_LEAVE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: details.toString(),
      });

      const data = await response.json();

      if (response.ok) {
        Alert.alert("Éxito", data.message || "Permiso registrado correctamente.");
        setModalVisible(false);
        setEmpNumber('');
        setReason('');
        fetchHistory();
      } else {
        Alert.alert("Error", data.detail || "No se pudo registrar el permiso.");
      }
    } catch (error) {
      console.error(error);
      Alert.alert("Error de red", "No se pudo conectar con el servidor.");
    }
  };

  const handleMarkLate = async () => {
    if (!empNumber) {
      Alert.alert("Error", "Ingresa el número de empleado.");
      return;
    }

    try {
      const details = new URLSearchParams();
      details.append('employ_number', empNumber.trim());

      const response = await fetch(MARK_LATE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: details.toString(),
      });

      const data = await response.json();

      if (response.ok) {
        Alert.alert("Éxito", data.message || "Retardo registrado correctamente.");
        setModalVisible(false);
        setEmpNumber('');
        setReason('');
        fetchHistory();
      } else {
        Alert.alert("Error", data.detail || "No se pudo registrar el retardo.");
      }
    } catch (error) {
      console.error(error);
      Alert.alert("Error de red", "No se pudo conectar con el servidor.");
    }
  };

  const filteredHistory = history.filter(item => {
    const matchesSearch = item.employee_name.toLowerCase().includes(search.toLowerCase()) ||
                          item.employ_number.includes(search) ||
                          item.date.includes(search);
    const matchesFilter = filterState === 'TODOS' || item.state === filterState;
    return matchesSearch && matchesFilter;
  });

  const getBadgeStyle = (state) => {
    switch (state) {
      case 'RETARDO':
        return styles.badgeRetardo;
      case 'PERMISO':
      case 'VACACIONES':
        return styles.badgePermiso;
      default:
        return styles.badgeOk;
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Historial y Control de Asistencias</Text>

      <TouchableOpacity style={styles.vacationButton} onPress={() => setModalVisible(true)}>
        <Text style={styles.vacationButtonText}>+ Registrar Incidencia / Permiso</Text>
      </TouchableOpacity>

      <TextInput
        style={styles.searchInput}
        placeholder="Buscar por empleado, # o fecha..."
        value={search}
        onChangeText={setSearch}
      />

      <View style={styles.filterRow}>
        {['TODOS', 'OK', 'RETARDO', 'PERMISO'].map((state) => (
          <TouchableOpacity
            key={state}
            style={[styles.filterBadge, filterState === state && styles.activeFilter]}
            onPress={() => setFilterState(state)}
          >
            <Text style={[styles.filterText, filterState === state && styles.activeFilterText]}>{state}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <FlatList
        data={filteredHistory}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.headerRow}>
              <Text style={styles.name}>{item.employee_name}</Text>
              <Text style={[styles.badge, getBadgeStyle(item.state)]}>
                {item.state}
              </Text>
            </View>
            <Text style={styles.subText}>Empleado #: {item.employ_number}</Text>
            <Text style={styles.subText}>Fecha: {item.date}</Text>
            <View style={styles.timeRow}>
              <Text style={styles.timeText}>Entrada: {item.check_in || '--:--'}</Text>
              <Text style={styles.timeText}>Salida: {item.check_out || '--:--'}</Text>
            </View>
          </View>
        )}
      />

      <Modal visible={modalVisible} animationType="slide" transparent={true}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Registrar Incidencia</Text>
            
            <TextInput
              style={styles.input}
              placeholder="Número de empleado"
              value={empNumber}
              onChangeText={setEmpNumber}
              keyboardType="numeric"
            />
            
            <TextInput
              style={styles.input}
              placeholder="Motivo (Solo para Permisos)"
              value={reason}
              onChangeText={setReason}
            />

            <View style={styles.modalButtons}>
              <TouchableOpacity style={[styles.btn, styles.btnCancel]} onPress={() => setModalVisible(false)}>
                <Text style={styles.btnText}>Cancelar</Text>
              </TouchableOpacity>

              <TouchableOpacity style={[styles.btn, { backgroundColor: '#FF9500' }]} onPress={handleMarkLate}>
                <Text style={styles.btnText}>+ Retardo</Text>
              </TouchableOpacity>

              <TouchableOpacity style={[styles.btn, styles.btnSend]} onPress={handleSendLeave}>
                <Text style={styles.btnText}>+ Permiso</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 15, backgroundColor: '#F5F5F5', paddingTop: 45 },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 10, color: '#333' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  vacationButton: { backgroundColor: '#34C759', padding: 10, borderRadius: 8, marginBottom: 10, alignItems: 'center' },
  vacationButtonText: { color: '#FFF', fontWeight: 'bold', fontSize: 13 },
  searchInput: { backgroundColor: '#FFF', padding: 10, borderRadius: 8, borderWidth: 1, borderColor: '#DDD', marginBottom: 10 },
  filterRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  filterBadge: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 15, backgroundColor: '#E0E0E0' },
  activeFilter: { backgroundColor: '#007AFF' },
  filterText: { fontSize: 12, fontWeight: 'bold', color: '#555' },
  activeFilterText: { color: '#FFF' },
  card: { backgroundColor: '#FFF', padding: 14, borderRadius: 10, marginBottom: 10, elevation: 2 },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  name: { fontSize: 15, fontWeight: 'bold', color: '#111' },
  badge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 5, fontWeight: 'bold', fontSize: 12 },
  badgeOk: { backgroundColor: '#E8F5E9', color: '#2E7D32' },
  badgeRetardo: { backgroundColor: '#FFEBEE', color: '#C62828' },
  badgePermiso: { backgroundColor: '#FFF3E0', color: '#E65100' },
  subText: { fontSize: 13, color: '#666', marginTop: 2 },
  timeRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 8, paddingTop: 6, borderTopWidth: 1, borderTopColor: '#EEE' },
  timeText: { fontSize: 13, fontWeight: '600', color: '#007AFF' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { width: '90%', backgroundColor: '#FFF', padding: 20, borderRadius: 10 },
  modalTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 15 },
  input: { backgroundColor: '#F0F0F0', padding: 10, borderRadius: 8, marginBottom: 12 },
  modalButtons: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 10 },
  btn: { flex: 1, paddingVertical: 10, paddingHorizontal: 4, borderRadius: 8, alignItems: 'center', marginHorizontal: 2 },
  btnCancel: { backgroundColor: '#8E8E93' },
  btnSend: { backgroundColor: '#007AFF' },
  btnText: { color: '#FFF', fontWeight: 'bold', fontSize: 12 }
});