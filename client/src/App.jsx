import {useState, useEffect} from "react";
import {Link} from "react-router-dom";
import Customers from "./components/Customers";
import Locations from "./components/Locations";
import Reservations from "./components/Reservations";

import "./App.css";
import Header from "./components/Header";
import NewCustomer from "./components/NewCustomer";
import NewReservation from "./components/NewReservation";

function App() {
  const [customers, setCustomers] = useState([]);
  const [locations, setLocations] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [showForms, setShowForms] = useState(false);
  useEffect(() => {
    fetch("/customers")
      .then(r => r.json())
      .then(customers => setCustomers(customers));
  }, []);

  useEffect(() => {
    fetch("/locations")
      .then(r => r.json())
      .then(locations => setLocations(locations));
  }, []);
  useEffect(() => {
    fetch("/reservations")
      .then(r => r.json())
      .then(reservations => setReservations(reservations));
  }, []);

  function onDeleteReservation(id) {
    const updatedReservations = reservations.filter(
      reservation => reservation.id !== id,
    );
    setReservations(updatedReservations);
  }
  function toggleForms() {
    setShowForms(prevShowForms => !prevShowForms);
  }

  function onAddNewCustomer(newCustomer) {
    setCustomers(customers => [newCustomer, ...customers]);
  }
  function onAddNewReservation(newReservation) {
    setReservations(reservations => [newReservation, ...reservations]);
  }
  return (
    <main className="flex flex-col w-full justify-center align-middle items-center mx-auto">
      <Header />
      {showForms ? (
        <div
          className="flex flex-row w-full items-sta justify-center h-fit"
          id="forms">
          <div className="w-1/3 h-fit">
            <NewCustomer onAddNewCustomer={onAddNewCustomer} />
          </div>
          <div className="divider divider-horizontal">OR</div>
          <div className="h-fit w-1/3">
            <NewReservation
              customers={customers}
              locations={locations}
              onAddNewReservation={onAddNewReservation}
            />
          </div>
        </div>
      ) : null}

      <div className="flex w-full justify-center items-center">
        <Customers customers={customers} toggleForms={toggleForms} />
      </div>
      <div className="divider my-4"></div>
      <div className="flex w-full justify-center items-center">
        <Locations locations={locations} />
      </div>
      <div className="divider my-4"></div>
      <div className="flex w-full justify-center items-center">
        <Reservations
          reservations={reservations}
          onDeleteReservation={onDeleteReservation}
        />
      </div>
    </main>
  );
}

export default App;
