"use client";
import { useState, useEffect } from "react";
import { CreateUser, GetSubjects, GetUser } from "../../../network/admin";
import {
  UserForm,
  SubjectForm,
  AllUsers,
  StudentForm,
} from "../../../components/admin";
import styles from "./admin.module.css";
import Cookies from "js-cookie";

export default function Admin_page() {
  const [isComponentVisible, setComponentVisible] = useState({
    first: false,
    second: false,
    third: false,
    fourth: false,
  });
  const [users, updateUsers] = useState([]);
  const [subject, updateSubject] = useState({ name: "", teacher_id: 0 });
  const [allUsers, updateAllUsers] = useState([]);
  const [allSubjects, updateAllSubject] = useState([]);

  const [students, updateStudents] = useState({
    subject_id: null,
    students_ids: {
      student_ids: [],
    },
  });
  const [error, setError] = useState("");
  const jwtToken = Cookies.get("jwtToken");

  function setVisible(prop) {
    setComponentVisible((prev) => ({ ...prev, [prop]: true }));
  }

  function setInvisible(prop) {
    setComponentVisible((prev) => ({ ...prev, [prop]: false }));
  }

  const getUsers = async (role) => {
    try {
      const response = await GetUser(role, jwtToken);
      updateAllUsers(response.response);
    } catch (error) {
      setError("Failed to fetch users. Please try again later.");
      console.error("Error fetching users:", error);
    }
  };

  useEffect(() => {
    const getSubjects = async () => {
      try {
        const response = await GetSubjects(jwtToken);
        updateAllSubject(response.response);
      } catch (error) {
        setError("Failed to fetch subjects. Please try again later.");
        console.error("Error fetching subjects:", error);
      }
    };

    if (jwtToken) {
      getSubjects();
    }
  }, []);

  const handleCreateUsers = async () => {
    try {
      setInvisible("first");
      return await CreateUser(users, jwtToken);
    } catch (error) {
      setError("Failed to create user. Please try again later.");
      console.error("Error creating user:", error);
    }
  };
  useEffect(() => {
    const clearErrorOnClick = () => setError(""); // Clear error on any click within this component
    document.addEventListener("click", clearErrorOnClick);

    return () => document.removeEventListener("click", clearErrorOnClick);
  }, []);

  return (
    <div className={styles.container}>
      {Object.values(isComponentVisible).every((value) => value === false) && (
        <button className={styles.button} onClick={() => setVisible("first")}>
          Create users
        </button>
      )}
      {isComponentVisible.first && (
        <div className={styles.feature_container}>
          <UserForm
            prop={users}
            UpdateProp={updateUsers}
            labels={["name", "email"]}
          />
          <div>
            <button className={styles.button} onClick={handleCreateUsers}>
              Create users
            </button>
            <button
              className={styles.button}
              onClick={() => {
                setInvisible("first");
              }}
            >
              Exit
            </button>
          </div>
        </div>
      )}
      {Object.values(isComponentVisible).every((value) => value === false) && (
        <button
          className={styles.button}
          onClick={() => {
            setVisible("second");
          }}
        >
          See all profiles
        </button>
      )}
      {isComponentVisible.second && (
        <div className={styles.feature_container}>
          <button
            className={styles.button}
            onClick={() => {
              getUsers("teacher");
            }}
          >
            Teachers
          </button>
          <button
            className={styles.button}
            onClick={() => {
              getUsers("student");
            }}
          >
            Students
          </button>

          <AllUsers users={allUsers} />

          <button
            className={styles.button}
            onClick={() => {
              setInvisible("second");
            }}
          >
            Exit
          </button>
        </div>
      )}
      {Object.values(isComponentVisible).every((value) => value === false) && (
        <button
          className={styles.button}
          onClick={() => {
            getUsers("teacher");
            setVisible("third");
          }}
        >
          Create subject
        </button>
      )}
      {isComponentVisible.third && (
        <div className={styles.feature_container}>
          <SubjectForm
            prop={subject}
            UpdateProp={updateSubject}
            users={allUsers}
          />
          <button
            className={styles.button}
            onClick={() => {
              setInvisible("third");
            }}
          >
            Exit
          </button>
        </div>
      )}
      {Object.values(isComponentVisible).every((value) => value === false) && (
        <button
          className={styles.button}
          onClick={() => {
            getUsers("student");
            setVisible("fourth");
          }}
        >
          Attach students
        </button>
      )}
      {isComponentVisible.fourth && (
        <div>
          <StudentForm
            UpdateState={updateStudents}
            AllUsers={allUsers}
            AllSubjects={allSubjects}
          />
          <button
            className={styles.button}
            onClick={() => {
              setInvisible("fourth");
            }}
          >
            Exit
          </button>
        </div>
      )}

      {error && <div style={{ color: "red" }}>{error}</div>}
    </div>
  );
}
