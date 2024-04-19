"use client";

import CanCreate from "@/network/info";
import styles from "./info.module.css";
import React, { useState, useEffect } from "react";
import Loading from "@/components/loading/loading";

export function Check() {
  const [canCreate, setCanCreate] = useState(null);
  const [loading, setLoading] = useState(false);
  {
    console.log(process.env.NEXT_PUBLIC_SERVER_URL);
  }
  useEffect(() => {
    setLoading(true);
    const fetchCanCreateStatus = async () => {
      try {
        const response = await CanCreate();
        setCanCreate(response.response);
      } catch {
      } finally {
        setLoading(false);
      }
    };

    fetchCanCreateStatus();
  }, []);
  return canCreate !== null && loading ? (
    <Loading />
  ) : (
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
  );
}

export default function Home() {
  return (
    <main>
      <Check />
    </main>
  );
}
