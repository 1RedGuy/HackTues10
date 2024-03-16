import axios from "axios";

export async function SignUpRequest(name, email, password, passwordConfirm) {
  return await axios.post(`${process.env.NEXT_PUBLIC_SERVER_URL}/sign-up`, {
    name,
    email,
    password,
    passwordConfirm,
  }).data;
}

export async function SignInRequest({ email, password }) {
  return (
    await axios.post(`${process.env.NEXT_PUBLIC_SERVER_URL}/sign-in`, {
      email,
      password,
    })
  ).data;
}
