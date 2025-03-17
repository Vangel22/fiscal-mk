const express = require("express");
const app = express();
const port = 3000;

app.use(express.json());

// In-memory queue for print jobs
const printQueue = [];

// Endpoint to queue a print job
app.post("/print", (req, res) => {
  const { clientId, content } = req.body;
  if (!clientId || !content) {
    return res.status(400).json({ error: "Missing clientId or content" });
  }
  printQueue.push({ clientId, content });
  res.json({ message: "Print job queued", clientId });
});

// Endpoint for client to fetch commands
app.get("/commands/:clientId", (req, res) => {
  const { clientId } = req.params;
  const command = printQueue.find((job) => job.clientId === clientId);
  if (command) {
    printQueue.splice(printQueue.indexOf(command), 1); // Remove from queue
    res.json(command);
  } else {
    res.json({ clientId, content: "" }); // No job
  }
});

app.listen(port, () => {
  console.log(`API running at http://localhost:${port}`);
});
