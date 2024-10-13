import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  if (req.method === "POST") {
    const { label, top_count } = req.body;

    try {
      // Send the TikTok URL to the Flask microservice to download the video
      const flaskResponse = await fetch("http://localhost:5000/api/search_query", {
        method: "POST",
        headers: {  
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ label, top_count }),
      });

      if (!flaskResponse.ok) {
        return res.status(flaskResponse.status).json({ error: "Failed to download video" });
      }

      let data = await flaskResponse.json();

        
    //   let data = {}
    //   data.resp = [
    //     {color: '#e31c0e', count: 426 },
    //     {color: '#e8e4e3', count: 322 },
    //     {color: '#FFFFF0', count: 59 }
    //   ]
      const { resp } = data;
      console.log(resp)
      

      

      return res.status(200).json({ "res": resp });


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
