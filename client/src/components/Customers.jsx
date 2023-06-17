import React from "react";
import CustomerCard from "./CustomerCard";

function Customers({customers, toggleForms}) {
  const displayCustomers = customers.map(customer => (
    <CustomerCard key={customer.id} customer={customer} />
  ));
  return (
    <div className="overflow-x-auto h-[250px]">
      <div className="flex flex-row align-center justify-center gap-4 mx-auto my-2">
        <h2 className="text-2xl">CUSTOMERS</h2>
        <button className="btn btn-primary btn-sm" onClick={toggleForms}>
          Add New Customer
        </button>
      </div>
      <table className="table table-xs">
        {/* head */}
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>{displayCustomers}</tbody>
      </table>
    </div>
  );
}

export default Customers;
