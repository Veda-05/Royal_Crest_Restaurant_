const express = require('express');
const bcrypt = require('bcrypt');
const Details = require('./userSchema');
const router = express.Router();
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');

router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());

// Add User Endpoint
router.post('/addUser', async (req, res) => {
  try {
    const hash = bcrypt.hashSync(req.body.password.trim(), 10);
    const emailPattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    const phonePattern = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;

    const firstname = req.body.firstname.trim().toUpperCase();
    const lastname = req.body.lastname.trim().toUpperCase();
    const email = req.body.email.trim();
    const password = hash;
    const mobile = req.body.mobile;

    if (!firstname || firstname.length <= 2) {
      if(!firstname){
        return res.send({ status: 0, Message: "Firstname is required" });
      }
      else{
        return res.send({ status: 0, Message: "Firstname must contain more than 2 characters" });
      }
    }

    if (!lastname) {
      return res.send({ status: 0, Message: "Lastname is required" });
    }

    if (!email || !emailPattern.test(email)) {
      if (!email) {
        return res.send({ status: 0, Message: "Email is required" });
      }
      else{
        return res.send({ status: 0, Message: "Invalid email" });
      }
    }

    if (!req.body.password || req.body.password.length < 8) {
      if(!req.body.password){
      return res.send({ status: 0, Message: "Password is required" });
      }
      else{
      return res.send({ status: 0, Message: "Password must contain at least 8 characters" });
      }
    }

    if (!mobile || !phonePattern.test(mobile)) {
      if(!mobile){
        return res.send({ status: 0, Message: "Mobile number is required" });
      }
      else{
        return res.send({ status: 0, Message: "Invalid Mobile number" });
      }
    }
    const emailExists = await Details.findOne({ email });
    const mobileExists = await Details.findOne({ mobile });
    if (emailExists) {
      return res.send({ status: 0, Message: "Email already exists in the database" });
    }

    if (mobileExists) {
      return res.send({ status: 0, Message: "Mobile number already exists in the database" });
    }
    const details = new Details({
      firstname,
      lastname,
      email,
      password,
      mobile,
      status: true,
    });
    await details.save();
    res.send({ status: 1, Message: "User successfully added" });
    console.log("User Added:", { firstname, lastname, email, mobile });
  } 
  catch (error) {
    res.send({ status: 0, Message: "Server Error" });
  }
});

router.get(`/userList`,async(req,res)=>{
  try{
    const decode=jwt.verify(req.headers.authorization,'P@ViThR@')
    console.log("decode",decode);
    const allUser=await Details.find({})
    res.send({status:1,data:allUser})
  }
  catch(error){
    res.send({status:0,Message:"Unauthorized User"})
  }
  })
router.post('/getUserByStatus', async (req, res) => {
  try {
    const status = req.body.status;
    const filteredUsers = await Details.find({ status });

    res.send({
      status: 1,
      statusCount: `Totally ${filteredUsers.length} ${status} status users are found`,
      data: filteredUsers,
    });
  } catch (error) {
    console.error("Error fetching users by status:", error);
    res.send({ status: 0, Message: "Server Error" });
  }
});
router.post('/login', async (req, res) => {
  try {
    const email = req.body.email.trim();
    const password = req.body.password.trim();
    const userData = await Details.findOne({ email });
    if (userData) {
      const isPasswordValid = bcrypt.compareSync(password, userData.password);
      if (!isPasswordValid) {
        return res.send("Incorrect Password");
      }
      const token = jwt.sign({ email }, 'P@ViThR@');
      res.send({ Status: 1, authToken: token });
    }
    else{
      return res.send("Email does not exist");
    }
  } 
  catch (error) {
    console.error("Error during login:", error);
    res.status(500).send({ status: 0, Message: "Server Error" });
  }
});
router.get('/changeUser', (req, res) => {
  res.send(req.headers);
});
router.post('/deleteUser', (req, res) => {
  res.send("deleteUser");
});
module.exports = router;