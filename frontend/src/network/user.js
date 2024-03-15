import axios from "axios";

export async function MyProfile() {
  try {
    const response = axios.get("http://localhost:5000/profiles/me");
    return response.data;
  } catch (error) {
    console.error("CreateUser error:", error);
    throw error;
  }
}
