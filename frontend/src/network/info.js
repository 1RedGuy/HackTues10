import axios from "axios";

export default async function CanCreate() {
  return (await axios.get(`${process.env.NEXT_PUBLIC_SERVER_URL}/info`)).data;
}
