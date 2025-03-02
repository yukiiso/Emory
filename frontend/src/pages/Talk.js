import React, { useState } from "react";
import styles from "../components/Talk.module.css";
import Card from "../components/Card";
import { useNavigate } from "react-router-dom";

const Talk = () => {
    // TO DO: Check if user is signed in

    const [selectedQuestion, setSelectedQuestion] = useState(null);
    const navigate = useNavigate();

    const handleQuestionSelect = (question) => {
        setSelectedQuestion(question);
        navigate("/record", { state: { question } });  // history.pushからnavigateに変更
    };
    
    return (
        <div className={styles["page-container"]}>
            <h1 className={styles.title}>Choose the question and tell me about youself!</h1>
            <div className={styles["card-container"]}>
                <Card title="Question 1" description="What is the concern or problem that brought you here?" onClick={handleQuestionSelect} />
                <Card title="Question 2" description="How is this concern or problem impacting your life? " onClick={handleQuestionSelect} />
                <Card title="Question 3" description="What are your hopes and wishes for resolving this concern or problem?" onClick={handleQuestionSelect} />
                <Card title="Question 4" description="What activities do you enjoy doing?" onClick={handleQuestionSelect} />
                <Card title="Question 5" description="Is there anything you want to talk about?" onClick={handleQuestionSelect} />
            </div>
        </div>
    );
};

export default Talk;