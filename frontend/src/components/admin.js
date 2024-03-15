"use client";
import styles from "./admin_components.module.css";
import { useState } from "react";
import SetState from "../utils/setState";
import AddObject from "../utils/addObject";
import { CreateSubject, Connect } from "../network/admin";

export function UserForm({ prop, UpdateProp, labels }) {
  const initialState = {
    name: "",
    email: "",
    role: "",
  };

  const [state, updateState] = useState(initialState);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    try {
      AddObject(prop, state, UpdateProp);
    } catch (err) {
      setError("An error occurred while adding the user. Please try again.");
      console.error(err);
    }
  };

  return (
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        {labels.map((label) => (
          <div key={label}>
            <label htmlFor={label.toLowerCase()} className={styles.label}>
              {label}
            </label>
            <input
              id={label.toLowerCase()}
              name={label.toLowerCase()}
              type={label.toLowerCase() === "email" ? "email" : "text"}
              value={state[label.toLowerCase()]}
              onChange={(e) =>
                SetState(
                  state,
                  label.toLowerCase(),
                  updateState,
                  e.target.value
                )
              }
              className={styles.input}
            />
          </div>
        ))}
        <div>
          <label htmlFor="role" className={styles.label}>
            Role
          </label>
          <select
            id="role"
            name="role"
            value={state.role}
            onChange={(e) => updateState({ ...state, role: e.target.value })}
            className={styles.input}
          >
            <option value="">Select role</option>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
        </div>
        {error && <div className={styles.error}>{error}</div>}
        <button type="submit" className={styles.button}>
          Create User
        </button>
      </form>
    </div>
  );
}
export function SubjectForm({ prop, UpdateProp, users }) {
  const initialState = {
    name: "",
    teacher_id: 0,
  };

  const [state, updateState] = useState(initialState);
  const [error, setError] = useState("");
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await CreateSubject(state);
      UpdateProp(state);
    } catch (err) {
      setError(
        "An error occurred while creating the subject. Please try again."
      );
      console.error(err);
    }
  };

  return (
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name</label>
          <input
            id="name"
            name="name"
            type="text"
            value={state.name}
            onChange={(e) =>
              SetState(state, "name", updateState, e.target.value)
            }
          />
        </div>
        <div>
          <label htmlFor="userSelect">Select Users:</label>
          <select
            className={styles.select}
            id="userSelect"
            name="userSelect"
            value={state.teacher_id}
            onChange={(e) => {
              SetState(state, "teacher_id", updateState, e.target.value);
            }}
          >
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </div>
        {error && <div style={{ color: "red" }}>{error}</div>}
        <button type="submit" className={styles.button}>
          Create Subject
        </button>
      </form>
    </div>
  );
}

export function StudentForm({ UpdateState, AllUsers, AllSubjects }) {
  const initialState = {
    subject_id: null,
    students_ids: {
      student_ids: [],
    },
  };

  const [state, updateState] = useState(initialState);
  const [error, setError] = useState("");

  const handleSubjectChange = (e) => {
    const subjectId = e.target.value ? Number(e.target.value) : null;
    updateState((prevState) => ({ ...prevState, subject_id: subjectId }));
  };

  const handleUserSelection = (e) => {
    const studentIds = Array.from(e.target.selectedOptions).map((option) => ({
      student_id: Number(option.value),
    }));
    updateState((prevState) => ({
      ...prevState,
      students_ids: { ...prevState.students_ids, student_ids: studentIds },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      UpdateState(state);
      await Connect(state.subject_id, state.students_ids);
    } catch (err) {
      setError("An error occurred. Please try again.");
      console.error(err);
    }
  };

  return (
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <div>
          <label htmlFor="subjectSelect">Select Subject:</label>
          <select
            className={styles.select}
            id="subjectSelect"
            name="subjectSelect"
            onChange={handleSubjectChange}
            value={state.subject_id || ""}
          >
            <option value="">Select a subject</option>
            {AllSubjects.map((subject) => (
              <option key={subject.id} value={subject.id}>
                {subject.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="userSelect">Select Students:</label>
          <select
            className={styles.select}
            multiple
            id="userSelect"
            name="userSelect"
            onChange={handleUserSelection}
            value={state.students_ids.student_ids.map((s) => s.student_id)}
          >
            {AllUsers.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </div>

        {error && <div style={{ color: "red" }}>{error}</div>}

        <button type="submit" className={styles.button}>
          Submit
        </button>
      </form>
    </div>
  );
}
export function AllUsers({ users }) {
  return (
    <div className={styles.formContainer}>
      {users.map((user, index) => (
        <div key={index}>
          <h2>{user.name}</h2>
          <div>
            {Object.entries(user).map(([key, value]) => (
              <p key={key}>
                <strong>{key}:</strong> {value}
              </p>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
