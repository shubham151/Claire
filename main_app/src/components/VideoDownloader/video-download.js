"use client"
import React, { useState, useEffect } from "react";
import { Button, Form, ListGroup, Row, Col  } from "react-bootstrap";
import styles from '@/styles/video.module.css';

const defaultUrl = `http://${window.location.hostname}:3000/uploads/`;

const TikTokDownloader = ({  }) => {
  const [videoUrl, setVideoUrl] = useState("");
  const [downloadedVideos, setDownloadedVideos] = useState([]);

  const fetchDownloadedVideos = async () => {
    try {
      const response = await fetch("/api/get-downloaded-videos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(),
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const videos = await response.json();
      setDownloadedVideos(videos.files);
    } catch (error) {
      console.error("Failed to fetch videos:", error);
    }
  };

  useEffect(() => {
    fetchDownloadedVideos();
  }, []);

  const handleDownload = async () => {
    if (!videoUrl) return;

    try {
      const response = await fetch("/api/download-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoUrl}),
      });

      if (!response.ok) {
        throw new Error(`Download failed: ${response.status}`);
      }

      const responseData = await response.json();
      setVideoUrl("");
      setDownloadedVideos(responseData.files);
      fetchDownloadedVideos();
    } catch (error) {
      console.error("Failed to download video:", error);
    }
  };

  return (
    <div className={styles.app}>
      <div className={styles.videoBg}>
        <video autoPlay loop muted>
          <source
            src="https://assets.codepen.io/3364143/7btrrd.mp4"
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className={styles.container}>
        <h1 className={styles.title}>TikTok Video Downloader</h1>

        <form onSubmit={(e) => {e.preventDefault(); handleDownload();}} className={styles.form}>
          <div className="mb-3">
            <label className="form-label" htmlFor="videoUrlInput">
              Enter TikTok Video URL
            </label>
            <input
              type="text"
              id="videoUrlInput"
              className="form-control"
              placeholder="https://www.tiktok.com/..."
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
            />
          </div>

          <Button type="submit" className="btn btn-primary">
            Download Video
          </Button>
        </form>

        <h5 className="mt-4">Downloaded Videos</h5>

        <div className={`${styles['video-previews']} mt-3`}>
          {downloadedVideos.length > 0 ? (
            <div className="d-flex flex-wrap justify-content-center ">
              {downloadedVideos.map((video, index) => (
                <div
                  key={index}
                  className={`container-flex ${styles['container-flex1']}`}
                >
                  <video controls width="240" height="480" src={defaultUrl + video}/>
                </div>
              ))}
            </div>
          ) : (
            <p>No videos downloaded yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TikTokDownloader;
