"use client";
import Cookies from "js-cookie";
import { useState } from "react";
import SetState from "../../../utils/setState";
import { SignInRequest } from "../../../network/auth";
import styles from "./sign_in.module.css";
import Router from "router";

export default function SignIn() {
  const [state, updateState] = useState({
    name: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const jwtToken = SignInRequest(state);
      Cookies.set("jwtToken", jwtToken, { expires: 0.5 });
      Router.push("../../admin");
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
