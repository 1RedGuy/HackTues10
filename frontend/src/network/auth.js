import axios from "axios";

export async function SignUpRequest(name, email, password, passwordConfirm) {
  return await axios.post("http://localhost:5000/sign_up", {
    name,
    email,
    password,
    passwordConfirm,
  }).data;
}

export async function SignInRequest(email, password) {
  return await axios.post("http://localhost:5000/sign_in", {
    email,
    password,
  }).data;
}
