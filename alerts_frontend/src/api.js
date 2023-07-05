// src/api.js
import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Replace with your API base URL

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getItems = async () => {
  try {
    const response = await api.get("/alert");
    return response.data;
  } catch (error) {
    console.log("Error fetching items:", error);
    throw error;
  }
};

export const addItem = async (item) => {
  try {
    const response = await api.post("/alert", item);
    return response.data;
  } catch (error) {
    console.log("Error adding item:", error);
    throw error;
  }
};
