import React, { useState } from "react";
import styles from "../components/SignIn.module.css";

const SignUp = () => {
    const [formData, setFormData] = useState({
        name: "",
        age: "",
        gender: "Male",
        username: "",
        email: "",
        password: "",
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };
    
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Signing up with:", formData);
        // TODO: APIリクエストの実装
    };

    return (
        <div className={styles["form-container"]}>
        <form onSubmit={handleSubmit}>
        <h1>Create an Account</h1>
            <div>
                <label>Name: </label>
                <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>
            <div>
                <label>Age: </label>
                <input type="number" name="age" value={formData.age} onChange={handleChange} required />
            </div>
            <div>
            <label>Gender: </label>
            <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
            </select>
            </div>
            <div>
                <label>Username:</label>
                <input type="text" name="username" value={formData.username} onChange={handleChange} required />
            </div>
            <div>
                <label>Email:</label>
                <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>
            <div>
                <label>Password:</label>
                <input type="password" name="password" value={formData.password} onChange={handleChange} required />
            </div>
            <button type="submit" className={styles.button}>Sign Up</button>
        </form>
        </div>
    );
};

export default SignUp;
