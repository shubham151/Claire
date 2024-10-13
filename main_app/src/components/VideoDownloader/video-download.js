"use client"
import React, { useState, useEffect } from "react";
import { Button, Form, ListGroup, Row, Col  } from "react-bootstrap";
import styles from '@/styles/video.module.css';
// import { useLoading } from "@/app/Loading";

const defaultUrl = `http://${window.location.hostname}:3000/uploads/`;

const TikTokDownloader = ({  }) => {
  const [videoUrl, setVideoUrl] = useState("");
  const [downloadedVideos, setDownloadedVideos] = useState([]);
//   const { setIsLoading } = useLoading();

  const fetchDownloadedVideos = async () => {
    try {
    //   setIsLoading(true)
      const response = await fetch("/api/get-downloaded-videos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(),
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const videos = await response.json();
      console.log(videos)
      setDownloadedVideos(videos.files);
    } catch (error) {
      console.error("Failed to fetch videos:", error);
    } finally {
    //   setIsLoading(false)
    }
    
  };

  useEffect(() => {
    fetchDownloadedVideos();
  }, []);

  const handleDownload = async () => {
    if (!videoUrl) return;

    try {
    //   setIsLoading(true)
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
    } finally {
    //   setIsLoading(false)
    }
  };


  return (
    <div className="p-4 border rounded shadow-sm">
      <div className="row align-items-center mb-3">
        <label className="form-label col-12 mb-2">Enter TikTok Video URL</label>
        <div className="col-10">
          <input
            type="text"
            className="form-control mb-3"
            placeholder="https://www.tiktok.com/..."
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
          />
        </div>
        <div className="col-2 text-end">
          <button onClick={handleDownload} className="btn btn-primary mb-3">
            Download Video
          </button>
        </div>
      </div>

      <h5>Downloaded Videos</h5>

      <div className={`${styles['video-previews']} mt-3`}>
        {downloadedVideos?.length > 0 ? (
          <div className="list-group">
            {downloadedVideos.map((video, index) => (
              <div
                key={index}
                className="d-flex justify-content-between align-items-start mb-2"
              >
                <div >
                  <video
                    controls
                    width="30%"
                    src={defaultUrl + video}
                    // style={{ marginRight: "10px" }}
                  />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No videos downloaded yet.</p>
        )}
      </div>
    </div>
  );
};

export default TikTokDownloader;
