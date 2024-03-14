import axios from "axios";

export default async function CanCreate() {
  return (await axios.get("http://localhost:5000/profiles")).data;
}
