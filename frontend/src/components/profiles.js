"use client";
import styles from "./profiles.module.css";
import { useState } from "react";
import SetState from "../utils/setState";
import AddObject from "../utils/addObject";

export default function Form({ users, UpdateUsers, names, UpdadeNames }) {
  const [state, updateState] = useState({
    name: "",
    role: "",
    email: "",
  });
  const handleSubmit = (e) => {
    e.preventDefault();

    AddObject(users, state, UpdateUsers);

    UpdadeNames(...names, state.name);
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
        <label htmlFor="role" className={styles.label}>
          Role - Teacher or Student
        </label>
        <input
          id="role"
          name="role"
          type="text"
          value={state.role}
          onChange={(e) => SetState(state, "role", updateState, e.target.value)}
          className={styles.input}
        />

        <button type="submit" className={styles.button}>
          Create user
        </button>
      </form>
    </div>
  );
}
