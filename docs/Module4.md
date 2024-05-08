## Guide for Web Server Frontend and Backend Implementation

### Part 1: Frontend: JavaScript
The JavaScript code provided in `index.js` is responsible for handling user interactions on the frontend of a web application. Here's a breakdown of its key functions and how they relate to the backend server operations:

1. **Selecting Elements from the DOM**
   ```javascript
   const loginForm = document.getElementById('loginForm');
   ```
   - Elements like forms and buttons are selected from the HTML document. These elements are used to interact with the user, such as taking input or handling button clicks.

2. **Event Listeners and Form Submission**
   ```javascript
   loginForm.addEventListener('submit', function(e) {
       e.preventDefault();
       const username = document.getElementById('username').value;
       const password = document.getElementById('password').value;
       ...
   });
   ```
   - An event listener is added to the login form. When the form is submitted, it prevents the default form submission action, retrieves the username and password from the form, and prepares to send these as a POST request.

3. **Making an HTTP POST Request**
   ```javascript
   fetch('/login', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify({username, password})
   })
   ```
   - This sends a POST request to the server at the `/login` endpoint. It includes the username and password in JSON format. This is where the frontend interacts directly with the backend.

4. **Handling Server Responses**
   ```javascript
   .then(response => response.json())
   .then(data => {
       if (data.success) {
           ...
       } else {
           ...
       }
   })
   ```
   - After sending the POST request, the frontend handles the JSON response from the server. Based on the response (`data.success`), it either shows a success message and redirects the user or displays an error message.

### Part 2: Backend: Python

### HTTP Requests: GET and POST

Before diving into the coding part, it's crucial to understand the basics of HTTP requests:

- **GET Request**: This request is used to retrieve data from a server at the specified resource. For example, when a browser requests a page from a server, it sends a GET request. The response from the server will typically be the content of the page requested.

- **POST Request**: Unlike GET, POST requests are used to send data to a server to create/update a resource. The data sent to the server with POST is stored in the request body of the HTTP request.

### Start Code Explanation

The start code provided sets up basic methods within a Python class handling HTTP requests:

#### `redirect_handler`
This function handles the redirection from non-host addresses to a designated host address.
##### Definition and Parameters
- **`def redirect_handler(self, redirect_domain, host):`**
  - `self`: This usually refers to the instance of the class that contains this function. It's commonly used in object-oriented programming to access properties and methods of the instance.
  - `redirect_domain`: This parameter represents the domain name to which the request will be redirected.
  - `host`: This represents the original host that the client tried to access.

##### Function Body
- **`self.send_response(302)`**
  - This function sends an HTTP response to the client with a status code of **302**. In HTTP, status codes like 302 represent "Found", which means the requested resource is temporarily moved to a different location. It's used to indicate a temporary redirection.

- **`self.send_header('Location', f'{protocol}://{redirect_domain}/?original_host={host}')`**
  - The `send_header` function sets an HTTP header for the response. In this case, the `'Location'` header is set to a specific URL.
  - The URL is created dynamically using Python's formatted strings (`f''`). It includes:
    - `protocol`: This likely refers to the communication protocol (`http` or `https`).
    - `redirect_domain`: The domain to which the client will be redirected.
    - `original_host={host}`: A query parameter indicating the original host the client tried to access. This information is typically used by the new server to understand the context of the redirection.

- **`self.end_headers()`**
  - This method finalizes the HTTP response by sending the headers set previously to the client.

##### Why is this function used?
The `redirect_handler` function is designed to handle the redirection of HTTP requests. Here's a scenario where this might be useful:
- When a user tries to access a certain website but needs to be redirected to a different site first. For example, a captive portal in a public Wi-Fi network often redirects users to a login page before allowing them to access the broader internet.
- By sending a 302 response and specifying a new location via the `Location` header, the server effectively tells the client's browser to automatically navigate to the specified URL.

#### `request_handler`
This function manages serving files based on the request path.

##### Function Overview
The `request_handler` function is designed to serve files from a directory based on the HTTP request path received by the server. It dynamically sets the content type based on the file extension and handles file not found errors.

##### Function Body
- **Request Path Handling**
    - ```python
        path = self.path.split('?', 1)[0]
        ```
    - `self.path` contains the requested URL path.
    - `.split('?', 1)[0]` splits the path at the first occurrence of '?'. This is used to separate the actual path from query parameters. The `[0]` selects the path part, ignoring any query strings.

    - ```python
        if path == '/':
            path = '/index.html'
        elif '.' not in path:
            path += '.html'
        ```
    - This code block checks if the path is just `'/'` (root path), it defaults to serving the `index.html` file. If the path does not contain a dot, assuming it is a directory or a file without an extension, it appends `.html` to it. This means it tries to serve an HTML file by default if no file type is specified.

- **Content Type Setting**
    - ```python
        if path.endswith(".html"):
            mimetype = 'text/html'
        elif path.endswith(".css"):
            mimetype = 'text/css'
        elif path.endswith(".js"):
            mimetype = 'application/javascript'
        else:
            mimetype = 'text/plain'
        ```
    - Based on the file extension in the path, the function sets the MIME type (`mimetype`). This tells the browser what kind of file is being sent so it can handle it correctly.
      - `.html` files are sent as `text/html`.
      - `.css` files are sent as `text/css`.
      - `.js` files are sent as `application/javascript`.
      - All other file types are sent as `text/plain`.

- **File Serving**
    - ```python
        try:
            with open(f'../web/{path[1:]}', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found: %s' % path)
        ```
    - `open(f'../web/{path[1:]}', 'rb')` attempts to open the file from the `web` directory located one level up from the current directory. The file is opened in binary read mode (`'rb'`).
    - `self.send_response(200)` sends a successful HTTP status code (200 OK).
    - `self.send_header('Content-type', mimetype)` sets the HTTP header for the content type based on the file's MIME type.
    - `self.end_headers()` sends the end of the HTTP headers to the client.
    - `self.wfile.write(file.read())` writes the content of the file to the response stream sent to the client.
    - If the file does not exist, `FileNotFoundError` is caught, and a 404 error is returned to the client indicating the file was not found.

##### Why This Function Is Used
This function is crucial for serving static files in a web application. It dynamically handles requests for different file types, ensures the correct content type, and provides basic error handling for missing files. This teaches fundamental concepts of HTTP, file handling, and dynamic response generation in web programming.

### How Does a Captive Portal Work?
1. **Redirection:** When a user connects to the network and tries to browse the web, they are redirected to the captive portal, typically via HTTP redirection.
2. **Authentication or Information Display:** The portal usually contains a form for user authentication or provides information about the terms of use.
3. **Access Control:** If the user authenticates or agrees to the terms, they are then granted access to the Internet.

#### HTTP Requests in Captive Portals
- **GET Requests:** These are used to retrieve information from the server. In captive portals, it's used to request the portal page or other network resources.
- **POST Requests:** Typically used to send data (like login credentials) to the server for processing.

#### Implementing the `do_GET` Method
The `do_GET` method will handle GET requests received by the captive portal. Based on the `host` value (domain name), it will either redirect to the captive portal page or serve the requested content.

##### Helper Functions for do_GET
- **`redirect_handler(self, redirect_domain, host)`:** This function will handle the redirection to the captive portal.
- **`request_handler(self)`:** This function will handle serving the regular content requested.

##### Implementation Steps of `do_GET`

The `do_GET` function handles incoming HTTP GET requests. In the context of a captive portal, it decides whether to serve the normal content or redirect the user to the captive portal page.

Here's a basic outline of how the function works:

- **Get Host Header**: The host header is extracted from the incoming request. This helps determine if the request was made to the captive portal domain.

1. **Check if Host Matches Captive Portal**: If the requested host is different from the captive portal's host:
    - **Redirect to Captive Portal**: The `redirect_handler` function is used to handle the redirection to the captive portal page.

2. **Serve Normal Content**: If the host matches the captive portal's host, the `request_handler` function serves the normal content.

#### Understanding the `do_POST` Function

1. Retrieve Request Details:
  - `request_ip = self.client_address[0]`: Fetches the IP address of the client making the request.
  - `mac_address = self.get_mac(request_ip)`: Calls the helper function to get the MAC address of the client, used to uniquely identify network devices.

2. Read Incoming Data:
  - `content_length = int(self.headers['Content-Length'])`: Determines the size of the incoming data.
  - `post_data = self.rfile.read(content_length)`: Reads the POST data based on the content length.

3. Handle Specific Paths:
  - `path = self.path.split('?', 1)[0]`: Extracts the path from the URL, ignoring any query parameters.

4. Process `/login` Path:
  If the path is `/login`, the code:
  - **Parse JSON Data:** 
    - `data = json.loads(post_data)`: Converts the JSON data into a Python dictionary.
    - If parsing fails, an error is sent back (`self.send_error(400, 'Invalid JSON')`).

  - **Validate Credentials:** 
    - The function should validate the username and password (currently, it's a placeholder with `if True:`).
    - This validation should check for username `'test'` and password `'pass'`.

  - **Update POX:**
    - If the credentials are correct, use `global_tcp_client.set_valid` to send the MAC address back to POX, indicating that the user is authenticated.

  - **Generate Response:**
    - Send an appropriate response based on whether the authentication was successful or not.

5. Handle Other Paths:
  For any other path:
  - Return a `404 Not Found` response, indicating the path doesn't exist.

### Implementing the `do_POST` Method

1. Implement Credential Validation:
  - **Understand the Requirement:** Credentials must be checked to ensure the user is authorized. The provided credential requirements (username and password) are simple for teaching purposes.
    
  - **Access the Credentials:** The incoming data (`post_data`) contains the username and password. The data is already converted into a dictionary using `json.loads()`, you just need to extract these credentials.

  - **Validation Logic:** 
    - Write code to check the extracted username and password against the expected values.
    - If they match, proceed to the next step of sending data to POX.
    - If they don't match, you don't need to do anything because the HTTP server returns the raw value of the response {'success': False}

2. Communicate with POX Server:
  - **Understand the Objective:** After successful credential validation, you need to inform the POX controller that the MAC address associated with the client is now authorized.

  - **Use Helper Functions:**
    - The provided helper function, `global_tcp_client.set_valid`, is used to communicate with POX. Pass the MAC address to this function.
