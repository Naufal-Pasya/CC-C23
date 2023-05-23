const express = require(`express`);
const app = express();
const PORT = process.env.PORT || 8080;

const api = require('./api');

app.get('/', (req, res) => {
    res.send('Capstone Project C-23')
})

app.use(express.json());
app.use('/api',api)

app.listen(PORT, () => {
    console.log(`Server Running on PORT ${PORT}`)
})

module.exports = app;