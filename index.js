const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 8080;

const api = require('./api');

app.use(cors());
app.use(express.json());
app.use('/api', api);

app.get('/', (req, res) => {
  res.send('Capstone Project C-23');
});

app.listen(PORT, () => {
  console.log(`Server Running on PORT ${PORT}`);
});

module.exports = app;