// gotten the code from https://codelabs.developers.google.com/codelabs/sign-in-with-google-button#1

function decodeJwtResponse(token) {
  let base64Url = token.split('.')[1];
  let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  let jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  return JSON.parse(jsonPayload);
}

function handleCredentialResponse(response) {
  sendJwtToBackend(response.credential); // sending the token to the backend endpoint app.py
  
  // for debugging purposes, printing out the user information. TODO: remove this in deployment 
  const responsePayload = decodeJwtResponse(response.credential); // should decode in backend

  console.log("ID: " + responsePayload.sub); // this is the most important field, the unique and unchangable ID of the user
  console.log('Full Name: ' + responsePayload.name);
  console.log('Given Name: ' + responsePayload.given_name);
  console.log('Family Name: ' + responsePayload.family_name);
  console.log("Image URL: " + responsePayload.picture);
  console.log("Email: " + responsePayload.email);
}

async function sendJwtToBackend(jwt) {
  try {
    const response = await fetch('/auth/google', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ token: jwt })
    });

    const data = await response.json();
    console.log('Response from backend:', data);

    if (data.success) {
      console.log('User signed in successfully: ', data.message);
      // window.location.href = "/";
    } else {
      console.error('wrong sign-in information:', data.message);
    }
  } catch (error) {
    console.error('Error: ', error);
  }
}