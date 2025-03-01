import React, { useState } from "react";
import styles from "../components/Talk.module.css";
import Card from "../components/Card";

const Talk = () => {
    // TO DO: Check if user is signed in

    return (
        <div className={styles["page-container"]}>
            <h1 className={styles.title}>Choose the question and tell me about youself!</h1>
            <div className={styles["card-container"]}>
                <Card title="Question 1" description="What is the concern or problem that brought you here?" />
                <Card title="Question 2" description="How is this concern or problem impacting your life? " />
                <Card title="Question 3" description="What are your hopes and wishes for resolving this concern or problem?" />
                <Card title="Question 4" description="What activities do you enjoy doing?" />
                <Card title="Question 5" description="Is there anything you want to talk about?" />
            </div>
        </div>
    );
};

export default Talk;