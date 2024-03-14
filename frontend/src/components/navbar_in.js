import Link from "next/link";
import styles from "./navbar.module.css";

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <Link href="/logged_out/sign_up" className={styles.link}>
        My Subjects
      </Link>
      <Link href="/logged_out/sign_in" className={styles.link}>
        My profile
      </Link>
    </nav>
  );
}
