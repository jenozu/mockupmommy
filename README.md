Mockup Mommy (MVP)
Mockup Mommy is a web-based SaaS application that allows designers and online sellers to easily generate high-quality product mockup images. The MVP (Minimum Viable Product) focuses on core functionality: an authenticated user can upload an artwork image, have it automatically inserted into a predefined Photoshop mockup template (with smart object and displacement mapping for realistic effects), and then download the resulting product mockup. This MVP uses a single fixed PSD template to demonstrate the end-to-end flow of upload → process → download.

> **Important Note**: This application requires Adobe Photoshop to be installed on the system. If you don't have Photoshop installed locally, please refer to [VM_SETUP.md](VM_SETUP.md) for instructions on setting up a Windows virtual machine with Photoshop.
Purpose and Overview
The purpose of Mockup Mommy is to streamline the creation of product mockups. Instead of manually editing templates in Photoshop, users can leverage this app to automate the process. The backend uses Adobe Photoshop scripting to produce photorealistic mockups, while the frontend provides a simple interface for upload and download. This approach saves time and ensures consistency by programmatically inserting designs into mockups​
helpx.adobe.com
. By focusing on one template in the MVP, we ensure the fundamental pipeline (file upload, Photoshop automation, and file download) works reliably before expanding to more features. Key technologies:
FastAPI (Python) – Serves as the backend API, handling authentication, file uploads, and coordinating the Photoshop automation.
Adobe Photoshop + JSX – Photoshop (running on a Windows server) performs the image processing. A JSX (ExtendScript) script is used to insert the uploaded design into the PSD template and apply effects (smart object replacement, displacement mapping, etc.) for realistic results​
medium.com
.
React (JavaScript) – Provides the frontend single-page application for users to log in, upload their artwork, and preview/download the mockup image.
Environment – Windows is required on the server side due to the Photoshop dependency. (Photoshop's scripting engine is used to generate the mockup on the fly.)
MVP Feature Set
The MVP of Mockup Mommy includes the following core features:
Authenticated User Access: Users must log in (authentication can be basic for MVP) to use the service. This ensures mockup generation is available only to authorized users (e.g., for a private beta).
Artwork Upload: Users can upload a design image (e.g. PNG or JPEG). The app provides a simple upload form that sends the file to the backend.
Automatic Mockup Generation: The backend takes the uploaded image and runs an automated Photoshop process. The single available PSD template contains a smart object layer for the design; the JSX script inserts the uploaded artwork into this smart object and applies displacement mapping (to simulate realistic 3D folds or texture) and any other effects (like lighting or shadows).
High-Quality Output: Photoshop produces a high-resolution mockup image (using the template's settings, e.g. 2400x2400 pixels) with the user's design seamlessly integrated. The output is saved as an image file (PNG/JPEG).
Download Functionality: Once processing is done, the user can download the generated mockup image through the frontend. The frontend will either display the mockup for preview and provide a download link/button.
Single Template Focus: The MVP uses one fixed product mockup template (for example, a T-shirt mockup or a mug, etc.). All uploads are applied to this same template. This simplifies development while proving out the core concept.
Note: Features like selecting different templates, bulk upload, etc., are not in scope for the MVP. The goal is to get the basic upload-and-generate pipeline working reliably.
Architecture & Data Flow
The Mockup Mommy MVP follows a classic client-server architecture with an external dependency on Adobe Photoshop for image processing. The major components are the React frontend (client), the FastAPI backend (server), and the Photoshop application running a script (worker for image generation). Below is a Mermaid diagram illustrating the architecture and data flow for the MVP:
mermaid
Copy
Edit
flowchart LR
    user["Authenticated User\n(Browser)"]
    frontend["React Frontend\n(Single Page App)"]
    backend["FastAPI Backend\n(Python on Windows)"]
    photoshop["Adobe Photoshop\n(JSX Script)"]

    user -->|1. Upload design| frontend
    frontend -->|2. HTTP POST /generate| backend
    backend -->|3. Invoke Photoshop JSX| photoshop
    photoshop -->|4. Generate mockup image| backend
    backend -->|5. HTTP Response (image)| frontend
    frontend -->|6. Provide download| user
Step-by-step data flow:
User Uploads Design: The authenticated user selects an artwork file in the React web app and initiates an upload.
Frontend API Call: The React frontend sends the file (via an HTTP POST request) to the FastAPI backend (to an endpoint, e.g. /generate or /upload). This request includes the image file data and the user's auth token/session info.
Backend Processing: The FastAPI backend receives the file, saves it to a temporary location, and then triggers the Photoshop automation script. This is done by calling Adobe Photoshop on the server with a JSX script. (Photoshop's scripting interface allows external programs to drive it via JavaScript​
helpx.adobe.com
.) The script opens the preset PSD template, inserts the uploaded design into the smart object layer, applies displacement maps or other filters, then saves the resulting mockup image to an output file.
Mockup Generation: Adobe Photoshop (running on the Windows server) executes the JSX script headlessly. It replaces the placeholder in the template with the user's artwork and renders the final mockup. Once done, Photoshop saves the output image (e.g., in a output/ directory or in-memory stream).
Backend Responds: After Photoshop finishes, the FastAPI backend reads the generated image file and responds to the frontend's request with the image (or a URL to download it). The backend may send the image as binary data or provide a link depending on implementation.
Frontend Displays Result: The React frontend receives the response. If it's the image data, it will display a preview of the mockup to the user and provide a download button. If it's a URL, the frontend will prompt the user to download the image. The user can then save the high-quality mockup file to their device.
Architecture notes:
The FastAPI backend contains the logic to authenticate users, handle file uploads, and communicate with Photoshop. It is stateless aside from handling files; user authentication could be done with JWT tokens or session cookies in MVP.
Photoshop automation: We use Photoshop's ExtendScript (.jsx) to do the heavy lifting. ExtendScript is essentially JavaScript with access to Photoshop's DOM and features​
medium.com
. The .jsx script for this app is tailored to the specific PSD template (e.g., it knows the smart object layer name to replace, and may use a displacement map layer for warping the design). The backend calls Photoshop in the background (e.g., via command line or COM interface) to run this script. (Ensure that Adobe Photoshop is installed and properly licensed on the server machine.)
The React frontend is a single-page app that might use a library for file uploads (or plain XHR/fetch). It interacts with the backend API endpoints for login and for generating the mockup. Once the mockup is fetched, it uses standard HTML5 to allow the user to download the image (for example, by creating a temporary link for the blob or using the download attribute).
Data handling: Uploaded images and generated outputs might be stored in a temporary folder on the server. These are typically cleared or overwritten on each new request in MVP. In a production scenario, one might use cloud storage or a database, but for MVP local file storage is sufficient.
Project Structure
The repository is organized to separate frontend and backend components for clarity and modularity. Below is an overview of the folder structure and important files:
backend/ – Backend application (Python FastAPI)
main.py – Entry point of the FastAPI app (defines the API, including upload and download endpoints, and possibly authentication).
routes/ – (If used) a directory for route definitions, e.g. routes/upload.py for the upload logic.
services/ – (If used) contains service modules, e.g. a module that wraps Photoshop automation (function to call the JSX script).
scripts/ – Contains the Adobe Photoshop JSX script and related assets. For example:
insert_design.jsx – The ExtendScript code that Photoshop executes to insert the uploaded image into the template and export the result.
template.psd – The Photoshop mockup template file used in the MVP (placed on the server to be loaded by the script).
(Note: The PSD might be large; it could be stored outside of version control if needed, but for a dev environment it's kept here for simplicity.)
requirements.txt – Python dependencies (e.g. FastAPI, Python libraries for handling files, maybe python-dotenv for config).
README.md – (This documentation)
Other files: You may also find config files (like .env for environment variables, e.g. Photoshop path or debug settings), and possibly a photoshop_interface.py that contains code to launch Photoshop with the script (e.g. using subprocess or a COM automation library).
frontend/ – Frontend application (React)
src/ – React source code (components, hooks, pages). Key parts might include:
App.js / App.tsx – Main React application component.
components/UploadForm.jsx – A component for the upload form (with file input and submit button).
components/MockupPreview.jsx – A component to display the returned mockup image and provide a download link.
api/index.js – API helper functions (for making requests to the FastAPI backend, e.g. using fetch or Axios).
auth/ – (If implemented) utilities for authentication (login form, managing JWT or session token).
public/ – Static files and the HTML template for React.
package.json – Node.js dependencies and scripts for the frontend (likely includes libraries like React, maybe a UI framework, etc.).
README.md – (Could include instructions specific to the frontend, if separate).
assets/ (optional) – This could include design assets like sample input images or output examples. (In some setups, the PSD template might reside here or in backend/scripts as noted.)
By structuring the project this way, the frontend and backend can be developed and tested independently. They communicate via HTTP API calls, which means the frontend could even be deployed separately from the backend service. The Photoshop-specific code is isolated in scripts or service modules so it can be modified or extended (for new templates or effects) without touching the API or frontend logic.
Setup and Installation
Setting up the Mockup Mommy MVP on a development machine involves preparing the backend (with Photoshop) and the frontend. The following guide assumes a Windows 10/11 environment for running the backend, since Photoshop automation requires Windows in this version. The frontend can be run on any OS (even the same Windows machine).
Prerequisites
Windows machine with Adobe Photoshop installed: Photoshop CC 2022 or later is recommended. Ensure you have a valid license. (The automation script is tested with Photoshop's scripting engine. You may need to enable "Allow Scripts to Write Files and Access Network" in Photoshop's preferences > Scripting, so that the JSX script can run without interruptions.)
Python 3.9+ installed on the machine. (The FastAPI backend runs on Python. It's good to use a recent version for compatibility with FastAPI and dependencies.)
Node.js (v14 or above) and npm/yarn installed. (Required to run and build the React frontend.)
Git installed (to clone the repository, or you can download the ZIP of the project).
Backend Setup (FastAPI + Photoshop)
Clone the repository:
bash
Copy
Edit
git clone https://github.com/yourusername/mockup-mommy.git
cd mockup-mommy
(If the frontend and backend are in separate repos, clone both; but in this MVP, assume one repo contains both.)
Create a Python virtual environment: (optional but recommended for development)
bash
Copy
Edit
python -m venv env
env\Scripts\activate  (on Windows)
This will isolate the Python dependencies for this project.
Install backend dependencies:
bash
Copy
Edit
cd backend
pip install -r requirements.txt
This installs FastAPI, Uvicorn (ASGI server), and any other needed libraries. Make sure the installation succeeds.
Configure environment variables (if needed):
The backend might require knowing the path to Photoshop or the template. Open backend/main.py (or a config file) and check if there are configurations for:
PHOTOSHOP_PATH – path to the Photoshop executable. For example:
C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe
By default, the code might assume Photoshop is in your system PATH or at a standard location. If not, update the path accordingly.
TEMPLATE_PATH – path to the PSD template file. This might be set to a relative path (e.g. scripts/template.psd). Ensure that file exists (it should be included in the repo under backend/scripts/). If you moved it, update the path.
Other settings: e.g. output directory, etc. (By default, the script may output to backend/output/ or similar.)
Start the FastAPI server:
In the backend directory, run the server using Uvicorn:
bash
Copy
Edit
uvicorn main:app --reload --host 127.0.0.1 --port 8000
This will start the FastAPI development server on localhost:8000. The --reload flag makes it auto-restart on code changes (useful during development). You should see console logs indicating the server is running.
Note: The first time a mockup generation request is made, Photoshop will be invoked. Photoshop may take a few seconds to launch if not already open. Keep an eye on the console for any errors (e.g., if Photoshop is not found or script errors). If everything is set up correctly, there should be a log like "Invoking Photoshop script..." and eventually "Mockup generated" or similar.
(Photoshop background note): You do not need to manually open Photoshop; the backend will launch it via the script. However, you might see Photoshop GUI briefly when the script runs (unless Photoshop can run minimized). This is normal for the MVP. Do not close Photoshop while the server is running; subsequent requests may reuse the same Photoshop process.
Frontend Setup (React)
Install frontend dependencies:
Open a new terminal (you can keep the backend running in the first terminal). Navigate to the project folder and then:
bash
Copy
Edit
cd frontend
npm install   # or use yarn install if you prefer
This will install all the Node.js packages required for the React app.
Configure frontend (if needed):
In most cases, the React app will have a configuration pointing to the backend API URL. For development, it might default to http://localhost:8000. Check any config file or .env in frontend for an API base URL. If you plan to access the backend from a different host or port, update it here. (For example, if testing on a local network, set REACT_APP_API_URL accordingly.)
Run the React development server:
bash
Copy
Edit
npm start
This starts the React app in development mode, typically at http://localhost:3000. Your browser should automatically open; if not, open that URL manually. You should see the Mockup Mommy web app interface load.
Use the app:
Register or log in (for MVP, this might be a placeholder form or a fixed test account, depending on implementation).
Go to the upload form, choose an image file (e.g., a PNG design), and submit.
The app will show a loading indicator (if implemented) while the backend processes the image. Photoshop will be doing the work on the server at this time.
After a short wait, the result should appear: the generated mockup image will be displayed. You can then click a download button to save it.
Try different images to see how they look on the mockup. (Remember, currently there's only one mockup style available.)
Troubleshooting setup:
If the FastAPI server isn't responding, check that it's running on port 8000 and that the frontend is calling the correct URL (CORS issues might appear if the domains differ; in development both are localhost, which is fine).
If Photoshop doesn't launch or the script fails, run the backend with logging enabled. Common issues could be incorrect paths or Photoshop security settings. Ensure the JSX script is in place. You can also manually open Photoshop and run the JSX script (File > Scripts > Browse in Photoshop) with a test image to verify the script works.
If the React app fails to compile or load, ensure Node version is compatible and all dependencies installed. You might need to adjust the proxy settings in development to point to the backend if using a proxy in package.json (some setups use a proxy for API calls in development).
Future Upgrades and Roadmap
While this MVP delivers the basic functionality, there are many enhancements planned for future versions. Some anticipated upgrade paths include:
Multiple Mockup Templates: Support for multiple PSD templates and mockup types. Users would be able to choose from a selection of product templates (t-shirts, mugs, posters, etc.) instead of being limited to one. This involves managing a library of PSD files and possibly generating thumbnails/previews for each option. The backend would need to load the chosen template's JSX or adjust the script to handle different templates dynamically.
Template Selection UI: Along with multiple templates, the frontend will feature a gallery or dropdown for template selection. This improves the user experience by letting them pick the context for their design (e.g., placing their artwork on a canvas print vs. a t-shirt).
Job Queue & Async Processing: As usage scales, generating mockups synchronously might not be ideal (each job can be slow and resource-intensive). We plan to introduce a background job queue (using something like Celery or RQ for Python). The FastAPI server would enqueue a job when an upload is received, and a worker process would handle running Photoshop. This allows processing multiple requests in parallel and improves reliability (the web request can return quickly and the result can be fetched later or pushed via WebSocket/notification when ready).
Etsy API Integration: For users who sell on platforms like Etsy, we aim to integrate with the Etsy API. This could allow Mockup Mommy to pull in a user's existing product listings or design files directly from their Etsy store, generate mockup images, and even upload the new images back to Etsy automatically. Such integration streamlines the workflow for online sellers – they can update their product photos with new mockups in a few clicks. (This would involve OAuth for Etsy, fetching listing data, and using Etsy's endpoints to upload images.)
Other Platform Integrations: Beyond Etsy, consider integration with print-on-demand services (e.g., Printful, Printify) or e-commerce platforms (Shopify, WooCommerce) so that mockups can be used directly in those contexts.
Improved Authentication & User Management: The MVP's auth system might be basic; future versions could implement a robust user management system (email verification, password reset, OAuth login options, etc.), possibly using a SaaS auth provider (Auth0, Firebase Auth) for reliability.
Performance and Scalability: Future upgrades would optimize the Photoshop automation. For instance, if Adobe provides a headless API or if a switch to a different image processing library becomes viable (to avoid needing a full Photoshop instance for each request), that could be explored. We might also containerize the application (e.g., using Docker with a Windows container for Photoshop, or splitting frontend/backend containers) to ease deployment.
UI/UX Enhancements: A more polished frontend with progress indicators during generation, better error messages (e.g., if the image is too large or the wrong format), and a history gallery of generated mockups for the user's session. Also, eventually adding features like image cropping or positioning within the template (for example, allowing the user to adjust how their design is placed on the product).
File Storage & Gallery: Persisting user uploads and outputs (with user's account) so they can re-download previous mockups or manage their designs. This likely involves a database and cloud storage in a production scenario – which is outside MVP scope but important for a full SaaS offering.
Each of these future improvements will be approached once the core MVP is validated. The emphasis will remain on clarity and modularity – for example, adding a new template should be as simple as adding a new PSD file and maybe a config, thanks to a modular design of the generation script, and integrating a queue should require minimal changes to the API layer. By building on a solid foundation from this MVP, Mockup Mommy can evolve into a robust service for all kinds of product mockup generation needs.