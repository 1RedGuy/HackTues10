"use client";
import Cookies from "js-cookie";
import { useState } from "react";
import SetState from "../../../utils/setState";
import { SignUpRequest } from "../../../network/auth";
import styles from "./sign_up.module.css";
import Router from "router";
import Loading from "@/components/loading/loading";
import { set } from "react-hook-form";

export default function SignUp() {
  const [state, updateState] = useState({
    name: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });
  const [loading, setLoading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const jwtToken = await SignUpRequest(state);
      Cookies.set("jwtToken", jwtToken, { expires: 0.5 });
      Router.push("../../logged_in/admin");
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return loading ? (
    <Loading />
  ) : (
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <label htmlFor="name" className={styles.label}>
          Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          value={state.name}
          onChange={(e) => SetState(state, "name", updateState, e.target.value)}
          className={styles.input}
        />
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
        <label htmlFor="passwordConfirm" className={styles.label}>
          Password Confirm
        </label>
        <input
          id="passwordConfirm"
          name="passwordConfirm"
          type="password"
          value={state.passwordConfirm}
          onChange={(e) =>
            SetState(state, "passwordConfirm", updateState, e.target.value)
          }
          className={styles.input}
        />
        <button type="submit" className={styles.button}>
          Sign Up
        </button>
      </form>
    </div>
  );
}
