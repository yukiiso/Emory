import { Link } from "react-router-dom";
import styles from "./Navbar.module.css";

const Navbar = () => {
    return (
		<div className={styles.navbar}>
			<img src="/logo_green.png" alt="Logo" className={styles.logo} />
			<Link to="/talk" className={styles.navButton}>
			{/* <img src="/talk.png" alt="Logo" className={styles.navImg} /> */}
			</Link>
			<Link to="/dash" className={styles.navButton}>Dash</Link>
		</div>
    );
};

export default Navbar;
