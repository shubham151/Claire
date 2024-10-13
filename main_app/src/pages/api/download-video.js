import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  if (req.method === "POST") {
    const { url } = req.body;

    try {
      // Send the TikTok URL to the Flask microservice to download the video
      const flaskResponse = await fetch("http://localhost:5000/api/download_video", {
        method: "POST",
        headers: {  
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!flaskResponse.ok) {
        return res.status(flaskResponse.status).json({ error: "Failed to download video" });
      }
      

      const folderPath = path.resolve("./public/uploads");

      const files = fs.readdirSync(folderPath);

      return res.status(200).json({ files });


    } catch (error) {
      console.error("Error in processing video:", error);
      return res.status(500).json({ error: "Internal Server Error" });
    }
  } else {
    // Handle unsupported HTTP methods
    res.setHeader("Allow", ["POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
