import Link from "next/link";
import styles from "./navbar.module.css";

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <Link href="/logged_in" className={styles.link}>
        Home
      </Link>
      <Link href="/logged_in/my_subjects" className={styles.link}>
        My Subjects
      </Link>
      <Link href="/logged_in/my_profile" className={styles.link}>
        My profile
      </Link>
    </nav>
  );
}
