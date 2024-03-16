"use client";
import Cookies from "js-cookie";
import { useState } from "react";
import SetState from "../../../utils/setState";
import { SignInRequest } from "../../../network/auth";
import styles from "./sign_in.module.css";
import { useRouter } from "next/navigation";

export default function SignIn() {
  const [state, updateState] = useState({
    email: "",
    password: "",
  });

  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await SignInRequest(state);
      if (response.response != null && response.response != undefined) {
        const jwtToken = response.response;
        Cookies.set("jwtToken", jwtToken, { expires: 0.5 });
        router.push("/logged_in");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <label htmlFor="email" className={styles.label}>
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          value={state.email}
          onChange={(e) =>
            SetState(state, "email", updateState, e.target.value)
          }
          className={styles.input}
        />
        <label htmlFor="password" className={styles.label}>
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          value={state.password}
          onChange={(e) =>
            SetState(state, "password", updateState, e.target.value)
          }
          className={styles.input}
        />

        <button type="submit" className={styles.button}>
          Sign In
        </button>
      </form>
    </div>
  );
}
