import axios from "axios";

export async function CreateUser(users) {
  await axios.post("http://localhost:5000/profiles", users);
}

export async function GetUser() {
  return (await axios.get("http://localhost:5000/profiles")).data;
}
