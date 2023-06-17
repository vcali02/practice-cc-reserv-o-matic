import React from "react";
import Logo from "../assets/reserv-o-matic-logos_white.png";
function Header() {
  return (
    <div className="flex flex-row align-middle justify-center">
      <img src={Logo} alt="logo" className="h-24 align-center" />
      <div className="my-auto text-2xl">Reserv-o-Matic Tracking System</div>
    </div>
  );
}

export default Header;
