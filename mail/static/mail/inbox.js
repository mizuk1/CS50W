document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
};

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Query the API for the latest emails in that mailbox
  fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Get the selector for the emails view
      const emailsView = document.querySelector('#emails-view');
      // ... do something else with emails ...
      emails.forEach(email => {
        // Create new div to print emails
        const emailDiv = document.createElement('div');
        // Add bootstrap classes
        emailDiv.classList.add('d-flex', 'align-items-center', 'border');
        // Add a value attribute with the email's id
        emailDiv.setAttribute('value', `${email.id}`);
        emailDiv.setAttribute('id', 'email');

        if (email.read) {
          emailDiv.classList.add('bg-light');
        } else {
          emailDiv.classList.add('bg-white');
        }
        // Attach email information to the div
        emailDiv.innerHTML = `
        <p class="m-2"><b>${email.sender}</b></p>
        <p class="m-2">${email.subject}</p>
        <p class="m-2" style="margin-left: auto!important;">${email.timestamp}</p>
        `;

        // Create archive button
        const archiveButton = document.createElement('button');
        // Add clases to button
        archiveButton.classList.add('btn', 'btn-sm', 'btn-outline-primary');
        archiveButton.innerHTML = email.archived ? "Unarchive" : "Archive";

        // Listen to a click event on that div
        emailDiv.addEventListener('click', function () {
          load_email(`${emailDiv.getAttribute('value')}`)
        });

        // Listen to a click event on the button
        archiveButton.addEventListener('click', function () {
          const isArchived = email.archived;
          // Update archived atribute
          fetch(`emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: !isArchived
            })
          })
            .then(() => {
              load_mailbox('inbox');
            })
        });
        

        emailsView.appendChild(emailDiv);
        if (mailbox != 'sent'){
          emailsView.appendChild(archiveButton);
        }
      });
    });
}

function load_email(email_id) {
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Update read atribute to true
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  // Get the selector for the email view
  const emailView = document.querySelector('#email-view');
  // Clean email view
  emailView.innerHTML = "";
  // Get request to receive the email's information
  fetch(`emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Create a header for the email
      const emailHead = document.createElement('div');
      // Add info to the header
      emailHead.innerHTML = `
        <p class="m-2"><b>From: </b>${email.sender}</p>
        <p class="m-2"><b>To: </b>${email.recipients}</p>
        <p class="m-2"><b>Subject: </b>${email.subject}</p>
        <p class="m-2"><b>Timestamp: </b>${email.timestamp}</p>
        `;

      // Create save button
      const replyButton = document.createElement('button');
      // Add clases to button
      replyButton.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'm-2');
      replyButton.innerHTML = "Reply";

      // Create email's body
      const emailBody = document.createElement('div');
      emailBody.innerHTML = `
        <hr>
        <pre class="m-2">${email.body}</pre>
      `;

      

      replyButton.addEventListener('click', function () {
        compose_email();
        // Fill in values
        let subject;
        if (/Re/i.test(email.subject)){
          subject = email.subject;
        } else {
          subject = "Re: " + email.subject;
        }
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
      });

      // Append divs and buttons to main div
      emailView.append(emailHead);
      emailView.append(replyButton);
      emailView.append(emailBody);
    });
}

function send_email(event) {
  // Prevent to submit the form
  event.preventDefault();

  // Get the form values
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send a post request to save the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result)
      load_mailbox('sent');
    });
}