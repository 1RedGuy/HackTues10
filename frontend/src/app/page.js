"use client";

import CanCreate from "@/network/info";
import styles from "./info.module.css";
import React, { useState, useEffect } from "react";

export function Check() {
  const [canCreate, setCanCreate] = useState(null);
  {
    console.log(process.env.NEXT_PUBLIC_SERVER_URL);
  }
  useEffect(() => {
    const fetchCanCreateStatus = async () => {
      const response = await CanCreate();
      setCanCreate(response.response);
    };

    fetchCanCreateStatus();
  }, []);
  return canCreate !== null ? (
    <div className={styles.container}>
      {canCreate ? (
        <>
          <h1>You can sign up</h1>
          <div className={styles.buttons}>
            <button className={styles.button}>
              <a href="./logged_out/sign_up" className={styles.link}>
                Sign Up
              </a>
            </button>
            <button className={styles.button}>
              <a href="./logged_out/sign_in" className={styles.link}>
                Sign In
              </a>
            </button>
          </div>
        </>
      ) : (
        <>
          <h1>Wait for the administrator to sign you up</h1>
          <button className={styles.button}>
            <a href="./logged_out/sign_in" className={styles.link}>
              Sign In
            </a>
          </button>
        </>
      )}
    </div>
  ) : (
    <div>Loading...</div>
  );
}

export default function Home() {
  return (
    <main>
      <Check />
    </main>
  );
}
