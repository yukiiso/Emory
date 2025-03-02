import { Link, useNavigate } from "react-router-dom";
import styles from "./Navbar.module.css";

const Navbar = () => {
	const navigate = useNavigate();

    // ログアウト処理
    const handleLogout = () => {
        // セッションまたは認証状態をクリア
        localStorage.removeItem("user"); // 例: ローカルストレージからユーザー情報を削除

        // リダイレクトしてログインページに遷移
        navigate("/sign-in");
    };
    return (
		<div className={styles.navbar}>
			<img src="/logo_green.png" alt="Logo" className={styles.logo} />
			<Link to="/talk" className={styles.navButton}>
				<img src="/talk.png" alt="Talk" className={styles.navImg} />
			</Link>
			<Link to="/dash" className={styles.navButton}>
				<img src="/dash.png" alt="Dashboard" className={styles.navImg} />
			</Link>
			<button onClick={handleLogout} className={styles.signoutButton}>
                Sign Out
            </button>
		</div>
    );
};

export default Navbar;
