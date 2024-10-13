import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
    if (req.method === "POST") {
      try {
        
        const folderPath = path.resolve("./public/uploads");

        const files = fs.readdirSync(folderPath);

        return res.status(200).json({ files });

  
  
      } catch (error) {
        console.error("Error fetching videos from Flask:", error);
        return res.status(400).json({ error: "Internal Server Error" });
      }
    } else {
      // Handle unsupported HTTP methods
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
  
