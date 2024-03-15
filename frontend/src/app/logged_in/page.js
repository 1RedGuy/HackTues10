import styles from "./logged_in.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      <h1>Welcome</h1>
      <h1>Go to my subjects to see the presentations</h1>
    </div>
  );
}
