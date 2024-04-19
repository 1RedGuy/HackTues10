"use client";

import styles from "./my_subjects.module.css";
import { getMySubjects } from "../../../network/user";
import Cookies from "js-cookie";
import { useState, useEffect } from "react";
import Loading from "@/components/loading/loading";
import { set } from "react-hook-form";

export default function MySubjects() {
  const [subjects, updateSubjects] = useState([]);
  const jwtToken = Cookies.get("jwtToken");
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true);
    const getSubjects = async () => {
      try {
        const response = await getMySubjects(jwtToken);
        updateSubjects(response.response);
      } catch (error) {
        setError("Failed to fetch subjects. Please try again later.");
        console.error("Error fetching subjects:", error);
      } finally {
        setLoading(false);
      }
    };
    if (jwtToken) {
      getSubjects();
    }
  }, []);
  return loading ? (
    <Loading />
  ) : (
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
