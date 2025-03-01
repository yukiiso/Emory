import React from "react";
import { Link } from "react-router-dom";
import styles from "./Card.module.css";

const Card = ({ title, description }) => {
    return (
        <Link to="/sign-in" className={styles.card}>
            <div>
                <h2 className={styles.cardTitle}>{title}</h2>
                <p className={styles.cardDescription}>{description}</p>
            </div>
        </Link>
    );
};

export default Card;
