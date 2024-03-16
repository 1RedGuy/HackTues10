"use client";

import styles from "./my_profile.module.css";
import { getMyProfile } from "../../../network/user";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";

export default function MyProfile() {
  const [user, updateUser] = useState({});

  useEffect(() => {
    async function getProfile() {
      try {
        const jwtToken = Cookies.get("jwtToken");
        const response = await getMyProfile(jwtToken);

        updateUser({ ...user, ...response.response });
      } catch (error) {
        console.error("Error:", error);
      }
    }
    getProfile();
  }, []);
  const handleLogout = () => {
    Cookies.remove("jwtToken");
    window.location.href = "/";
  };

  return (
    <div className={styles.container}>
      <h2>My Profile</h2>
      <div>
        <strong>Name:</strong> {user.name}
      </div>
      <div>
        <strong>Email:</strong> {user.email}
      </div>
      <div>
        <strong>Role:</strong> {user.role}
      </div>
      <div>
        <strong>ID:</strong> {user.id}
      </div>
      <button
        className={styles.button}
        onClick={() => {
          handleLogout();
        }}
      >
        Sign out
      </button>
    </div>
  );
}
