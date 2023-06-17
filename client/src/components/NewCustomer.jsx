import {useState} from "react";

function NewCustomer({onAddNewCustomer}) {
  const [formData, setFormData] = useState({name: "", email: ""});
  const [errors, setErrors] = useState([]);
  function handleChange(event) {
    const name = event.target.name;
    let value =
      event.target.type === "checkbox"
        ? event.target.checked
        : event.target.value;

    setFormData({...formData, [name]: value});
  }

  function handleSubmit(event) {
    event.preventDefault();
    fetch("/customers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    }).then(response => {
      if (response.status === 400) {
        console.log(response);
        setErrors([response.status, response.statusText]);
      } else if (response.ok) {
        response.json().then(customer => {
          setFormData({name: "", email: ""});
          setErrors([]);
          onAddNewCustomer(customer);
        });
      } else {
        response.json().then(error => setErrors(error.errors));
      }
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <h2 className="text-2xl text-center">Add New Customer</h2>
      <div className="flex flex-row justify-between items-center">
        <label htmlFor="name">Name</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={event => handleChange(event)}
          className="input input-bordered input-xs input-primary w-64 "
        />
      </div>
      <div className="flex flex-row justify-between items-center">
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={event => handleChange(event)}
          className="input input-bordered input-xs input-primary w-64"
        />
      </div>
      {errors.map(error => (
        <p key={error} style={{color: "red"}}>
          {error}
        </p>
      ))}
      <button type="submit" className="btn btn-success btn-sm">
        Submit
      </button>
    </form>
  );
}

export default NewCustomer;
