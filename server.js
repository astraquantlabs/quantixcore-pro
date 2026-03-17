import express from "express";
import cors from "cors";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const OPENAI_KEY = process.env.OPENAI_KEY;
const TAVILY_KEY = process.env.TAVILY_KEY;

app.post("/chat", async (req, res) => {
  const { message, history } = req.body;

  try {
    // 🔎 Search API
    const searchRes = await fetch("https://api.tavily.com/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        api_key: TAVILY_KEY,
        query: message,
        search_depth: "advanced"
      })
    });

    const searchData = await searchRes.json();
    const results = searchData.results
      .map(r => r.content)
      .join("\n");

    // 🧠 AI API
    const aiRes = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${OPENAI_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: "You are AstraQuant AI. Use search results to give accurate answers."
          },
          {
            role: "system",
            content: `Search Data:\n${results}`
          },
          ...history,
          { role: "user", content: message }
        ]
      })
    });

    const aiData = await aiRes.json();

    res.json({
      reply: aiData.choices[0].message.content,
      sources: searchData.results.slice(0, 3)
    });

  } catch (err) {
    res.status(500).json({ error: "Error processing request" });
  }
});

app.listen(3000, () => console.log("🚀 AstraQuant v3 running on port 3000"));