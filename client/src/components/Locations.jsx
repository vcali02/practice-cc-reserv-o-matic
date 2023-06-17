import React from "react";
import LocationCard from "./LocationCard";
function Locations({locations}) {
  const displayLocations = locations.map(location => (
    <LocationCard key={location.id} location={location} />
  ));
  return (
    <div className="overflow-x-auto h-[250px] pt-4">
      <h2 className="text-2xl">LOCATIONS</h2>
      <table className="table table-xs">
        {/* head */}
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Maximum Party Size</th>
          </tr>
        </thead>
        <tbody>{displayLocations}</tbody>
      </table>
    </div>
  );
}

export default Locations;
