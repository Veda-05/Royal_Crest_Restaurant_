const express=require("express");
const app=express();
const bodyParser=require('body-parser')
const users=require("./users")
const cors=require('cors')

const mongoose=require('mongoose')

app.use(cors())
app.use(`/users`,users)
app.use(bodyParser.urlencoded({extended:false}))
app.use(bodyParser.json())


mongoose.connect("mongodb://localhost:27017/dream")
.then((res)=>{
  console.log("Connected successfully")
})
.catch((err)=>{
console.log(err);
})

const port=8000
app.listen(port,()=>{
  console.log(`connecting https://localhost:8000 ${port}`)
})

























// const express = require("express");
// const bodyParser = require("body-parser");
// const mongoose = require('mongoose');
// var cors = require('cors')
// const users = require("./users");
// const order = require("./order");
// const app = express();
// app.use(cors())

// app.use(bodyParser.urlencoded({ extended: false }))
// app.use(bodyParser.json())
// app.use(`/users`,users)
// app.use('/order',order)

// const connection=mongoose.connect('mongodb://localhost:27017/dream')
// .then((res)=>
//   console.log("Sucessfully Connected"))
// .catch((err)=>
//   console.log("Error")); 

// const port=8000;
// app.listen(port,()=>{
//   console.log(`connecting http://localhost:5000 ${port}`)
// })