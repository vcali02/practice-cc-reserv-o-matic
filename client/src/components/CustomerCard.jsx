import React from "react";

function CustomerCard({customer}) {
  return (
    <tr>
      <td>{customer.id}</td>
      <td>{customer.name}</td>
      <td>{customer.email}</td>
    </tr>
  );
}

export default CustomerCard;
