const request = fetch('http://127.0.0.1:8000/api/auth/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'Application/json'
  },
  body: JSON.stringify({
    username: 'recedivies09',
    password: 'rcd320112'
  })
}).then(res => res.json())
  .then(data => console.log(data));

const {refresh, access} = request;