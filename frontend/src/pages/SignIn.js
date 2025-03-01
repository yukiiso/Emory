import React, { useState } from "react";
import styles from "../components/SignIn.module.css";

const SignIn = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log("Signing in with:", { username, password });
		// TODO: ここでAPIにリクエストを送る
  	};

	return (
		<div className={styles["form-container"]}>
		<form onSubmit={handleSubmit}>
		<h1>Sign In</h1>
			<div>
				<label>Username: </label>
				<input className={styles.input} type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
			</div>
			<div>
				<label>Password: </label>
				<input className={styles.input} type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
			</div>
			<button type="submit" className={styles.button}>Sign In</button>
		</form>
		</div>
	);
};

export default SignIn;
