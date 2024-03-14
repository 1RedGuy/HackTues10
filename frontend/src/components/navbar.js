import Link from "next/link";
import styles from "./navbar.module.css";

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <Link href="/" className={styles.home}>
        Home
      </Link>
      <Link href="/logged_out/sign_up" className={styles.link}>
        Sign up
      </Link>
      <Link href="/logged_out/sign_in" className={styles.link}>
        Sign in
      </Link>
    </nav>
  );
}
