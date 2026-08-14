import Header from "../components/Header/Header";
import CarForm from "../components/CarForm/CarForm";

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