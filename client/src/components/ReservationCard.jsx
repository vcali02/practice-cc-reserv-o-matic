import React from "react";

function ReservationCard({reservation, onDeleteReservation}) {
  function handleDeleteReservation() {
    fetch(`/reservations/${reservation.id}`, {
      method: "DELETE",
      headers: {"Content-Type": "application/json"},
    }).then(response => {
      if (response.ok) {
        onDeleteReservation(reservation.id);
      }
    });
  }
  return (
    <tr>
      <td>{reservation.id}</td>
      <td>{reservation.party_name}</td>
      <td>{reservation.customer.name}</td>
      <td>{reservation.location.name}</td>
      <td>{reservation.party_size}</td>
      <td>
        <button
          className="btn btn-sm btn-error"
          onClick={() => handleDeleteReservation()}>
          Delete
        </button>
      </td>
    </tr>
  );
}

export default ReservationCard;
