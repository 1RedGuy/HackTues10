import Navbar from "../../components/navbar_out";

export default function Layout({ children }) {
  return (
    <main>
      <Navbar />
      {children}
    </main>
  );
}
