"use client";
import { useState } from "react";
import { CreateUser } from "../../../network/profile";
import Form from "../../../components/profiles";
import styles from "./admin.module.css";

export default function Admin_page() {
  const [isComponentVisible, setComponentVisible] = useState(false);
  const [users, updateUsers] = useState([]);
  const [names, updateNames] = useState([]);
  const showComponent = () => {
    setComponentVisible(true);
  };

  const hideComponent = () => {
    setComponentVisible(false);
  };
  const handleSubmit = async () => {
    hideComponent();
    await CreateUser();
  };
  return (
    <div className={styles.container}>
      {!isComponentVisible && (
        <button className={styles.button} onClick={showComponent}>
          Create users
        </button>
      )}
      {isComponentVisible && (
        <div>
          <Form
            users={users}
            UpdateUsers={updateUsers}
            names={names}
            UpdadeNames={updateNames}
          />

          <button className={styles.button} onClick={handleSubmit}>
            Create users
          </button>
        </div>
      )}

      {!isComponentVisible && (
        <div>
          <button className={styles.button}>Create subject</button>
        </div>
      )}
      {!isComponentVisible && (
        <div>
          <button className={styles.button}>Attach students</button>
        </div>
      )}
    </div>
  );
}
