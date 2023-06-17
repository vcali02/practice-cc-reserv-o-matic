import React from "react";

function LocationCard({location}) {
  return (
    <tr>
      <td>{location.id}</td>
      <td>{location.name}</td>
      <td>{location.max_party_size}</td>
    </tr>
  );
}

export default LocationCard;
