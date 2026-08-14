import Header from "../components/Header/Header";
import CarForm from "../components/CarForm.jsx";

function Dashboard() {
  return (
    <>
      <Header />

      <main className="container">
        <CarForm />
      </main>
    </>
  );
}

export default Dashboard;