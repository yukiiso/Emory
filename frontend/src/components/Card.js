import React from "react";
import styles from "./Card.module.css";

const Card = ({ title, description, onClick }) => {
    return (
        <div className={styles.card} onClick={() => onClick(description)}>
            <div>
                <h2 className={styles.cardTitle}>{title}</h2>
                <p className={styles.cardDescription}>{description}</p>
            </div>
        </div>
    );
};

export default Card;
