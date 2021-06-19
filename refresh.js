const refresh = 'refresh token you previously redeemed or had stored';

const request = fetch('http://127.0.0.1:8000/api/auth/token/refresh/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    refresh: refresh
  })
}).then(res => res.json())
  .then(data => console.log(data));

const { access } = request;

