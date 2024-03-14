import Navbar from "../../components/navbar_in";

export default function Layout({ children }) {
  return (
    <main>
      <Navbar />
      {children}
    </main>
  );
}
