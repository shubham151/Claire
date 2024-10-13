"use client";
// pages/index.js

import React, { useState } from "react";
import Head from "next/head";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "@/styles/home.module.css";
// import {useLoading} from '@/app/Loading'

// const { setIsLoading } = useLoading();

// const colorNameToHex = {
//   // ... [Same as before, mapping color names to hex codes]
// };

// function extractColors(text) {
//   // ... [Same as before, function to extract colors from text]
// }

export default function Home() {
  const [text, setText] = useState("");
  const [topCount, setTopCount] = useState(5);
  const [results, setResults] = useState([]);
  const [lightMode, setLightMode] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make the API call here to fetch recent documents
      const response = await fetch("/api/fetch-response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          label: text,
          top_count: topCount,
        }),
      });

      if (response.ok) {
        const res = await response.json(); // Directly get the array
        console.log(res);
        setResults(res.res); // Set the results from the API
      } else {
        console.error("Error fetching documents and templates");
      }
    } catch (error) {
      console.error("Error:", error);
    }

    // Remove or comment out the following block if not needed
    /*
    const colorCounts = extractColors(text);
    const sortedColors = Object.entries(colorCounts).sort((a, b) => b[1] - a[1]);
    const topColors = sortedColors.slice(0, topCount);
    setResults(topColors);
    */
  }
  
  console.log("SM", results);

  const toggleLightMode = () => {
    setLightMode(!lightMode);
  };

  return (
    <div className={`${styles.app} ${lightMode ? styles.lightMode : ""}`}>
      <Head>
        <title>Color Analytics</title>
      </Head>

      <div className={styles.videoBg}>
        <video autoPlay loop muted>
          <source
            src="https://assets.codepen.io/3364143/7btrrd.mp4"
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className={styles.darkLight} onClick={toggleLightMode}>
        <svg
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="1.5"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
        </svg>
      </div>

      <div className={styles.container}>
        <div className={styles.contentWrapper}>
          <h1 className={styles.title}>Color Analytics</h1>

          <form onSubmit={handleSubmit} className={styles.form}>
            <div className="mb-3">
              <label htmlFor="textInput" className={`form-label `}>
                Enter Label:
              </label>
              <input
                className="form-control"
                id="textInput"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter the label eg. Car"
              ></input>
            </div>
            <div className="mb-3">
              <label htmlFor="topCountInput" className="form-label">
                Top Count:
              </label>
              <input
                type="number"
                className="form-control"
                id="topCountInput"
                value={topCount}
                onChange={(e) => setTopCount(Number(e.target.value))}
                min="1"
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Analyze
            </button>
          </form>

          {results.length > 0 && (
            
            <div className={styles.results}>
              <h2>Top {topCount} Colors:</h2>
              <div className="row">
                {results.map(({ color, count }) => (
                
                  <div className="col-md-4 mb-4" key={color}>
                    
                    <div className={`card`}>
                      <div
                        className=""
                        style={{
                          backgroundColor: color + ' !important', 
                          height: "150px",
                        }}
                      ></div>
                      <div className="card-body">
                        <h5 className="card-title">{color.toUpperCase()}</h5>
                        <p className="card-text">Count: {count}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
