"use client";

import styles from "./my_subjects.module.css";
import { getMySubjects } from "../../../network/user";
import Cookies from "js-cookie";
import { useState, useEffect } from "react";

export default function MySubjects() {
  const [subjects, updateSubjects] = useState([]);
  const jwtToken = Cookies.get("jwtToken");
  useEffect(() => {
    const getSubjects = async () => {
      try {
        const response = await getMySubjects(jwtToken);
        updateSubjects(response.response);
      } catch (error) {
        setError("Failed to fetch subjects. Please try again later.");
        console.error("Error fetching subjects:", error);
      }
    };
    if (jwtToken) {
      getSubjects();
    }
  }, []);
  return (
    <div className={styles.formContainer}>
      {subjects.map((subject, index) => (
        <div key={index}>
          <h2>{subject.name}</h2>
          <h2>{subject.teacher_id}</h2>
        </div>
      ))}
    </div>
  );
}
