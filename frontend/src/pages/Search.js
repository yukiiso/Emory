import React, { useState } from "react";
import styles from "../components/Search.module.css";
import { useNavigate } from "react-router-dom";

const Search = () => {
    const users = [
        { id: 1, username: "john_doe", name: "John Doe" },
        { id: 2, username: "jane_smith", name: "Jane Smith" },
        { id: 3, username: "michael_jackson", name: "Michael Jackson" },
    ];

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const navigate = useNavigate();

    const handleSearch = () => {
        // 検索クエリに一致するユーザーをフィルタリング
        const filteredUsers = users.filter(user =>
            user.username.toLowerCase().includes(query.toLowerCase())
        );
        setResults(filteredUsers);
    };

    const handleSelectUser = (username) => {
        navigate(`/dash?user=${username}`);
    };
    return (
        <div className={styles["page-container"]}>
            <h1>Search Users</h1>
            <div className={styles.searchBar}>
                <input type="text" placeholder="Enter username" value={query} onChange={(e) => setQuery(e.target.value)} className={styles["search-input"]}/>
                <button onClick={handleSearch} className={styles.searchButton}>
                    <img src="/search.png" alt="Search" className={styles.searchIcon} />
                </button>
            </div>
            <ul className={styles["results-list"]}>
                {results.map(user => (
                    <div className={styles["result-item"]}>
                        <li key={user.id}>{user.name} ({user.username}) </li>
                        <button className={styles["selectButton"]} onClick={() => handleSelectUser(user.username)}>
                            SELECT
                        </button>

                    </div>
                ))}
            </ul>
        </div>
    );
};

export default Search;
