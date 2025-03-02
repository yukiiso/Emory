import { Link } from "react-router-dom";
import styles from "./Navbar.module.css";

const Navbar = () => {
    return (
		<div className={styles.navbar}>
			<Link to="/talk" className={styles.navButton}>Talk</Link>
			<Link to="/dash" className={styles.navButton}>Dash</Link>
		</div>
    );
};

export default Navbar;
