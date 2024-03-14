import CanCreate from "@/network/info";
import styles from "./info.module.css";
import Router from "router";

export function Check() {
  if (CanCreate) {
    return (
      <div className={styles.container}>
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
      </div>
    );
  } else {
    return (
      <div>
        <h1>Wait for the administrator to sign you up</h1>
        <button className={styles.button}>
          <a href="./logged_out/sign_in" className={styles.link}>
            Sign In
          </a>
        </button>
      </div>
    );
  }
}

export default function Home() {
  return (
    <main>
      <title>Info</title>
      <Check />
    </main>
  );
}
