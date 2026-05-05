import os
import subprocess
import json
from pathlib import Path
import tempfile
import logging
from typing import Optional
import time
import psutil
import signal

class PhotoshopService:
    def __init__(self):
        # Initialize paths
        self.base_dir = Path(os.path.dirname(os.path.dirname(__file__)))
        self.templates_folder = self.base_dir / "templates"
        self.output_folder = self.base_dir / "output"
        self.uploads_folder = self.base_dir / "uploads"
        
        # Create necessary directories
        self.templates_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=self.base_dir / "photoshop_automation.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Find Photoshop path
        self.photoshop_path = self._find_photoshop_path()
        if not self.photoshop_path:
            raise Exception("Photoshop installation not found")

    def _find_photoshop_path(self) -> Optional[str]:
        """Find the Photoshop executable path."""
        possible_paths = [
            r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2022\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2021\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop CC 2019\Photoshop.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _kill_photoshop_processes(self, force: bool = False):
        """Kill any running Photoshop processes.
        
        Args:
            force: If True, use SIGKILL instead of SIGTERM
        """
        killed_pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Check both process name and any child processes
                if any(ps_name in proc.info['name'].lower() for ps_name in ['photoshop', 'ps_helper']):
                    pid = proc.info['pid']
                    self._log_message("info", f"{'Force killing' if force else 'Terminating'} Photoshop process: {pid}")
                    
                    if force:
                        proc.kill()  # SIGKILL
                    else:
                        proc.terminate()  # SIGTERM
                        
                    try:
                        proc.wait(timeout=5)  # Wait up to 5 seconds for graceful termination
                    except psutil.TimeoutExpired:
                        if not force:
                            # If normal termination failed, force kill
                            self._log_message("info", f"Force killing unresponsive Photoshop process: {pid}")
                            proc.kill()
                            proc.wait(timeout=5)
                    
                    killed_pids.append(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
                self._log_message("error", f"Error killing process: {str(e)}")
                continue
        
        return killed_pids

    def _log_message(self, level: str, message: str):
        """Log messages to file and print to console."""
        if level == "info":
            logging.info(message)
        elif level == "error":
            logging.error(message)
        print(message)

    def _create_jsx_script(self, input_path: str, template_path: str, output_path: str) -> str:
        """Create the JSX script for Photoshop automation."""
        # Convert Windows paths to forward slashes for JSX
        input_path = str(input_path).replace('\\', '/')
        template_path = str(template_path).replace('\\', '/')
        output_path = str(output_path).replace('\\', '/')
        
        return f"""#target photoshop

// Disable all UI updates and dialogs
app.displayDialogs = DialogModes.NO;
app.scriptingBuildDate;

// Performance optimizations
app.preferences.rulerUnits = Units.PIXELS;
app.preferences.typeUnits = TypeUnits.PIXELS;
app.preferences.interpolation = ResampleMethod.BICUBIC;
app.preferences.maximumHistoryStates = 1;

// Disable refresh
app.preferences.dynamicColorSliders = false;
app.preferences.useHistoryLog = false;
app.preferences.optimizeForFileSizes = true;

function forceQuitPhotoshop() {{
    try {{
        // First try the executeAction method
        var idquit = charIDToTypeID('quit');
        executeAction(idquit, undefined, DialogModes.NO);
    }} catch(e) {{
        try {{
            // If that fails, try alternate method
            app.quit();
        }} catch(e2) {{
            // Both methods failed
            return false;
        }}
    }}
    return true;
}}

function processImage() {{
    var doc = null;
    var imageDoc = null;
    var success = false;
    
    try {{
        // Open the mockup template
        var templateFile = new File("{template_path}");
        if (!templateFile.exists) {{
            forceQuitPhotoshop();
            return false;
        }}
        
        // Load the image we want to place
        var inputFile = new File("{input_path}");
        if (!inputFile.exists) {{
            forceQuitPhotoshop();
            return false;
        }}
        
        imageDoc = app.open(inputFile);
        imageDoc.selection.selectAll();
        imageDoc.selection.copy();
        imageDoc.close(SaveOptions.DONOTSAVECHANGES);
        
        doc = app.open(templateFile);
        
        // Find all Smart Object layers
        var smartObjLayers = [];
        for (var i = 0; i < doc.layers.length; i++) {{
            if (doc.layers[i].kind === LayerKind.SMARTOBJECT) {{
                smartObjLayers.push(doc.layers[i]);
            }}
        }}
        
        if (smartObjLayers.length === 0) {{
            doc.close(SaveOptions.DONOTSAVECHANGES);
            forceQuitPhotoshop();
            return false;
        }}
        
        // Process each Smart Object layer
        for (var j = 0; j < smartObjLayers.length; j++) {{
            try {{
                app.activeDocument = doc;
                doc.activeLayer = smartObjLayers[j];
                
                try {{
                    executeAction(stringIDToTypeID("placedLayerEditContents"), undefined, DialogModes.NO);
                }} catch(e) {{
                    executeAction(stringIDToTypeID("editSmartObject"), undefined, DialogModes.NO);
                }}
                
                var smartDoc = app.activeDocument;
                smartDoc.selection.selectAll();
                smartDoc.paste();
                
                var layer = smartDoc.activeLayer;
                var bounds = smartDoc.activeLayer.bounds;
                var width = bounds[2] - bounds[0];
                var height = bounds[3] - bounds[1];
                
                var scaleX = smartDoc.width / width * 100;
                var scaleY = smartDoc.height / height * 100;
                var scale = Math.max(scaleX, scaleY);
                
                layer.resize(scale, scale, AnchorPosition.MIDDLECENTER);
                
                var newBounds = layer.bounds;
                var deltaX = (smartDoc.width - (newBounds[2] - newBounds[0])) / 2;
                var deltaY = (smartDoc.height - (newBounds[3] - newBounds[1])) / 2;
                layer.translate(-newBounds[0] + deltaX, -newBounds[1] + deltaY);
                
                smartDoc.save();
                smartDoc.close();
            }} catch(e) {{}}
        }}
        
        // Save final result
        var saveFile = new File("{output_path}");
        var pngOptions = new PNGSaveOptions();
        pngOptions.compression = 4;
        pngOptions.interlaced = false;
        
        doc.saveAs(saveFile, pngOptions, true);
        doc.close(SaveOptions.DONOTSAVECHANGES);
        
        success = true;
    }} catch(err) {{
        if (imageDoc) {{
            imageDoc.close(SaveOptions.DONOTSAVECHANGES);
        }}
        if (doc) {{
            doc.close(SaveOptions.DONOTSAVECHANGES);
        }}
        success = false;
    }} finally {{
        // Always try to quit Photoshop, even if there was an error
        forceQuitPhotoshop();
        return success;
    }}
}}

processImage();"""

    async def generate_mockup(self, input_image_path: str, template_path: str) -> str:
        """
        Generate a mockup using Photoshop automation.
        Args:
            input_image_path: Path to the input image
            template_path: Path to the PSD template file
        Returns:
            Path to the generated mockup image
        """
        temp_jsx_path = None
        process = None
        
        try:
            # Kill any existing Photoshop processes
            self._kill_photoshop_processes()
            
            # Ensure input file exists
            input_path = Path(input_image_path)
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # Ensure template file exists
            template_file = Path(template_path)
            if not template_file.exists():
                raise FileNotFoundError(f"Template file not found: {template_file}")

            # Create output filename
            output_filename = f"mockup_{input_path.stem}_{int(time.time())}.png"
            output_path = self.output_folder / output_filename

            # Create temporary JSX script
            self._log_message("info", f"Generating mockup for {input_path.name}")
            with tempfile.NamedTemporaryFile(suffix='.jsx', mode='w', delete=False) as f:
                jsx_script = self._create_jsx_script(
                    str(input_path.absolute()),
                    str(template_file.absolute()),
                    str(output_path.absolute())
                )
                f.write(jsx_script)
                temp_jsx_path = f.name

            # Run Photoshop with the script
            process = subprocess.Popen(
                [str(self.photoshop_path), "-background", "-execute", temp_jsx_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for the process with timeout
            try:
                stdout, stderr = process.communicate(timeout=60)  # 60 seconds timeout
            except subprocess.TimeoutExpired:
                if process:
                    process.kill()
                self._kill_photoshop_processes(force=True)  # Force kill if timeout
                raise Exception("Photoshop process timed out")
            
            # Wait for output file to appear (with timeout)
            start_time = time.time()
            while not output_path.exists() and (time.time() - start_time) < 30:
                time.sleep(0.5)
            
            if not output_path.exists():
                raise Exception("Output file was not generated")
            
            # Ensure Photoshop is fully closed
            self._kill_photoshop_processes()
            
            return str(output_path)
            
        except Exception as e:
            self._log_message("error", f"Error generating mockup: {str(e)}")
            # Ensure cleanup on error
            if process:
                try:
                    process.kill()
                except:
                    pass
            self._kill_photoshop_processes(force=True)
            raise
            
        finally:
            # Clean up temporary script file
            if temp_jsx_path and os.path.exists(temp_jsx_path):
                try:
                    os.unlink(temp_jsx_path)
                except:
                    pass 